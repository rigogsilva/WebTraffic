#! /usr/bin/env python3
import csv
import sqlite3
from datetime import datetime
import pandas as pd 
import string
from os import path
import os
from tkinter import *

def main():
    
    def setPath():
        #Get value from Entry and save to path.txt
        url = theTextBox1.get()
        f = open('path.txt', 'w')
        if f.mode == 'w':
            f.write(url)
        f.close()
        #Exit root and continue. 
        root.destroy()

    #----------------------------------------------------------------------
    ### Allow use to change the path where the files reside.
    #----------------------------------------------------------------------
    root = Tk()
    root.title('Web Traffic per User')

    topFrame = Frame(root)
    topFrame.pack()
    bottonFrame = Frame(root)
    bottonFrame.pack(side=BOTTOM)

    #Get default path and if not exists save to path.txt file. 
    urlPathDefault = ''
    if path.exists('path.txt'):
        f = open('path.txt', 'r')
        if f.mode == 'r':
            urlPathDefault = f.read()
        f.close()
    else: 
        f = open('path.txt', 'w+')
        urlPathDefault = 'https://s3-us-west-2.amazonaws.com/cauldron-workshop/data/'
        f.write(urlPathDefault)
        f.close()

    theTextBox1 = Entry(bottonFrame, width=50)
    theTextBox1.insert(END, urlPathDefault)
    theTextBox1.pack()
    theTextBox1.focus_set()

    theLabel1 = Label(text='Enter the path for the Traffic User Data:', fg='#FF6400')
    theLabel1.pack()

    theButton1 = Button(bottonFrame, text='Submit', fg='#373431')
    theButton1.pack()
    url = ''
    theButton1.config(command=setPath)

    root.mainloop()

    #----------------------------------------------------------------------
    ### Download all files (a.csv, ... , z.csv) to the all.csv locally. 
    ### Do this using AWS S3 bucket. 
    #----------------------------------------------------------------------

    # Measure time spent creating moving data from (a.csv, ... , z.csv) to the all.csv
    startTime = datetime.now()

    #Set alphabet list from a through z and create the file names based on these values
    alphabet = ['a']#list(string.ascii_lowercase)
    fileNames = []
    for eachLetter in alphabet:
        fileNames = fileNames + [(str(eachLetter) + '.csv')]

    #Get default path. It will exist by this point.
    if path.exists('path.txt'):
        f = open('path.txt', 'r')
        if f.mode == 'r':
            url = f.read()
        f.close()

    #Remove all.csv if exists
    if path.exists('all.csv'):
        os.remove('all.csv')
        print('Removed all.csv')

    #Loop through each file name and copy the data to all.csv file. Count the ammount of rowns copied.
    allFilesRow = 0
    for fileName in fileNames:
        urlFile = url + fileName
        data = pd.DataFrame(pd.read_csv(urlFile))
        print('Copying ' + str(len(data)) + ' rows from file ' + urlFile)
        allFilesRow = allFilesRow + len(data)

        with open('all.csv', 'a+') as f:
            data.to_csv(f, index=False, encoding='utf-8')

    print('Rows for all the files: ' + str(allFilesRow))

    #End measure time
    endTime = datetime.now()
    print('Time spent moving data into all.csv from (a.csv, ... , z.csv) files is ' + str(endTime - startTime))

    #----------------------------------------------------------------------
    ### Create a DB and add values from all.csv file to tWebTraffic table.  
    ### Use the database to group the data based on employee and path
    #----------------------------------------------------------------------

    # Measure time spent moving data to from all.csv to sqlite3 table. 
    startTime = datetime.now()

    #Start database connect and store it in memory
    con = sqlite3.connect(':memory:')

    #Create tWebTraffic table
    con.execute("CREATE TABLE tWebTraffic ('drop', length, path, user_agent, user_id INTEGER);")

    rowConter = 0 

    #Add data from all.csv file into tWebTraffic table
    with open('all.csv', 'rU') as file:
        reader = csv.DictReader(file)
        
        #Count rows and restart file to the first row
        rows = list(reader)
        rowConter = len(rows)
        file.seek(0)

        rowList = []
        for row in reader:
            rowList = [(row['drop'],row['length'],row['path'],row['user_agent'],row['user_id'])]
            con.executemany('INSERT INTO tWebTraffic VALUES (?,?,?,?,?)', rowList)

    #End measure time
    endTime = datetime.now()
    print('Time spent moving data into tWebTraffic from all.csv is ' + str(endTime - startTime) + ' for ' +  str(rowConter) + ' rows.')

    #----------------------------------------------------------------------
    ### Get data from tWebTraffic and add it to WebTrafficPerUser.csv file
    #----------------------------------------------------------------------

    # Measure time spent creating WebTrafficPerUser file from sqlite3 table. 
    startTime = datetime.now()

    #Select the date grouped by user and path. And also return the sum of the length per user and path. 
    cursor = con.execute("SELECT user_id, path, sum(length) FROM tWebTraffic WHERE user_id <> 'user_id' GROUP BY user_id, path ORDER BY user_id, SUM(length) DESC")
    rows = cursor.fetchall();

    #Get unique user id
    dupUsers = []
    for uniqueID in rows:
        dupUsers.append(str(uniqueID[0]))

    #Get all unique users
    uniqueIDS = set(dupUsers)

    #Concatenate path and length per user.
    usersWithPath = []
    for eachUser in uniqueIDS:
        pathLenghPerUser = ''
        for eachPath in rows:
            #Append path and lengh if user matches
            if str(eachUser) == str(eachPath[0]):
                pathLenghPerUser = str(pathLenghPerUser) + (' Page: ' + str(eachPath[1]) + '  time spent (sec): ' + str(eachPath[2]) + ' | ')
        usersWithPath.append([eachUser, pathLenghPerUser])
        
    #Write data to WebTrafficPerUser file
    wtpu = csv.writer(open("WebTrafficPerUser2.csv", "w+"))
    #Add header
    header = [('User ID', 'Page in Website and Time Spent (sec)')]
    wtpu.writerows(header)
    #Add all rows from wtpu into WebTrafficPerUser.csv file.
    #wtpu.writerows(rows)
    wtpu.writerows(usersWithPath)

    #End measure time
    endTime = datetime.now()
    print('Time spent moving data into WebTrafficPerUser from tWebTraffic table is ' + str(endTime - startTime))

    #----------------------------------------------------------------------
    ### Validate data
    #----------------------------------------------------------------------

    #Validate unique users
    uniqueUsers = con.execute("SELECT count(distinct user_id) FROM tWebTraffic WHERE user_id <> 'user_id'")

    for i in uniqueUsers:
        print(i)

    #----------------------------------------------------------------------
    ### Extra: Get data from tWebTraffic and add it to DistinctBrosers.csv file
    #----------------------------------------------------------------------

    #----------------------------------------------------------------------
    ### Extra: Get data from tWebTraffic and add it to PagesUsersStayTheLongest.csv file
    #----------------------------------------------------------------------

    #Close database connection
    con.commit()
    con.close()

    root = Tk()
    root.title('Web Traffic per User')

    topFrame = Frame(root)
    topFrame.pack()

    bottonFrame = Frame(root)
    bottonFrame.pack(side=BOTTOM)

    theTextBox1 = Entry(bottonFrame, width=40)
    theTextBox1.pack()
    theTextBox1.focus_set()

    theLabel1 = Label(text='Enter the path for the Traffic User Data:', fg='#FF6400')
    theLabel1.pack()

    theButton1 = Button(bottonFrame, text='Submit', fg='#373431')
    theButton1.pack()
    url = ''
    theButton1.config(command=setPath)

    root.mainloop()


if __name__ == "__main__":
    main()