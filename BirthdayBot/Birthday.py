from datetime import datetime

class Birthday(datetime):
    """Represents all of our users birthdays"""
    date_format: str = "%m/%d/%Y" #mm/dd/yyyy
    def __new__(cls, datestring:str): # Creates the object
        converted_date: datetime =  datetime.strptime(datestring, Birthday.date_format)
        return super().__new__(cls, year=converted_date.year, month=converted_date.month, day=converted_date.day)
    def __init__(self, datestring:str): # Initializes the object
        super().__init__()  
        
    def daysUntil(self) -> int:
        today: datetime.datetime = datetime.now()
        date1: datetime.datetime = datetime(today.year, int(self.month), int(self.day))
        date2: datetime.datetime = datetime(today.year + 1, int(self.month), int(self.day))
        days: datetime.timedelta = ((date1 if date1 > today else date2) - today).days
        return days
        
    def __repr__(self):
        return "<Birthday(day='{}', month='{}', year='{}')>".format(self.day, self.month,self.year)
    
    def __str__(self):
        return "{} {}, {}".format(self.strftime("%B"),self.day,self.year)
    
    


# my_bday = Birthday("09/27/20")
# print(my_bday.__repr__())
# print(my_bday)