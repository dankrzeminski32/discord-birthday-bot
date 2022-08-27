import csv
import discord
import pandas as pd
from datetime import datetime

class bdayConfig:

    def bdayFinder():
        rows = []
        count=0

        with open("DiscordBirthdays.csv", 'r') as file:
            csvreader = csv.reader(file)
            header = next(csvreader)
            for row in csvreader:
                rows.append(row)

        for i in range(len(rows)):
                for j in range(len(rows[i])):
                        print(rows[i][j])
                        
        #Change so it checks for todays date instead of specified date
        for row in csvreader:
            if row[0] !="Birthday":    #might need to change "birthday" to "name"           
                date = datetime.datetime.strptime (row [0],"%d/%m/%y")     
                if date < datetime.datetime.strptime ("2014-09-26 00:00:00", "%d/%m/%y")and date > datetime.datetime.strptime ("2014-09-25 00:00:00", "%d/%m/%y"):
                    count = count+1

    def isDateValid(date, pattern = "%d/%m/%y"):
        try:
            datetime.strptime(date, pattern)
            return True
        except ValueError:
            return False

    bdayFinder()
    