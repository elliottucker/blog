Title: Using gspread to populate a Google Spreadsheet from a multi dimensional dictionary
Date: 2013-05-11 14:48
Tags: Python, Google Docs, Beginner

I'm often asked to knock up quick transaction reports and in the past I'd normally automate sending these by email or having them exported to an Excel sheet in a shared directory.  As a company that uses Google Apps it made sense to have these reports created as a Google Spreadsheet instead.  Thanks to the excellent [gspread](https://github.com/burnash/gspread) Python library this is extremely easy.

We'll create a Spreadsheet with multiple worksheets, one for each year in the report.  Worksheets will be made up of rows of months a columns of clients, with cells being a random value.

First off we'll make a two dimensional dictionary data to play with.  You can safely ignore test_data() but it gives a useful example of the kind of data I might see.

``` python
from collections import defaultdict         # only required for 
from random import random                   # test data

import gspread

def test_data():

	months = ['Jan','Feb','Mar','Apr,','May','Jun','Jul']
	clients = ['Client 1','Client 2','Client 3','Client 4']

	data = defaultdict(dict)
	for month in months:
		for client in clients:
            data[month][client] = (int(random()*100),int(random()*100))

	return data

```

These should leave us with a dictionary with months and clients for keys with a list of random numbers but no particular order.

``` python
>>> data['Jan']['Client 1']
(42,34)
```

Create a class to do the grunt work of creating worksheets and updating cells.  The class will take your Google username and password, and the name of a previously created Google Spreadshet.

Define a method suitable for your data - obviously this will be determined by your needs but the below example would be a common simple report.  Here I'm going to have a method that updates a single year's worksheet with the data defined in the above test data.  It will loop through the months, then the clients and create a row with the data "month,client,value 1, value 2"

``` python
class Sheet:
    def __init__(self,username,password,spreadsheet):
        gc = gspread.login(username,password)
        self.spreadsheet = gc.open(spreadsheet)
        self.rowcount = {}


    def update_year(self,year,data):

        rowcount = 2  # Start at 2 to leave room for headers


        # Check for an existing worksheet for the year and create one if not
        # Each sheet is a year
        
        try:
            worksheet= self.spreadsheet.worksheet(year)
        except gspread.WorksheetNotFound:
            self.spreadsheet.add_worksheet(year,100,5)
            worksheet = self.spreadsheet.worksheet(year)

        # Loop through the months in the data dictionary and build
        # a row to add to the worksheet"""

        for month in data.keys():

            for client in data[month].keys():
                
                # a row of data to add to the spreadsheet.
                row = (month,client,data[month][client][0],data[month][client][1])

                cell_list = worksheet.range("A%s:D%s" % (rowcount,rowcount))

                # cell_list now containts a list of cell objects. Use map and a tiny
                # function (setcell) to update the list of cell objects with a row of values.

                map(self.setcell,cell_list,row)
                worksheet.update_cells(cell_list)
                # move on a row in the sheet.
                rowcount += 1

    def setcell(self,c,v):
        c.value = v

```

And then call the class in your script:

``` python

if __name__ == "__main__":

    GOOGLEUSERNAME='you@gmail.com'
    GOOGLEPASSWORD = 'yourpassword'
    GOOGLESHEETNAME = 'Test Sheet'
    
    years = ['2010','2011','2012','2013']
    sheet  = Sheet(GOOGLEUSERNAME,GOOGLEPASSWORD,GOOGLESHEETNAME)
    
    for year in years:
        data = test_data()

        sheet.update_year(year,data)
```




