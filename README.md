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
    pip3 install pandas
    python3 -m pip install pandas
    
![Design](https://github.com/rigogsilva/WebTraffic/blob/master/Design/Wireframe.jpeg)

