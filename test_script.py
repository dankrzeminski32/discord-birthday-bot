from datetime import datetime, date
from db_settings import session_scope
from BirthdayBot.models import DiscordUser
from sqlalchemy import extract

with session_scope() as session:
    my_data = session.query(DiscordUser).filter(
        extract('month', DiscordUser.Birthday) == datetime.today().month,
        extract('day', DiscordUser.Birthday) == datetime.today().day,

    ).all()

    month = my_data[1].Birthday.month
    year = my_data[1].Birthday.year
    day = my_data[1].Birthday.day
    today = date.today()

    age = today.year - year - ((today.month, today.day) < (month, day))

    print(age)
