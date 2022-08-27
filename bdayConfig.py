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
        today = date.today()
        today = today.strftime("%m/%d")
        #print("Today's date:", today)
        data = pd.read_csv("DiscordBirthdays.csv")

        data.columns = ["Name", "Birthday"]
        rawlist = list(data.Birthday)
        print(rawlist)
        for i in rawlist:
            if today == i:
                birthday = True
            else:
                birthday = False
            #if isDateValid(i,"%m/%d/%y"):
                #print(i)
            #else:
                #print("This date is invalid")
        print(birthday)



    bdayCheck()
    