import sqlite3

db=sqlite3.connect("database.db")
cur=db.cursor()

cur.execute('''
    CREATE TABLE IF NOT EXISTS users_data (
            Username TEXT(50) primary key ,
            Passwords TEXT(50)

    )



''')
db.commit
db.close