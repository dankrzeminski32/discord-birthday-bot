import csv
import discord
import pandas as pd
from datetime import datetime
from datetime import date

class bdayConfig:
    data = pd.read_csv("DiscordBirthdays.csv")

    def bdayFinder():
        rows = []
        count=0  
        with open("DiscordBirthdays.csv", 'r') as file:
            csvreader = csv.reader(file)
            header = next(csvreader)
            for row in csvreader:
                rows.append(row)


    def isDateValid(date, pattern = "%m/%d/%y"):
        try:
            datetime.strptime(date, pattern)
            return True
        except ValueError:
            return False

    data.columns = ["Name", "Birthday"]
    rawlist = list(data.Birthday)
    print(rawlist)
    for i in rawlist:
        if isDateValid(i,"%m/%d/%y"):
            print(i)
        else:
            print("This date is invalid")


    today = date.today()
    today = today.strftime("%m/%d")
    print("Today's date:", today)
    bdayFinder()
    