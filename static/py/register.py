#!C:\Python\Python35\Python.exe
import cgi, cgitb
import pymysql

form = cgi.FieldStorage()
db = pymysql.connect("172.16.199.70","l630003073","123456","l630003073")

cursor = db.cursor()

username = form.getvalue("username")
password = form.getvalue("password")
repassword = form.getvalue("repassword")
email = form.getvalue("email")
if password != repassword:
    print("Content-type:text.html")
    print()
    print("""
    <head>
    <meta http-equiv="refresh" content="1;url=http://localhost/register.html"> 
    </head>
    <body>
    <h>Failed!</h>
        """)
    os._exit(0)


sql = "SELECT user_name FROM user"
cursor.execute(sql)
results = cursor.fetchall()
for each in results:
    if each == username:
        print("Content-type:text.html")
        print()
        print("""
        <head>
        <meta http-equiv="refresh" content="1;url=http://localhost/register.html"> 
        </head>
        <body>
        <h>Failed!</h>
            """)
        os._exit(0)

sql = "SELECT user_email FROM user"
cursor.execute(sql)
results = cursor.fetchall()
for each in results:
    if each == email:
        print("Content-type:text.html")
        print()
        print("""
        <head>
        <meta http-equiv="refresh" content="1;url=http://localhost/register.html"> 
        </head>
        <body>
        <h>Failed!</h>
            """)
        os._exit(0)



sql = "INSERT INTO user (user_name, user_email, user_pass) VALUES ('%s', '%s', '%s')"
record = [(username, email, password)]
try:
    for each in record:
        cursor.execute(sql % each)
        db.commit()
        print("Content-type:text.html")
        print()
        print("""
        <head>
        <meta http-equiv="refresh" content="1;url=http://localhost/signin.html"> 
        </head>
        <body>
        <h>Success!</h>
            """)
except:
    db.rollback()
    print("Content-type:text.html")
    print()
    print("""
    <head>
    <meta http-equiv="refresh" content="1;url=http://localhost/register.html"> 
    </head>
    <body>
    <h>Failed!</h>
        """)


db.close()