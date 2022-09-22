import csv
import discord
import random
from discord.ext import commands
from datetime import datetime
from datetime import date
from db_settings import session_scope
from sqlalchemy import extract
from BirthdayBot.models import DiscordUser
from BirthdayBot.models import BirthdayImages
from BirthdayBot.models import BirthdayMessages


class BirthdayChecker(object):
    """Handles the checking of birthdays for the day"""

    def __init__(self, bot):
        self.bot = bot

    def getAllBirthdays(self) -> list:
        with session_scope() as session:
            all_birthdays = (
                session.query(DiscordUser)
                .filter(
                    extract("month", DiscordUser.Birthday) == datetime.today().month,
                    extract("day", DiscordUser.Birthday) == datetime.today().day,
                )
                .all()
            )
            session.expunge_all()

        return all_birthdays

    async def sendBirthdayMessages(self, todays_birthdays: list, channel) -> None:
        with session_scope() as session:
            birthdayMessage = random.choice(session.query(BirthdayMessages).all())
            birthdayMessage = birthdayMessage.bdayMessage
            author = random.choice(session.query(BirthdayMessages).all())
            author = author.author
            birthdayImage = random.choice(session.query(BirthdayImages).all())
            birthdayImage = birthdayImage.bdayImage

        for birthday in todays_birthdays:
            embed = discord.Embed(
                title="Happy Birthday!",
                description=f"{birthday.username}",
                color=discord.Color.blue(),
            )
            embed.add_field(
                name="Quote:",
                value=birthdayMessage + "\n🤵" + author,
                inline=False,
            )
            embed.set_image(url=birthdayImage)
            await channel.send(embed=embed)

    def __str__(self):
        return f"BirthdayChecker reading from {self.csvfileName}"
