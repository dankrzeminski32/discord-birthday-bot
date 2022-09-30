from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Date, BigInteger, Boolean
from sqlalchemy.ext.hybrid import hybrid_property
from BirthdayBot.Birthday import Birthday
from BirthdayBot.Utils import session_scope

Base = declarative_base()

class BaseMixIn(Base):
    @classmethod
    def create(cls, **kw):
        with session_scope() as session:      
            obj = cls(**kw)
            session.add(obj)

class DiscordUser(BaseMixIn):
    __tablename__ = "DiscordUser"
    id = Column(Integer, primary_key=True)
    username = Column(String)
    _birthday = Column('birthday',Date)
    discord_id = Column(BigInteger)
    guild = Column(BigInteger)

    def _init__(self,username: str,birthday: Birthday, discord_id: int,guild: int ):
        self.username = username
        self._birthday = birthday
        self.discord_id = discord_id
        self.guild = guild

    def __repr__(self):
        return "<DiscordUser(id='{}', username='{}', birthday={}, guild={})>".format(
            self.id, self.username, self.birthday, self.guild
        )
            
    @hybrid_property
    def birthday(self) -> Birthday:
        birthday: Birthday = Birthday(self._birthday) 
        return birthday
    
    @birthday.setter
    def birthday(self, birthday:Birthday):
        self._birthday = birthday
        


class BirthdayMessages(BaseMixIn):
    __tablename__ = "RandomMessages"
    id = Column(Integer, primary_key=True)
    bdayMessage = Column(String)
    author = Column(String)

    def __repr__(self):
        return "<BirthdayMessages(id='{}', bdayMessage={}, author={})>".format(
            self.id, self.bdayMessage, self.author
        )


class BirthdayImages(BaseMixIn):
    __tablename__ = "BirthdayImages"
    id = Column(Integer, primary_key=True)
    bdayImage = Column(String)

    def __repr__(self):
        return "<BirthdayImages(id='{}', bdayImage={})>".format(self.id, self.bdayImage)


class IssueReports(BaseMixIn):
    __tablename__ = "IssueReports"
    id = Column(Integer, primary_key=True)
    dateCreated = Column(Date)
    issues = Column(String)
    guild = Column(BigInteger)
    is_resolved = Column(Boolean)

    def __repr__(self):
        return "<BirthdayImages(id='{}', dateCreated={}, issues={}, guild={}, is_resolved{})>".format(
            self.id, self.dateCreated, self.issues, self.guild, self.is_resolved
        )
