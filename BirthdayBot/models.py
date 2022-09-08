from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Date

Base = declarative_base()

class DiscordUser(Base):
    __tablename__ = 'DiscordUsers'
    id = Column(Integer, primary_key=True)
    username = Column(String)
    Birthday = Column(Date)
    
    def __repr__(self):
        return "<DiscordUser(id='{}', username='{}', birthday={})>"\
                .format(self.id, self.username, self.birthday)
