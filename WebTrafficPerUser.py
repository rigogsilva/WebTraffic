#! /usr/bin/env python3
import csv
import sqlite3
from datetime import datetime
import pandas as pd 
import string
from os import path
import os
from tkinter import *

#----------------------------------------------------------------------
### Create WebTrafficPerUser.py file function
#----------------------------------------------------------------------
def createFile():
    
    #Screen for information log. 
    root = Tk()
    root.title('Web Traffic per User')
    
    def openExcel():
        os.system("open -a 'Microsoft Excel.app' '%s'" % 'WebTrafficPerUser.csv')

    variable = StringVar()
    variableString = ''

    topFrame = Frame(root)
    topFrame.pack()
    bottonFrame = Frame(root)
    bottonFrame.pack(side=BOTTOM)
    label1 = Label(text='Processing Infomarmation Log:', fg='#FF6400')
    label1.pack()
    label2=Label(bottonFrame,width=80, height=10, textvariable=variable)
    label2.pack(side=BOTTOM)

    #Set screen to the middle of the screen. 
    h = 200
    w = 700
    ws = root.winfo_screenmmwidth()
    hs = root.winfo_screenheight()
    x = (ws/2) + (w/4)
    y = (hs/2) - (h/2)
    root.geometry('%dx%d+%d+%d' % (w,h,x,y))
    root.update()

    #----------------------------------------------------------------------
    ### Download all files (a.csv, ... , z.csv) to the all.csv locally. 
    #----------------------------------------------------------------------

    # Measure time spent processind data
    startTime = datetime.now()

    #Set alphabet list from a through z and create the file names based on these values
    alphabet = list(string.ascii_lowercase)
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
    frames = []
    for fileName in fileNames:
        urlFile = url + fileName
        data = pd.DataFrame(pd.read_csv(urlFile))
        #Display into in screen. 
        variable.set('Copying ' + str(len(data)) + ' rows from file ' + urlFile)
        root.update()
        allFilesRow = allFilesRow + len(data)
        frames.append(data)
        result = pd.concat(frames)
        
        with open('all.csv', 'a+') as f:
            data.to_csv(f, index=False, encoding='utf-8')

    print('Rows for all the files: ' + str(allFilesRow))

    #----------------------------------------------------------------------
    ### Create a DB and add values from all.csv file to tWebTraffic table.  
    ### This will be used for data validation at the bottom of the program.
    #----------------------------------------------------------------------

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

    #----------------------------------------------------------------------
    ### Sum the time for the user in each path. 
    ### Create a data frame with the same values but horizontally. 
    ### Add results to WebTrafficPerUser.csv file
    #----------------------------------------------------------------------

    #Sum the length time per user and path and add to a data new data frame.
    groupBy = result.groupby(['user_id', 'path']).sum()

    #Add back index since the group by takes the index out. 
    groupByIndex = groupBy.add_suffix('_sum').reset_index()

    #Set transfor groupByIndex into a pivot data frame. This returns values horizontally. 
    newf = groupByIndex.pivot(index='user_id', columns='path', values='length_sum').fillna(0)
    with open('WebTrafficPerUser.csv', 'w+') as f:
        newf.to_csv(f, index=True, encoding='utf-8') 
    
    #----------------------------------------------------------------------
    ### Validate data using sql and the panda dataframe 
    #----------------------------------------------------------------------

    #Validate unique users
    uniqueUsers = con.execute("SELECT count(distinct user_id) FROM tWebTraffic WHERE user_id <> 'user_id'")
        
    #Print unique users from source file: 
    uniqueIDS = result['user_id'].unique()
    uniqueIDS = len(uniqueIDS)
    
    #Set variableString 
    variableString = 'Unique users from all the files: ' + str(uniqueIDS) + '\n'
    print('Unique users from source file: ' + str(uniqueIDS))

    #Print unique users from database: 
    uniqueUsersDB = 0
    for i in uniqueUsers:
        uniqueUsersDB = i[0]
        print('Unique users from database: ' + str(uniqueUsersDB))

    if uniqueUsersDB != uniqueIDS:
        print('Unique users don''t match')
    else: 
        print('Unique users match.')

    #End measure time
    endTime = datetime.now()
    variableString = variableString + 'Time spent processing the data: ' + str(endTime - startTime) + '\n'
    print('Time spent processing the data: ' + str(endTime - startTime))

    #Add open buttons
    variable.set(variableString)
    button1 = Button(bottonFrame, text='Open File in Excel', fg='#373431')
    button1.pack()
    button1.config(command=openExcel)
    label1.destroy()
    root.update()

    root.mainloop()

def main():    
    #----------------------------------------------------------------------
    ### Prompt for web traffic data path function
    #----------------------------------------------------------------------
    def pathPrompt():
        root = Tk()
        root.title('Web Traffic per User')

        def setPath():
            #Get value from Entry and save to path.txt
            url = theTextBox1.get()
            f = open('path.txt', 'w')
            if f.mode == 'w':
                f.write(url)
            f.close()
            #Exit root and continue. 
            root.destroy()
            createFile()

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

        theLabel2 = Label(bottonFrame, fg='red')
        theLabel2.pack()

        theButton1 = Button(bottonFrame, text='Submit', fg='#373431')
        theButton1.pack()
        theButton1.config(command=setPath)
        url = ''

        #Set the appliction to the middle of the screen. 
        h = 150
        w = 700
        ws = root.winfo_screenmmwidth()
        hs = root.winfo_screenheight()
        x = (ws/2) + (w/4)
        y = (hs/2) - (h/2)
        root.geometry('%dx%d+%d+%d' % (w,h,x,y))

        root.mainloop()
        
    pathPrompt()

if __name__ == "__main__":
    main()