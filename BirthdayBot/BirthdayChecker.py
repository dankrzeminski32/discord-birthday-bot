import csv
import discord
from discord.ext import commands
from datetime import datetime
from datetime import date
from db_settings import session_scope
from sqlalchemy import extract
from BirthdayBot.models import DiscordUser


class BirthdayChecker(object):
    """Handles the checking of birthdays for the day"""
    def __init__(self,bot):
        self.bot = bot
    
    def getAllBirthdays(self) -> list:
        with session_scope() as session:
            all_birthdays = session.query(DiscordUser).filter(
                extract('month', DiscordUser.Birthday) == datetime.today().month,
                extract('day', DiscordUser.Birthday) == datetime.today().day,

            ).all()
            session.expunge_all()

        return all_birthdays

    async def sendBirthdayMessages(self, todays_birthdays: list, channel) -> None:
        for birthday in todays_birthdays:
            embed = discord.Embed(
            title = f'Happy Birthday! {birthday.username}',
            description = "Hope this works...",
            color = discord.Color.blue()
            )
            await channel.send(embed=embed)
        
    def __str__(self):
        return f'BirthdayChecker reading from {self.csvfileName}'