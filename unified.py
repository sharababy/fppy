#!/usr/bin/env python

import hashlib
import time
import Adafruit_CharLCD as LCD
import sqlite3 as sq;
from pyfingerprint.pyfingerprint import PyFingerprint
from datetime import datetime
from urllib import urlencode
from urllib2 import Request, urlopen
import RPi.GPIO as GPIO

left 	= 6
right 	= 5
select 	= 16

current_menu = 0;

class Figpi:

	def setup(self):
		
		GPIO.setmode(GPIO.BCM)
		GPIO.setup(left, GPIO.IN, pull_up_down=GPIO.PUD_UP)
		GPIO.setup(right, GPIO.IN, pull_up_down=GPIO.PUD_UP)
		GPIO.setup(select, GPIO.IN, pull_up_down=GPIO.PUD_UP)

	def printMenuItem(self, item):

		if item == 1:
			self.printLCD("-Use Arrow Keys-\nTake Attendance");
		
		elif item == 2:
			self.printLCD("-Use Arrow Keys-\nEnroll Faculty");
		
		elif item == 3:
			self.printLCD("-Use Arrow Keys-\nEnroll Student");

		else:
			self.printLCD("-Use Arrow Keys-\nReady !")


	def makeMenu(self,options):
		menu = -1
		self.printLCD("-Use Arrow Keys-")
		while True:			
			if  GPIO.input(left) == False:
				
				print('Left Button Pressed...')
				
				if menu > 1:

					menu = menu-1;
					print(menu)
					self.printLCD("-Use Arrow Keys-\n"+str(options[menu][0]))

				while GPIO.input(left) == False:
					time.sleep(0.2)

			if GPIO.input(right) == False:
				
				print('Right Button Pressed...')
				
				if menu < len(options)-1:
					menu = menu+1;
					print(menu)
					self.printLCD("-Use Arrow Keys-\n"+str(options[menu][0]))

				while GPIO.input(right) == False:
					time.sleep(0.2)


			elif GPIO.input(select) == False:
				
				print('Select Button Pressed...')
				return menu;


	def execute(self,item):
		if item == 1:
			self.take_attendance();
		elif item == 2:
			self.enroll_faculty();
		elif item == 3:
			self.enroll_student();

	def startx(self):
		self.printMenuItem(0)
		global current_menu;
		while True:			
			# print("yo")
			if  GPIO.input(left) == False:
				
				print('Left Button Pressed...')
				
				if current_menu > 1:

					current_menu = current_menu-1;
					print(current_menu)
					self.printMenuItem(current_menu)
				while GPIO.input(left) == False:
					time.sleep(0.2)

			if GPIO.input(right) == False:
				
				print('Right Button Pressed...')
				
				if current_menu < 3:
					current_menu = current_menu+1;
					print(current_menu)
					self.printMenuItem(current_menu)

				while GPIO.input(right) == False:
					time.sleep(0.2)


			elif GPIO.input(select) == False:
				
				print('Select Button Pressed...')
				self.execute(current_menu);
				while GPIO.input(select) == False:
					time.sleep(0.2)

	def push_attendance(self):
		conn = sq.connect("./attendance.db");
		c  = conn.cursor();

		c.execute("SELECT * FROM attendance3 where syncstatus = 0")
		rows = c.fetchall()

		print(rows)

		url = 'http://192.168.43.143:3000/newAttendanceFile' # Set destination URL here
		post_fields = {
						'year': 3,
						'data':rows
						}     # Set POST fields here

		request = Request(url, urlencode(post_fields).encode())

		json = urlopen(request).read().decode()
		# print(json)

		c.execute("UPDATE attendance3 set syncstatus = 1 where syncstatus = 0;")

		conn.close();


	def create_class(self):
		cno = raw_input("Enter course number : ");
		name = raw_input("Enter class name : ");
		faculty = raw_input("Enter faculty id : ");
		classcount = raw_input("Enter number of classes in a semester : ");

		conn = sq.connect("attendance.db");
		c  = conn.cursor();

		c.execute(''' insert into class(cno,classcount,name,facultyid) values(?,?,?,?)''', (cno,classcount,name,faculty) )

		conn.commit();
		conn.close();




	def printLCD(self,msg):

		# Raspberry Pi pin setup
		lcd_rs = 25
		lcd_en = 24
		lcd_d4 = 23
		lcd_d5 = 17
		lcd_d6 = 18
		lcd_d7 = 22
		lcd_backlight = 2

		# Define LCD column and row size for 16x2 LCD.
		lcd_columns = 16
		lcd_rows = 2

		lcd = LCD.Adafruit_CharLCD(lcd_rs, lcd_en, lcd_d4, lcd_d5, lcd_d6, lcd_d7, lcd_columns, lcd_rows, lcd_backlight)
		lcd.clear()
		lcd.message(msg)
		

	def enroll_faculty(self):
		sha = ""

		## Enrolls new finger
		##

		## Tries to initialize the sensor
		try:
		    f = PyFingerprint('/dev/serial0', 57600, 0xFFFFFFFF, 0x00000000)

		    if ( f.verifyPassword() == False ):
		        raise ValueError('The given fingerprint sensor password is wrong!')

		except Exception as e:
		    print('The fingerprint sensor could not be initialized!')
		    print('Exception message: ' + str(e))
		    exit(1)

		## Gets some sensor information
		print('Currently used templates: ' + str(f.getTemplateCount()) +'/'+ str(f.getStorageCapacity()))

		## Tries to enroll new finger
		try:
		    print('Waiting for finger...')

		    ## Wait that finger is read
		    while ( f.readImage() == False ):
		        pass

		    ## Converts read image to characteristics and stores it in charbuffer 1
		    f.convertImage(0x01)

		    ## Checks if finger is already enrolled
		    result = f.searchTemplate()
		    positionNumber = result[0]

		    if ( positionNumber >= 0 ):
		        print('Template already exists at position #' + str(positionNumber))
		        exit(0)

		    print('Remove finger...')
		    time.sleep(2)

		    print('Waiting for same finger again...')

		    ## Wait that finger is read again
		    while ( f.readImage() == False ):
		        pass

		    ## Converts read image to characteristics and stores it in charbuffer 2
		    f.convertImage(0x02)

		    ## Compares the charbuffers
		    if ( f.compareCharacteristics() == 0 ):
		        raise Exception('Fingers do not match')

		    ## Creates a template
		    f.createTemplate()

		    ## Saves template at new position number
		    positionNumber = f.storeTemplate()
		    print('Finger enrolled successfully!')
		    print('New template position #' + str(positionNumber))

		except Exception as e:
		    print('Operation failed!')
		    print('Exception message: ' + str(e))
		    exit(1)




		sha = self.get_finger_sha();

		name = raw_input("Please enter your name?")

		conn = sq.connect("attendance.db");

		c  = conn.cursor();


		# c.execute(''' ''')



		c.execute(''' insert into faculty(name,sha) values(?,?)''', (name,sha) )


		conn.commit();

		conn.close();



	def enroll_student(self):

		try:
		    f = PyFingerprint('/dev/serial0', 57600, 0xFFFFFFFF, 0x00000000)

		    if ( f.verifyPassword() == False ):
		        raise ValueError('The given fingerprint sensor password is wrong!')

		except Exception as e:
		    print('The fingerprint sensor could not be initialized!')
		    print('Exception message: ' + str(e))
		    exit(1)

		## Gets some sensor information
		print('Currently used templates: ' + str(f.getTemplateCount()) +'/'+ str(f.getStorageCapacity()))

		## Tries to enroll new finger
		try:
		    print('Waiting for finger...')

		    ## Wait that finger is read
		    while ( f.readImage() == False ):
		        pass

		    ## Converts read image to characteristics and stores it in charbuffer 1
		    f.convertImage(0x01)

		    ## Checks if finger is already enrolled
		    result = f.searchTemplate()
		    positionNumber = result[0]

		    if ( positionNumber >= 0 ):
		        print('Template already exists at position #' + str(positionNumber))
		        exit(0)

		    print('Remove finger...')
		    time.sleep(2)

		    print('Waiting for same finger again...')

		    ## Wait that finger is read again
		    while ( f.readImage() == False ):
		        pass

		    ## Converts read image to characteristics and stores it in charbuffer 2
		    f.convertImage(0x02)

		    ## Compares the charbuffers
		    if ( f.compareCharacteristics() == 0 ):
		        raise Exception('Fingers do not match')

		    ## Creates a template
		    f.createTemplate()

		    ## Saves template at new position number
		    positionNumber = f.storeTemplate()
		    print('Finger enrolled successfully!')
		    print('New template position #' + str(positionNumber))

		except Exception as e:
		    print('Operation failed!')
		    print('Exception message: ' + str(e))
		    exit(1)


		sha = self.get_finger_sha();

		name = raw_input("Please enter your name?")
		roll = raw_input("Please enter your roll number?")

		conn = sq.connect("attendance.db");
		c  = conn.cursor();

		c.execute(''' insert into student(sha,name,roll) values(?,?,?)''', (sha,name,roll) )

		conn.commit();
		conn.close();

	def getCourses(self,sha):
		conn = sq.connect("attendance.db");
		c  = conn.cursor();

		c.execute("SELECT id FROM faculty WHERE sha = ?", (sha,))
		 
		faculty = c.fetchall()

		c.execute("SELECT cno FROM class WHERE facultyid = ?", (faculty[0][0],))
		
		courses = c.fetchall()		

		conn.commit();
		conn.close();

		return courses;

	def take_for_course(self,course,fsha):
		while True:
			self.printLCD("Place Student\nFinger Print")

			today = datetime.today()
			day = today.day
			month = today.month
			year = today.year;

			conn = sq.connect("attendance.db");
			c  = conn.cursor();

			sha = self.get_finger_sha()

			c.execute("SELECT f.id,f.name FROM faculty as f WHERE sha=?", (sha,))
			rows = c.fetchall()
			# print(rows)
			if len(rows) > 0 and sha == fsha:
				self.printLCD("Class Ended")
				time.sleep(2);
				break;

			c.execute("SELECT s.id,s.name,s.roll FROM student as s WHERE sha=?", (sha,))
			rows = c.fetchall()

			# print("Attendance given by ",rows[0][1])
			self.printLCD(rows[0][1]+"\n"+rows[0][2])

			studentid = rows[0][0]

			c.execute("SELECT c.id FROM class as c WHERE c.cno = ?", (course,))
			rows = c.fetchall()
			courseid = rows[0][0]

			c.execute("INSERT into attendance3(studentid,courseid,day,month,year,syncstatus) VALUES(?,?,?,?,?,0)", (studentid,courseid,day,month,year) )

			conn.commit();
			conn.close();
			time.sleep(2);

	def get_finger_sha(self):
		sha = ""
		## Search for a finger
		##

		## Tries to initialize the sensor
		try:
		    f = PyFingerprint('/dev/serial0', 57600, 0xFFFFFFFF, 0x00000000)

		    if ( f.verifyPassword() == False ):
		        raise ValueError('The given fingerprint sensor password is wrong!')

		except Exception as e:
		    print('The fingerprint sensor could not be initialized!')
		    print('Exception message: ' + str(e))
		    exit(1)

		## Gets some sensor information
		print('Currently used templates: ' + str(f.getTemplateCount()) +'/'+ str(f.getStorageCapacity()))

		## Tries to search the finger and calculate hash
		try:
		    print('Waiting for finger...')

		    ## Wait that finger is read
		    while ( f.readImage() == False ):
		        pass

		    ## Converts read image to characteristics and stores it in charbuffer 1
		    f.convertImage(0x01)

		    ## Searchs template
		    result = f.searchTemplate()

		    positionNumber = result[0]
		    accuracyScore = result[1]

		    if ( positionNumber == -1 ):
		        print('No match found!')
		        self.printLCD('No match found!')
		        self.startx()
		    else:
		        print('Found template at position #' + str(positionNumber))
		        print('The accuracy score is: ' + str(accuracyScore))

		    ## OPTIONAL stuff
		    ##

		    ## Loads the found template to charbuffer 1
		    f.loadTemplate(positionNumber, 0x01)

		    ## Downloads the characteristics of template loaded in charbuffer 1
		    characterics = str(f.downloadCharacteristics(0x01)).encode('utf-8')

		    ## Hashes characteristics of template
		    sha = hashlib.sha256(characterics).hexdigest();

		    print('SHA-2 hash of template: ' + hashlib.sha256(characterics).hexdigest())

		except Exception as e:
		    print('Operation failed!')
		    print('Exception message: ' + str(e))
		    exit(1)

		return sha;

	def take_attendance(self):
		sha = ""

		self.printLCD("Put Faculty \n Finger Print")

		# name = raw_input("Attendance for which course number ? : ")

		sha = self.get_finger_sha();

		courses = self.getCourses(sha);

		print(courses)

		selected = self.makeMenu(courses)
		self.take_for_course( courses[ selected ][0],sha)


		

	def endprogram(self):
         GPIO.cleanup()



if __name__ == "__main__":


	fa = Figpi()
	fa.setup()
	          
	try:
	    fa.startx()

	except KeyboardInterrupt:
	     print('keyboard interrupt detected')
	     fa.endprogram()

	



	# fa.enroll_student()
	# fa.printLCD("Communication\nBitch !")
	# fa.push_attendance();
	


# 29,31,36





