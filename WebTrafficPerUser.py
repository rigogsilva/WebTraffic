#! /usr/bin/env python3
import csv
import sqlite3

#----------------------------------------------------------------------
### Download all files (a.csv, ... , z.csv) to the all.csv locally. 
### Do this using AWS S3 bucket. 
#----------------------------------------------------------------------

#----------------------------------------------------------------------
### Create a database and add values from all.csv file.  
### Use the database to group the data based on employee and path
#----------------------------------------------------------------------

#Start database connect and store it in memory
con = sqlite3.connect(':memory:')

#Create tWebTraffic table
con.execute("CREATE TABLE tWebTraffic ('drop', length, path, user_agent, user_id);")

#Add data from all.csv file into tWebTraffic table
with open('all.csv', 'rU') as file:
    reader = csv.DictReader(file)
    rowList = []
    for row in reader:
        rowList = [(row['drop'],row['length'],row['path'],row['user_agent'],row['user_id'])]
        con.executemany('INSERT INTO tWebTraffic VALUES (?,?,?,?,?)', rowList)

#----------------------------------------------------------------------
### Get data from tWebTraffic and add it to WebTrafficPerUser.csv file
#----------------------------------------------------------------------
cursor = con.execute("SELECT user_id, path, sum(length) from tWebTraffic GROUP BY user_id, path ORDER BY user_id, sum(length) DESC")
rows = cursor.fetchall();
wtpu = csv.writer(open("WebTrafficPerUser.csv", "w+"))

#Add header
header = [('User ID', 'Path', 'Length (sec)')]
wtpu.writerows(header)

#Add rows
wtpu.writerows(rows)

#----------------------------------------------------------------------
### Get data from tWebTraffic and add it to DistinctBrosers.csv file
#----------------------------------------------------------------------

#----------------------------------------------------------------------
### Get data from tWebTraffic and add it to PagesUsesLeaveTheMost.csv file
#----------------------------------------------------------------------

#Close database connection
con.commit()
con.close()
