from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Date

Base = declarative_base()

class DiscordUser(Base):
    __tablename__ = 'DiscordUsers'
    id = Column(Integer, primary_key=True)
    username = Column(String)
    Birthday = Column(Date)
    UserId = Column(String)
    
    def __repr__(self):
        return "<DiscordUser(id='{}', username='{}', birthday={})>"\
                .format(self.id, self.username, self.Birthday)

class BirthdayMessages(Base):
    __tablename__ = 'RandomMessages'
    id = Column(Integer, primary_key=True)
    bdayMessage = Column(String)


    def __repr__(self):
        return "<BirthdayMessages(id='{}', bdayMessage{})>"\
                .format(self.id, self.bdayMessage)