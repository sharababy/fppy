from urllib.parse import urlencode
from urllib.request import Request, urlopen
import sqlite3 as sq;


conn = sq.connect("./attendance.db");
c  = conn.cursor();

c.execute("SELECT * FROM attendance3 where syncstatus = 0")
rows = c.fetchall()

print(rows)

url = 'http://localhost:3000/newAttendanceFile' # Set destination URL here
post_fields = {
				'year': 3,
				'data':rows
				}     # Set POST fields here

request = Request(url, urlencode(post_fields).encode())

json = urlopen(request).read().decode()
# print(json)

c.execute("UPDATE attendance3 set syncstatus = 1 where syncstatus = 0;")

conn.close();
