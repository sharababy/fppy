import sqlite3 as sq;

conn = sq.connect("attendance.db");

c  = conn.cursor();

c.execute('''CREATE TABLE student  ( 
                                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                                        sha TEXT NOT NULL UNIQUE, 
                                        name TEXT NOT NULL, 
                                        roll TEXT NOT NULL
                                    )''')

c.execute('''CREATE TABLE class     ( 
                                        id INTEGER PRIMARY KEY AUTOINCREMENT,  
                                        cno TEXT NOT NULL,
                                        classcount INTEGER NOT NULL,
                                        name TEXT NOT NULL, 
                                        facultyid TEXT NOT NULL
                                    )''')


c.execute('''CREATE TABLE faculty   ( 
                                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                                        name TEXT NOT NULL, 
                                        sha TEXT NOT NULL UNIQUE 
                                    )''')

c.execute('''CREATE TABLE attendance3  ( 
                                        studentid INTEGER NOT NULL, 
                                        courseid INTEGER NOT NULL, 
                                        day INTEGER NOT NULL,
                                        month INTEGER NOT NULL,
                                        year INTEGER NOT NULL,
                                        syncstatus INTEGER NOT NULL
                                    )''')


conn.commit();

conn.close();


