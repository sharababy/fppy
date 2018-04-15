from urllib.parse import urlencode
from urllib.request import Request, urlopen
import sqlite3 as sq;


conn = sq.connect("attendance.db");

c  = conn.cursor();

c.execute("SELECT * FROM attendance3 where syncstatus = 0")
 
rows = c.fetchall()

print(rows)

conn.close();
