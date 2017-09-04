# Web Traffic Transformation
## Objective:
Write a script/program to transform web traffic data stored in time-record format where each row is a page view into a per-user format where each row is a different user and the columns represent the time spent on each of the pages.
The files with the user data is stored in a url. The url has multiple CSV files that store the same data with the following columns drop (1 if this is the last page the user visited, 0 otherwise), length (time spent in the page in seconds), path (page the user visited), useragent (browser type), userid (user ID).
The output file should be a CSV file with one row per user: User (user_id), length of time (sec), Path.

## Criteria:
1. The url where the files are can be changed by the user.
2. The output file should be a CSV file that can be opened using Excel.
3. The program should be stored in a public GitHub account with documentation on how to install and run it.

## Dependencies: 
1. Python 3.6
2. sqlite3 - It should come with python3
3. Install Certificates.command: 
        Go to Applications/Python 3.6 and double-click Install Certificates.command
4. Pandas - pip3 install pandas

## Installation:
1. Install dependencies above.
2. Download or clone the program. 
3. Open a terminal, navidate to the program root folder
4. Run the following command on terminal: python3 WebTrafficPerUser.py
    
## Design:    
![Design](https://github.com/rigogsilva/WebTraffic/blob/master/Design/Wireframe.jpeg)

