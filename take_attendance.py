import hashlib
import time
import sqlite3 as sq;
from pyfingerprint.pyfingerprint import PyFingerprint
from datetime import datetime

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

c.execute("SELECT s.id,s.name FROM student as s WHERE sha=?", (sha,))
 
rows = c.fetchall()

print("Attendance given by ",rows[0][1])

studentid = rows[0][0]

c.execute("SELECT c.id FROM class as c WHERE c.cno = ?", (name,))

rows = c.fetchall()

courseid = rows[0][0]

c.execute(''' insert into attendance3(studentid,courseid,day,month,year,syncstatus) values(?,?,?,?,?,0)''', (studentid,courseid,day,month,year) )

conn.commit();

conn.close();

