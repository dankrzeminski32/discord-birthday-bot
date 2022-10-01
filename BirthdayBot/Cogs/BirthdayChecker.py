import csv
from email import message
import discord
import random
from discord.ext import commands
from datetime import datetime
from datetime import date
from BirthdayBot.Cogs.UserAgeInfo import UserAgeInfo
from BirthdayBot.Utils import session_scope, logger
from sqlalchemy import extract
from BirthdayBot.Models import DiscordUser
from BirthdayBot.Models import BirthdayImages
from BirthdayBot.Models import BirthdayMessages


class BirthdayChecker(object):
    """Handles the checking of birthdays for the day"""

    def __init__(self, bot):
        self.bot = bot

    @classmethod
    def getAllBirthdays(cls, guild) -> list:
        with session_scope() as session:
            all_birthdays = (
                session.query(DiscordUser)
                .filter(
                    extract("month", DiscordUser.Birthday) == datetime.today().month,
                    extract("day", DiscordUser.Birthday) == datetime.today().day,
                    DiscordUser.guild == guild.id,
                )
                .all()
            )
            session.expunge_all()

        return all_birthdays

    async def sendBirthdayMessages(self, todays_birthdays: list, channel) -> None:

        for birthday in todays_birthdays:
            random_msg_details = self.generateRandomMessage()
            embed = discord.Embed(
                title="Happy Birthday!",
                description=f"<@{birthday.discord_ID}>",
                color=discord.Color.red(),
            )
            embed.add_field(
                name="Quote:",
                value=random_msg_details["message"]
                + "\n ~ 🤵"
                + random_msg_details["author"],
                inline=False,
            )
            embed.set_image(url=random_msg_details["birthdayImage"])
            await channel.send(embed=embed)
            logger.info(
                "Sending Birthday Announcement: Username: {} -  Quote ID: {} - Author: {} - Image ID: {}".format(
                    birthday.username,
                    random_msg_details["message_id"],
                    random_msg_details["author"],
                    random_msg_details["birthdayImage_id"],
                )
            )

    def generateRandomMessage(self) -> dict:
        with session_scope() as session:
            birthdayMessage = random.choice(session.query(BirthdayMessages).all())
            birthdayImage = random.choice(session.query(BirthdayImages).all())

            bdayMessage = {
                "message": birthdayMessage.bdayMessage,
                "author": birthdayMessage.author,
                "birthdayImage": birthdayImage.bdayImage,
                "message_id": birthdayMessage.id,
                "birthdayImage_id": birthdayImage.id,
            }

            return bdayMessage


class BirthdayCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.hybrid_command(
        name="today",
        description="Displays everyoen with birthdays for the day.",
    )
    async def today(self, ctx):
        guildId = ctx.message.guild
        todayBdays = BirthdayChecker.getAllBirthdays(guildId)
        month = datetime.today().month
        day = datetime.today().day
        embed = discord.Embed(
            title=f"Todays Birthday's - {month}/{day}",
            description="List of people with birthdays today:",
            color=0x9C84EF,
        )
        for birthdays in todayBdays:
            userAge = UserAgeInfo.getUserAge(birthdays.Birthday)
            embed.add_field(
                name=birthdays.username, value=f"is {userAge} today!", inline=False
            )
        await ctx.send(embed=embed)

    @commands.hybrid_command(
        name="me",
        description="Displays user information.",
    )
    async def me(self, ctx):
        await ctx.send("To do")


async def setup(bot):
    await bot.add_cog(BirthdayCommands(bot))
