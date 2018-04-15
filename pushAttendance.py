import sqlite3 as sq;

conn = sq.connect("attendance.db");

c  = conn.cursor();

c.execute("SELECT s.id FROM student as s WHERE sha=?", (sha,))
 
rows = c.fetchall()

# print(rows[0][0])

conn.close();
