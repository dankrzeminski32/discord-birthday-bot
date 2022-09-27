from sqlalchemy.orm import Session
from contextlib import contextmanager
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from config import DATABASE_URI
from BirthdayBot.Models import Base
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


def recreateDB():
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)
    # print(Base.metadata.__dict__)


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
