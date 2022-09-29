from sqlalchemy.orm import Session
from contextlib import contextmanager
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from config import DATABASE_URI
from BirthdayBot.Models import Base, DiscordUser
import logging
from logging import FileHandler

# ----- LOGGING CONFIG -----
logger = logging.getLogger(__name__)
fh = FileHandler("bot.log", mode="w")
logger.setLevel("DEBUG")
formatter = logging.Formatter(
    "%(asctime)s - %(filename)s - %(levelname)-2s - %(message)s",
    datefmt="%Y-%m-%d - %I:%M:%S %p",
)
fh.setFormatter(formatter)
logger.addHandler(fh)
logger.info("Logger has been successfully configured.")
# ----- END LOGGING CONFIG -----

# GLOBAL DATABASE SESSIONAMKER
engine = create_engine(DATABASE_URI)
Session = sessionmaker(bind=engine)


@contextmanager
def session_scope():
    session = Session()
    try:
        yield session
        session.commit()
    except Exception:
        session.rollback()
        raise
    finally:
        session.close()


def recreateDB():
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)
    # print(Base.metadata.__dict__)



def addUserToDB(username: str, birthday: str, discord_id: str, guild: int) -> None:
    # session_scope will raise an exception if invalid, use this with try/except
    with session_scope() as s:
        user = DiscordUser(
            username=str(username),
            Birthday=birthday,
            discord_ID=discord_id,
            guild=guild,
        )
        s.add(user)

