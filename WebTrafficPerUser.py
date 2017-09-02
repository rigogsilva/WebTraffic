#! /usr/bin/env python3
import csv
import sqlite3
import pandas as pd

con = sqlite3.connect(':memory:')
cur = con.cursor()
cur.execute("CREATE TABLE tWebTraffic (col1, col2);")

#with open('data.csv', 'rb') as fin:
 #   dr = csv.DictReader(fin)
  #  to_db = [(i['col1'], i['col2']) for i in dr]

df = pd.read_csv('data.csv')
df.to_sql('tWebTraffic', con, if_exists='append', index=False)    

cur.executemany("INSERT INTO tWebTraffic (col1, col2) VALUES (?, ?);", to_db)
con.commit()
con.close()