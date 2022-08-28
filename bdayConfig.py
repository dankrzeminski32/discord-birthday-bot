import csv
import discord
import pandas as pd
from datetime import datetime
from datetime import date

class BdayConfig:
    """Has methods that returns certain data pretaining the .csv data file. Thus, having access to names and birthdays."""

    def __init__(self):
        self.csvfileName = "DiscordBirthdays.csv"

        self.data = pd.read_csv(self.csvfileName)
        self.data.columns = ["DiscordName", "Birthday"]
        self.dateList = list(self.data.Birthday)
        self.nameList = list(self.data.DiscordName)


    def isDateValid(self, date, pattern = "%m/%d"):
        try:
            datetime.strptime(date[:-3], pattern)#[:-3] Takes off the last 3 characters of the date
            return True
        except ValueError as e:
            print(e)
            return False

    def getBirthdays(self):
        todaysBirthdays = []

        today = date.today()
        today = today.strftime("%m/%d/%y")
        
        print(self.dateList)
        print(self.nameList)

        for i in self.dateList:
            if i == today and self.isDateValid(str(i), "%m/%d"):
                todaysBirthdays += [i]
                birthday = True
            else:
                birthday = False

        print(birthday)
        print(todaysBirthdays)
        return todaysBirthdays

    def getDiscordNames(self):
        todaysBirthdays = []
        birthdayDiscordNames = []

        count = 0

        today = date.today()
        today = today.strftime("%m/%d/%y")
        #print("Today's date:", today)
        data = pd.read_csv("DiscordBirthdays.csv")

        data.columns = ["DiscordName", "Birthday"]
        dateList = list(data.Birthday)
        nameList = list(data.DiscordName)

        for row in data:
            print(row)

        for i in dateList:
            if i == today:
                todaysBirthdays += [i]
                birthdayDiscordNames += [i]
                birthday = True
            else:
                
                birthday = False

        print(birthdayDiscordNames)
    
    def testFunction(self):
        today = date.today()
        today = today.strftime("%m/%d/%y")

        with open(self.csvfileName) as f:
            reader = csv.reader(f)
            next(reader, None)
            for row in reader:
                if row[1] == today and self.isDateValid(str(row[1]), "%m/%d"):
                    print(row)
        



bdayConfigObject = BdayConfig()



#bdayConfigObject.getBirthdays()
#bdayConfigObject.getDiscordNames()
bdayConfigObject.testFunction()
    