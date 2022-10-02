from datetime import datetime



class Birthday(datetime):
    """Represents all of our users birthdays"""
    date_format: str = "%m/%d/%Y" #mm/dd/yyyy
    def __new__(cls, birthday:datetime): # Creates the object
        return super().__new__(cls, year=birthday.year, month=birthday.month, day=birthday.day)
    
    def __init__(self, birthday: datetime): # Initializes the object
        super().__init__()  
        self.is_today: bool = (self.day == datetime.now().day and self.month == datetime.now().month)

        
    @classmethod
    def fromUserInput(cls, datestring: str) -> None:
        converted_date: datetime =  datetime.strptime(datestring, Birthday.date_format)
        return cls(converted_date)

    @staticmethod
    def isValidInput(datestring: str) -> bool:
        try:
            datetime.strptime(datestring, Birthday.date_format)
            return True
        except:
            return False

        
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
    
    


def validateTests():
    from BirthdayBot.Models import DiscordUser
    from BirthdayBot.Utils import session_scope
    my_bday: Birthday = Birthday.fromUserInput("09/30/2020")
    print(my_bday.daysUntil())

    new_user = DiscordUser.create(
        username = "yo",
        birthday = my_bday,
        discord_id=22312312,
        guild=123123
    )

    with session_scope() as session:
        session.add(new_user)
        
    with session_scope() as session:
        test_user:DiscordUser = session.query(DiscordUser).filter_by(username="yo").first()
        session.expunge_all()
        
    print(test_user)
        

    # print(my_bday.__repr__())
    # print(my_bday)