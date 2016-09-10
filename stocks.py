


'''
This is incomplete (i moved all my trading stuff over to quantopian) but it's sstill a good quick example of calling
the yahoo finance stock api

This is a python script that will read from tickers.txt, and structure
a yahoo csv query to return various tickers.   
** A separate script will run daily to see if we have an buy triggers (or close to buy triggers)

Fields pulled from quote

price
day high
day low

FIelds calculated
Todays date


'''


import MySQLdb
import _mysql

### Create a table for the ticker, insert in one row for today's date after close ###
def insertQuoteRow(ticker, openPrice, dayLow, dayHigh):


    db = _mysql.connect(host="localhost", user="turtleUser",passwd="password",db="turtleDB")

    import time
#works for date #### 
    date = time.strftime('%Y-%m-%d')


    print("date is " + date) 
    createTableQuery = "CREATE TABLE IF NOT EXISTS " + ticker + "( id INT UNSIGNED AUTO_INCREMENT PRIMARY KEY, ticker VARCHAR(5) NOT NULL, date DATE, openPrice DOUBLE NOT NULL, highPrice DOUBLE NOT NULL, lowPrice DOUBLE NOT NULL, 20dayHigh DOUBLE NOT NULL, 20dayLow DOUBLE NOT NULL)"
    db.query(createTableQuery)
    myquery = "INSERT INTO " + ticker + " " + "(ticker,date,openPrice,highPrice, lowPrice) VALUES('" +  ticker + "'," + "'" + date  + "'," + openPrice + ", " + dayHigh + ", " + dayLow + ")"
    print(myquery)

    db.query(myquery)





######################## main method ##########################

# open tickers.txt

import csv
with open('tickers.csv', 'rb') as f:
    reader = csv.reader(f)
    tickersList = list(reader)

for ticker in tickersList:
    print(ticker)
    print('\n')

# for each line in tickers.txt -> append to yahooquote string

query = "http://finance.yahoo.com/d/quotes.csv?s="
for row in tickersList:
    for ticker in row[:-1]:
        query += (ticker + "+")

    query +=  "&f=ogh"   
###  o = open,  g = days low, h = days high

print(query + "\n")


#make query and put in file 'f'    
import urllib2
f = urllib2.urlopen(query)
#print f.read(5000)

print("reading lines now... \n")
lineArray = f.readlines()

inc=0
for line in lineArray:
    line = line.split(",") 
    ticker = str(tickersList[0][inc])
    open = line[0]
    low = line[1]
    high = line[2]
    print("Ticker: " + ticker)
    print("Open Price: " + open)
    print("Day Low: " + low)
    print("Day High: " + high)
    inc+= 1
    insertQuoteRow(ticker, open, low, high)






