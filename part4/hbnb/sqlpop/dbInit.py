import sqlite3

conn = sqlite3.connect("test.db")
cursor = conn.cursor()

with open("tablegen.sql") as f:
    cursor.executescript(f.read())

with open("initialize.sql") as f:
    cursor.executescript(f.read())

with open("CRUD.sql") as f:
    cursor.executescript(f.read())

conn.commit()
conn.close()