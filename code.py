# coding: utf-8

import web
import hashlib
from web import form
import types 
import datetime
import random

import pymysql
pymysql.install_as_MySQLdb()

db = web.database(dbn='mysql',host='172.16.199.70', user='l630003073', pw='123456', db='l630003073')



# router
urls = (
    '/signin','signin',
    '/register','register',
    '/welcome','welcome',
    '/index','index',
    '/logout','logout',
    '/pay','pay',
    '/shopping','shopping',
    '/management','management',
    '/cart','cart',
)
#  use session to set debug to False
web.config.debug = False 
app = web.application(urls, globals())

session = web.session.Session(app, web.session.DiskStore('sessions'))

# templates
render = web.template.render('templates/',globals={'context': session})

# class

#welcome
class welcome:
    def GET(self):
        return render.welcome()
    
# shopping
class shopping:
    def GET(self):
        if session.get('logged_in'):
            return render.shopping()
        else:
            return '<h1>Signin Error!!!</h1></br><a href="/signin">signin</a>'
    def POST(self):
        if session.get('logged_in'):
            i = web.input()
            price = i.get('product')
            session.price = price
            if int(price) == 65:
                session.ptype = 1
                session.type = 'Product 1'
            if int(price) == 100:
                session.ptype = 2
                session.type = 'Product 2'
            if int(price) == 135:
                session.ptype = 3
                session.type = 'Product 3'
            uid = str(session.get('uid'))
            sql = 'select * from user where id='+uid
            resultList = list(db.query(sql))
            raise web.seeother('/cart')
        else:
            return '<h1>Signin Error!!!</h1></br><a href="/signin">signin</a>'
    
# register
class register:
    def GET(self):
        return render.register()
    def POST(self):
        i = web.input()
        name = i.get('username')
        if len(name) < 3 or len(name) > 17:
            return '<h1>The usename should more than 4 and less than 16</h1></br><a href=" ">Register</a >'
        pwd = i.get('password')
        if len(pwd) < 7 or len(pwd) > 22 :
            return '<h1>The password should more than 8 and less than 21</h1></br><a href=" ">Register</a >'
        repwd = i.get('repassword')
        email = i.get('email')
        if pwd != repwd:
            return '<h1>Password and confirm password is not the same!!!</h1></br><a href=" ">Register</a >'
        myvar = dict(user_name=name,user_pass=pwd,user_email=email)
        result1 = list(db.select('user',myvar, where="user_name=$user_name"))
        result2 = list(db.select('user',myvar, where="user_email=$user_email"))
        if result1:
            return '<h1>User name has been register!!!</h1></br><a href="/register">Register</a >'
        if result2:
            return '<h1>Email has been register!!</h1></br><a href="/register">Register</a >'
        else:
            inserts = db.insert('user',myvar, user_name=name,user_email=email,user_pass=pwd)
            return '<h1>Register Success!</h1></br><a href="/signin">Signin</a >'
        
# signin       
class signin:
    def GET(self):
        if session.get('logged_in'):
            raise web.seeother('/index')
            # return render.timetable()
        else:
            return render.signin()

    def POST(self):
        i = web.input()
        name = i.get('name')
        password = i.get('pwd')
        myvar = dict(user_name=name,user_pass=password)
        results = list(db.select('user',myvar, where="user_name=$user_name and user_pass=$user_pass"))
        if results:
            session.logged_in = True
            session.uid = results[0].id
            session.uname = results[0].user_name
            session.ubalance = results[0].balance
            session.uemail = results[0].user_email
            raise web.seeother('/index')
        else:
            return '<h1>Signin Error!!!</h1></br><a href="/signin">signin</a>'

# pay
class pay:
    def GET(self):
        if session.get('logged_in'):
            return render.pay()
        else:
            return '<h1>Signin Error!!!</h1></br><a href="/signin">signin</a>'
    def POST(self):
        if session.get('logged_in'):
            i = web.input()
            uid = str(session.get('uid'))
            pay = i.get('paymoney')
            try:
                inserts = db.update('user', balance = int(session.ubalance) + int(pay), where='id='+uid)
            except Exception:
                return '<h1>Please input number</h1></br><a href="/index">Go back</a >'
            else:
                return '<h1>Payment Success!</h1></br><a href="/index">Go back</a >'
        else:
            return '<h1>Signin Error!!!</h1></br><a href="/signin">signin</a>'

# user logout
class logout:
    def GET(self):
        session.kill()
        # session.logged_in = False
        return '<h1>Success!</h1></br><a href="/welcome">Go back</a>'

# index
class index:
    def GET(self):
        if session.get('logged_in'):
            uid = str(session.get('uid'))
            sql = 'select * from user where id='+uid
            resultList = list(db.query(sql))
            session.ubalance = resultList[0].balance
            return render.index()
        else:
            return '<h1>Signin Error!!!</h1></br><a href="/signin">signin</a>'

# cart
class cart:
    def GET(self):
        if session.get('logged_in'):   
            return render.cart()
        else:
            return '<h1>Signin Error!!!</h1></br><a href="/signin">signin</a>'
    def POST(self):
        if session.get('logged_in'):
            uid = str(session.get('uid'))
            i = web.input()
            days = i.get('days')
            notes = i.get('notes')
            price = int(session.price) * int(days)
            ptype = session.ptype
            if int(price) > int(session.ubalance):
                return '''<h1>Not enough balance!</h1></br><a href="/index">Go back</a>'''
            update = db.update('user', balance = int(session.ubalance) - int(price), where='id='+uid)
            utoday = datetime.date.today()
            dueday = datetime.date.today() + datetime.timedelta(days = 365 * int(days))
            if notes == "You can add any extra comment here.":
                notes = ''
            if ptype == 1:
                inserts = db.insert('status',id=uid,comment = notes)
            if ptype == 2:
                inserts = db.insert('status',id=uid,comment = notes)
            if ptype == 3:
                inserts = db.insert('status',id=uid,comment = notes)
            myvar = dict(id=uid)
            sql = 'select * from status where id='+uid+' ORDER BY `status`.`order_id` DESC'
            results = list(db.query(sql))
            orderid = results[0].order_id
            rport = random.randint(10000,99999)
            insertp = db.insert('product',order_id=orderid,ip='233.421.2.123',port = rport,type=ptype)
            insertt = db.insert('time',year=days,start_date=utoday,due_date=dueday,order_id=orderid,id=uid,type=ptype)
            return '<h1>Success!</h1></br><a href="/index">Go back</a>'
        else:
            return '<h1>Signin Error!!!</h1></br><a href="/signin">signin</a>'

# management
class management:
    def GET(self):
        if session.get('logged_in'):
            uid = str(session.get('uid'))
            sql1 = 'select * from status where id='+uid
            result1 = list(db.query(sql1))
            sql2 = 'select * from time where id='+uid
            result2 = list(db.query(sql2))
            return render.management(result1, result2)
        else:
            return '<h1>Signin Error!!!</h1></br><a href="/signin">signin</a>'


if __name__ == "__main__":
    app.run()
