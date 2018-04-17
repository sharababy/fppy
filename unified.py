#!/usr/bin/env python

import hashlib
import time
import Adafruit_CharLCD as LCD
import sqlite3 as sq;
from pyfingerprint.pyfingerprint import PyFingerprint
from datetime import datetime

class Figpi:

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
		


	def enroll_student(self):
		sha = ""

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
		        exit(0)
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


		name = raw_input("Please enter your name?")
		roll = raw_input("Please enter your roll number?")

		conn = sq.connect("attendance.db");
		c  = conn.cursor();

		c.execute(''' insert into student(sha,name,roll) values(?,?,?)''', (sha,name,roll) )

		conn.commit();
		conn.close();

	def take_attendance(self):
		sha = ""

		name = raw_input("Attendance for which course number ? : ")

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
		        exit(0)
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




		today = datetime.today()

		day = today.day
		month = today.month
		year = today.year;


		conn = sq.connect("attendance.db");

		c  = conn.cursor();

		c.execute("SELECT s.id,s.name,s.roll FROM student as s WHERE sha=?", (sha,))
		 
		rows = c.fetchall()

		print("Attendance given by ",rows[0][1])

		self.printLCD(rows[0][1]+"\n"+rows[0][2])

		studentid = rows[0][0]

		c.execute("SELECT c.id FROM class as c WHERE c.cno = ?", (name,))

		rows = c.fetchall()

		courseid = rows[0][0]

		c.execute(''' insert into attendance3(studentid,courseid,day,month,year,syncstatus) values(?,?,?,?,?,0)''', (studentid,courseid,day,month,year) )

		conn.commit();

		conn.close();




if __name__ == "__main__":

	fa = Figpi()

	# fa.enroll_student()
	fa.printLCD("Ready !")
	fa.take_attendance();
	


# 5,6,16





