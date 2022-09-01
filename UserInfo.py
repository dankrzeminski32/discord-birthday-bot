import csv
from datetime import datetime
from datetime import date


class UserAgeInfo():

    def __init__(self, filename):
        self.csvFile = "DiscordBirthdays.csv"
    
    def getUserAge(self):
        today = date.today()
        today = today.strftime("%m/%d/%y")

        age = today.year - birthdate.year - ((today.month, today.day) < (birthdate.month, birthdate.day))

        with open(self.csvFile) as f:
            reader = csv.reader(f)
            next(reader, None)
            for row in reader:
                if row[1] == today and self.isDateValid(str(row[1]), "%m/%d/%y"):
                    return row
        
    
    def isDateValid(self, date, pattern="%m/%d/%y"):
        try:
            datetime.strptime(date[:5], pattern)
            return True
        except ValueError:
            return False

test = UserAgeInfo("DiscordBirthdays.csv")
test.getUserAge()