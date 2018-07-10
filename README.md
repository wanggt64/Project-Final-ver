# SimpleOrderRoom
2018 workshopII continue exercise.
Python3.x
Simple Online Order Room

================================
### Function

#### Admin -- 
	

- Login
- Add User
- Add Room
- Manage Room order list

#### User -- 
	
- Login
- Book Room
- Manage Room list(Check - Remove order)

================================
### how to start
- install web.py
	~~~
	pip install web.py==0.40.dev0
	~~~

- create a code.py file and write some code

	~~~
	import web

	urls = (
	    '/', 'index'
	)

	class index:
	    def GET(self):
	        return "Hello, world!"

	if __name__ == "__main__":
	    app = web.application(urls, globals())
	    app.run()

	~~~

- run

	~~~
	 python3 code.py http://0.0.0.0:8080/

	 # or 
	 
	 python3 code.py 1234
	~~~

================================

### web.py -- templates

- create a folder  templates 

- create a test.html into templates folder

- test.html 
	~~~
	$def with (name)
	$if name:
	     
	    <em>Hello</em> to $name.<br> 
	    Welcome to try web.py<br> 
	$else:
	    <em>Hello</em>, CSTer!

	~~~ 

- update code.py

	~~~
	import web
	render = web.template.render('templates/')

	urls = (
	    '/(.*)', 'index'
	)

	class index:
	    def GET(self,name):
	    	return render.test(name)
	        # return "Hello, world!"


	if __name__ == "__main__":
	    app = web.application(urls, globals())
	    app.run()

	~~~

- run

	~~~
	 python3 code.py http://0.0.0.0:8080/

	 # or 
	 
	 python3 code.py 1234
	~~~

================================

### Build your UI

- create a folder 'static' fort static resources

- templates
	- login.html
	- orderlist.html
	- timetable.html
	- user.html
	- week.html

================================
	
### Database - testweb and test web.py session

- tables
	- user
		~~~
		CREATE TABLE `user` (
		  `id` int(11) NOT NULL PRIMARY KEY AUTO_INCREMENT,
		  `user_name` varchar(200) NOT NULL,
		  `user_email` varchar(200) NOT NULL,
		  `user_pass` varchar(200) NOT NULL,
		  `user_role` varchar(200) NOT NULL
		) ENGINE=InnoDB DEFAULT CHARSET=utf8;
		~~~
	- roomorder
		~~~
		CREATE TABLE `roomorder` (
		`id` int(11) NOT NULL PRIMARY KEY AUTO_INCREMENT,
		`course_title` varchar(200) NOT NULL,
		`teacher_name` varchar(200) NOT NULL,
		`uic_email` varchar(200) NOT NULL,
		`timetable_id` int(11) NOT NULL,
		`user_id` int(11) NOT NULL,
		`status` int(11) NOT NULL,
		`apply_date` varchar(200) NOT NULL
		) ENGINE=InnoDB DEFAULT CHARSET=utf8;
		~~~
	- timetable
		~~~
		CREATE TABLE `timetable` (
		`id` int(11) NOT NULL PRIMARY KEY AUTO_INCREMENT,
		`week_num` int(11) NOT NULL,
		`cell_row` int(11) NOT NULL,
		`cell_col` int(11) NOT NULL,
		`cell_content` varchar(200) DEFAULT NULL,
		`lab_room` varchar(200) DEFAULT NULL,
		`status` int(11) NOT NULL
		) ENGINE=InnoDB DEFAULT CHARSET=utf8;
		~~~
	- week
		~~~
		CREATE TABLE `week` (
		  `id` int(11) NOT NULL PRIMARY KEY AUTO_INCREMENT,
		  `week_num` int(11) NOT NULL,
		  `date_start` varchar(200) DEFAULT NULL,
		  `date_end` varchar(200) DEFAULT NULL,
		  `status` int(11) NOT NULL
		) ENGINE=InnoDB DEFAULT CHARSET=utf8;
		~~~

- modify code.py
	- modify class test

- run

	~~~
	 python3 code.py 1234
	~~~

================================


### Functions

