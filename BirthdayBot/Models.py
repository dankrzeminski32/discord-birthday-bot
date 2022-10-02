from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Date, BigInteger, Boolean
from sqlalchemy.ext.hybrid import hybrid_property
from BirthdayBot.Birthday import Birthday
from BirthdayBot.Utils import session_scope
from sqlalchemy.ext.declarative import declared_attr

class Base:
    @declared_attr
    def __tablename__(cls):
        return cls.__name__ #.lower()
    @classmethod
    def create(cls, **kw) -> None:
        with session_scope() as session:      
            obj = cls(**kw)
            session.add(obj)
    @classmethod
    def get(cls, field: str, value: str) -> object:
        kwargs = {field: value}
        with session_scope() as session:      
            obj = session.query(cls).filter_by(**kwargs).scalar()
            session.expunge_all()
            return obj  

    id =  Column(Integer, primary_key=True)


Base = declarative_base(cls=Base)


class DiscordUser(Base):
    username = Column(String)
    _birthday = Column('birthday',Date)
    discord_id = Column(BigInteger)
    guild = Column(BigInteger)

    def __init__(self,username: str,birthday: Birthday, discord_id: int,guild: int ):
        self.username = username
        self._birthday = birthday
        self.discord_id = discord_id
        self.guild = guild

    def __repr__(self):
        return "<DiscordUser(id='{}', username='{}', birthday={}, discord_id={}, guild={})>".format(
            self.id, self.username, self.birthday, self.discord_id, self.guild
        )
            
    @hybrid_property
    def birthday(self) -> Birthday:
        birthday: Birthday = Birthday(self._birthday) 
        return birthday
    
    @birthday.setter
    def birthday(self, birthday: Birthday):
        self._birthday = birthday
        
    def update(self, field, new_value):
        with session_scope() as session:
            self.__setattr__(field,new_value)
            session.add(self)
    
class BirthdayMessages(Base):
    bdayMessage = Column(String)
    author = Column(String)

    def __repr__(self):
        return "<BirthdayMessages(id='{}', bdayMessage={}, author={})>".format(
            self.id, self.bdayMessage, self.author
        )


class BirthdayImages(Base):
    bdayImage = Column(String)

    def __repr__(self):
        return "<BirthdayImages(id='{}', bdayImage={})>".format(self.id, self.bdayImage)


class IssueReports(Base):
    dateCreated = Column(Date)
    issues = Column(String)
    guild = Column(BigInteger)
    is_resolved = Column(Boolean)

    def __repr__(self):
        return "<BirthdayImages(id='{}', dateCreated={}, issues={}, guild={}, is_resolved{})>".format(
            self.id, self.dateCreated, self.issues, self.guild, self.is_resolved
        )
