import csv
from discord.ext import commands
from datetime import datetime
from datetime import date

class BirthdayChecker(object):
    """Handles the checking of birthdays for the day"""
    def __init__(self, databaseFileName: str):
        self.csvfileName = databaseFileName

    def getFirstBirthday(self) -> list:
        today = date.today()
        today = today.strftime("%m/%d/%y")

        with open(self.csvfileName) as f:
            reader = csv.reader(f)
            next(reader, None)
            for row in reader:
                if row[1] == today and self.isDateValid(str(row[1]), "%m/%d"):
                    return row
        
    
    def isDateValid(self, date: str, pattern="%m/%d") -> bool:
        try:
            datetime.strptime(date[:-3], pattern)#[:-3] Takes off the last 3 characters of the date
            return True
        except ValueError:
            return False
        
    def __str__(self):
        return f'BirthdayChecker reading from {self.csvfileName}'