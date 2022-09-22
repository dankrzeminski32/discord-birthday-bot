import csv
import discord
import random
from discord.ext import commands
from datetime import datetime
from datetime import date
from db_settings import session_scope
from sqlalchemy import extract
from BirthdayBot.models import BirthdayImages
from BirthdayBot.models import BirthdayMessages


with session_scope() as session:
    birthdayMessage = random.choice(session.query(BirthdayMessages).all())
    birthdayMessage = birthdayMessage.bdayMessage
    author = random.choice(session.query(BirthdayMessages).all())
    author = author.author
    birthdayImage = random.choice(session.query(BirthdayImages).all())
    birthdayImage = birthdayImage.bdayImage
    print(birthdayMessage)
    print(author)
    print(birthdayImage)
