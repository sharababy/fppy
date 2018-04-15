import sqlite3 as sq;

conn = sq.connect("attendance.db");

c  = conn.cursor();

c.execute(''' insert into class(,name,roll) values(?,?,?)''', (sha,name,roll) )



conn.commit();

conn.close();


