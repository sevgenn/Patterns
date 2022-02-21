import sqlite3

connection = sqlite3.connect('patterns.db')
cursor = connection.cursor()
with open('create_db.sql') as data:
    script = data.read()
cursor.executescript(script)
cursor.close()
