import sqlite3 as sq;

cno = raw_input("Enter course number : ");
name = raw_input("Enter class name : ");
faculty = raw_input("Enter faculty id : ");
classcount = raw_input("Enter number of classes in a semester : ");

conn = sq.connect("attendance.db");
c  = conn.cursor();

c.execute(''' insert into class(cno,classcount,name,facultyid) values(?,?,?,?)''', (cno,classcount,name,faculty) )

conn.commit();
conn.close();


