from xmlrpc.client import Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Date, BigInteger, Boolean


Base = declarative_base()


class DiscordUser(Base):
    __tablename__ = "DiscordUser"
    id = Column(Integer, primary_key=True)
    username = Column(String)
    Birthday = Column(Date)
    discord_ID = Column(String)
    guild = Column(BigInteger)

    def __repr__(self):
        return "<DiscordUser(id='{}', username='{}', birthday={}, guild={})>".format(
            self.id, self.username, self.Birthday, self.guild
        )


class BirthdayMessages(Base):
    __tablename__ = "RandomMessages"
    id = Column(Integer, primary_key=True)
    bdayMessage = Column(String)
    author = Column(String)

    def __repr__(self):
        return "<BirthdayMessages(id='{}', bdayMessage={}, author={})>".format(
            self.id, self.bdayMessage, self.author
        )


class BirthdayImages(Base):
    __tablename__ = "BirthdayImages"
    id = Column(Integer, primary_key=True)
    bdayImage = Column(String)

    def __repr__(self):
        return "<BirthdayImages(id='{}', bdayImage={})>".format(self.id, self.bdayImage)


class IssueReports(Base):
    __tablename__ = "IssueReports"
    id = Column(Integer, primary_key=True)
    dateCreated = Column(Date)
    issues = Column(String)
    guild = Column(BigInteger)
    is_resolved = Column(Boolean)

    def __repr__(self):
        return "<IssueImages(id='{}', dateCreated={}, issues={}, guild={}, is_resolved = '{}')>".format(
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
        return "<CelebrityBirthdays(id='{}', register='{}', age = '{}', help = '{}', botinfo = '{}', serverinfo = '{}', ping = '{}', invite = '{}', server = '{}', report = '{}', today = '{}', todayceleb = '{}', tomorrow = '{}', tomorrowceleb = '{}', month = '{}', monthceleb = '{}')>".format(
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
