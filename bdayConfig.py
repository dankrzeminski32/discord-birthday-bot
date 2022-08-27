import csv
import discord
import pandas as pd
from datetime import datetime
from datetime import date

class bdayConfig:

    def isDateValid(date, pattern = "%m/%d/%y"):
        try:
            datetime.strptime(date, pattern)
            return True
        except ValueError:
            return False

    def bdayCheck():
        todaysBirthdays = []
        today = date.today()
        today = today.strftime("%m/%d/%y")
        #print("Today's date:", today)
        data = pd.read_csv("DiscordBirthdays.csv")

        data.columns = ["DiscordName", "Birthday"]
        dateList = list(data.Birthday)
        nameList = list(data.DiscordName)
        print(dateList)
        print(nameList)

        for i in dateList:
            if i == today:
                todaysBirthdays += [i]
                birthday = True
            else:
                birthday = False
            #if isDateValid(i,"%m/%d/%y"):
                #print(i)
            #else:
                #print("This date is invalid")
        print(birthday)
        print(todaysBirthdays)



    bdayCheck()
    