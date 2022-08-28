import csv
import discord
import pandas as pd
from datetime import datetime
from datetime import date

class BdayConfig:
    """Has methods that returns certain data pretaining the .csv data file. Thus, having access to names and birthdays."""

    def __init__(self):
        self.csvfileName = "DiscordBirthdays.csv"

    def isDateValid(self, date, pattern = "%m/%d"):
        try:
            datetime.strptime(date[:-3], pattern)#[:-3] Takes off the last 3 characters of the date
            return True
        except ValueError as e:
            print(e)
            return False
    
    def getBirthdays(self):
        today = date.today()
        today = today.strftime("%m/%d/%y")

        with open(self.csvfileName) as f:
            reader = csv.reader(f)
            next(reader, None)
            for row in reader:
                if row[1] == today and self.isDateValid(str(row[1]), "%m/%d"):
                    print(row)
        



bdayConfigObject = BdayConfig()

bdayConfigObject.getBirthdays()
    