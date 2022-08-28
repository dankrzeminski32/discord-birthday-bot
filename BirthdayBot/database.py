import csv
from discord.ext import commands
from datetime import datetime
from datetime import date


class Database(object):
    """Handles operations relating to our csv database"""       
    def __init__(self, filename):
        self.csvFile = open(filename, "w", newline="")
        self.csvWriter = csv.writer(self.csvFile)
        self.createColumnHeaders()

    def createColumnHeaders(self):
        self.csvWriter.writerow(["DiscordName", "Birthday"])

class BirthdayChecker(object):
    """Handles the checking of birthdays for the day"""
    def __init__(self, databaseFileName):
        self.csvfileName = databaseFileName

    def getBirthdays(self):
        today = date.today()
        today = today.strftime("%m/%d/%y")

        with open('../{}'.format(self.csvfileName)) as f:
            reader = csv.reader(f)
            next(reader, None)
            for row in reader:
                if row[1] == today and self.isDateValid(str(row[1]), "%m/%d"):
                    return row
        
    
    def isDateValid(self, date, pattern="%m/%d"):
        try:
            datetime.strptime(date[:-3], pattern)#[:-3] Takes off the last 3 characters of the date
            return True
        except ValueError:
            return False

birthdaychecker = BirthdayChecker("DiscordBirthdays.csv")
print(birthdaychecker.getBirthdays())