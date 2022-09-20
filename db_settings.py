from sqlalchemy.orm import Session
from contextlib import contextmanager
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from config import DATABASE_URI
from BirthdayBot.models import Base

engine = create_engine(DATABASE_URI)
Session = sessionmaker(bind=engine)
#Base.metadata.drop_all(engine)
#Base.metadata.create_all(engine)

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