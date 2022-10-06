from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Date, BigInteger, Boolean
from sqlalchemy.ext.hybrid import hybrid_property
from BirthdayBot.Birthday import Birthday
from BirthdayBot.Utils import session_scope
from sqlalchemy.ext.declarative import declared_attr


class Base:
    @declared_attr
    def __tablename__(cls):
        return cls.__name__  # .lower()

    @classmethod
    def create(cls, **kw) -> None:
        with session_scope() as session:
            obj = cls(**kw)
            session.add(obj)

    @classmethod
    def get(cls, **kwargs) -> object:
        with session_scope() as session:
            obj = session.query(cls).filter_by(**kwargs).scalar()
            session.expunge_all()
            return obj

    @classmethod
    def getAll(cls, **kwargs) -> list:
        with session_scope() as session:
            obj: list = session.query(cls).filter_by(**kwargs).all()
            session.expunge_all()
            return obj

    id = Column(Integer, primary_key=True)


Base = declarative_base(cls=Base)


class DiscordUser(Base):
    username = Column(String)
    _birthday = Column("birthday", Date)
    discord_id = Column(BigInteger)
    guild = Column(BigInteger)

    def __init__(self, username: str, birthday: Birthday, discord_id: int, guild: int):
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
            self.__setattr__(field, new_value)
            session.add(self)

    @staticmethod
    def does_user_exist(discord_id: int) -> bool:
        user = DiscordUser.get(discord_id=discord_id)
        return False if user is None else True


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
        return "<IssueReports(id='{}', dateCreated={}, issues={}, guild={}, is_resolved = '{}')>".format(
            self.id, self.dateCreated, self.issues, self.guild, self.is_resolved
        )


class CelebrityBirthdays(Base):
    __tablename__ = "CelebrityBirthdays"
    id = Column(Integer, primary_key=True)
    celebName = Column(String)
    celebAge = Column(Integer)
    celebJob = Column(String)
    celebBirthdate = Column(Date)
    celebLifeSpan = Column(String)

    def __repr__(self):
        return "<CelebrityBirthdays(id='{}', celebName='{}', celebAge = '{}', celebJob = '{}',celebBirthdate = '{}', lifeSpan = '{}')>".format(
            self.id, self.celebName, self.celebAge, self.celebJob, self.celebLifeSpan
        )


class CommandCounter(Base):
    __tablename__ = "CommandCounter"
    id = Column(Integer, primary_key=True)
    register = Column(Integer)
    age = Column(Integer)
    help = Column(Integer)
    botinfo = Column(Integer)
    serverinfo = Column(Integer)
    ping = Column(Integer)
    invite = Column(Integer)
    server = Column(Integer)
    report = Column(Integer)
    today = Column(Integer)
    todayceleb = Column(Integer)
    tomorrow = Column(Integer)
    tomorrowceleb = Column(Integer)
    month = Column(Integer)
    monthceleb = Column(Integer)

    def __repr__(self):
        return "<CommandCounter(id='{}', register='{}', age = '{}', help = '{}', botinfo = '{}', serverinfo = '{}', ping = '{}', invite = '{}', server = '{}', report = '{}', today = '{}', todayceleb = '{}', tomorrow = '{}', tomorrowceleb = '{}', month = '{}', monthceleb = '{}')>".format(
            self.id,
            self.register,
            self.age,
            self.help,
            self.botinfo,
            self.serverinfo,
            self.ping,
            self.invite,
            self.server,
            self.report,
            self.today,
            self.todayceleb,
            self.tomorrow,
            self.tomorrowceleb,
            self.month,
            self.monthceleb,
        )
