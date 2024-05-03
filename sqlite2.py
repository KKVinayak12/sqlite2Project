#!/usr/bin/env python
# coding: utf-8

# In[ ]:


from sqlite3.dbapi2 import Cursor
import sqlite3
import re

db = sqlite3.connect(":memory:")
Cursor = db.cursor()

Cursor.execute('''
DROP TABLE IF EXISTS Counts''')

Cursor.execute('''
CREATE TABLE Counts (org TEXT, count INTEGER)''')

fname = input('Enter file name: ')
if ( len(fname) < 1 ) : fname = 'mbox.txt'
fh = open(fname)
for line in fh:
    if not line.startswith('From: ') : continue
    all_org = re.findall("@(.+)\s", line)
    org = all_org[0]
    Cursor.execute('SELECT count FROM Counts WHERE org = ? ', (org, ))
    row = Cursor.fetchone()
    if row is None:
        Cursor.execute('''INSERT INTO Counts (org, count) 
                VALUES ( ?, 1 )''', ( org, ) )
    else :
        Cursor.execute('UPDATE Counts SET count=count+1 WHERE org = ?',
            (org, ))
    db.commit()

sqlstr = 'SELECT org, count FROM Counts ORDER BY count DESC LIMIT 10'

for row in Cursor.execute(sqlstr) :
    print (str(row[0]), row[1])

db.close()

