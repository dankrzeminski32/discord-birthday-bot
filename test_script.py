from datetime import datetime
from db_settings import session_scope
from BirthdayBot.models import DiscordUser
from sqlalchemy import extract

with session_scope() as session:
    my_data = session.query(DiscordUser).filter(
        extract('month', DiscordUser.Birthday) == datetime.today().month,
        extract('day', DiscordUser.Birthday) == datetime.today().day,

    ).all()

    print(my_data[0].username)
    print(datetime.today())