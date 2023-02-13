import sqlite3
import os

dbname = 'meds.db'
if os.path.exists(dbname):
    os.remove(dbname)

conn = sqlite3.connect(dbname)
cur = conn.cursor()

sql = 'CREATE TABLE time(id INTEGER PRIMARY KEY AUTOINCREMENT, time INTEGER, amount INTGER)'
cur.execute(sql)

sql = 'CREATE TABLE record(id INTEGER PRIMARY KEY AUTOINCREMENT, amount INTEGER, time INTEGER)'
cur.execute(sql)

sql = f'insert into record(amount, time) values (1,999)'
cur.execute(sql)

sql = f'insert into time(amount, time) values (800,5)'
cur.execute(sql)
sql = f'insert into time(amount, time) values (1200,5)'
cur.execute(sql)
sql = f'insert into time(amount, time) values (1800,5)'
cur.execute(sql)

conn.commit()

cur.close()
conn.close()