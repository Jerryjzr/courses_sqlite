import sqlite3

conn = sqlite3.connect('course.db')
c = conn.cursor()

c.execute('''CREATE TABLE courses
             (id INTEGER PRIMARY KEY AUTOINCREMENT,
             course_name TEXT NOT NULL,
             teacher TEXT NOT NULL,
             time TEXT NOT NULL,
             location TEXT NOT NULL)''')

conn.commit()
conn.close()