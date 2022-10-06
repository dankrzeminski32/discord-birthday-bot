from asyncio.windows_events import NULL
import csv
import requests
from email import message
from types import NoneType
import discord
import random
from discord.ext import commands
from datetime import datetime
from datetime import date
from BirthdayBot.Utils import session_scope, logger
from sqlalchemy import extract
from BirthdayBot.Models import DiscordUser
from BirthdayBot.Models import BirthdayImages
from BirthdayBot.Models import BirthdayMessages
from BirthdayBot.Birthday import Birthday


class BirthdayChecker(object):
    """Handles the checking of birthdays for the day"""

    def __init__(self, bot):
        self.bot = bot

    async def sendBirthdayMessages(self, todays_birthdays: list, channel) -> None:
        for birthday in todays_birthdays:
            random_msg_details = self.generateRandomMessage()
            embed = discord.Embed(
                title="Happy Birthday!",
                description=f"<@{birthday.discord_id}>",
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

            testImage = BirthdayChecker.validateImage(birthdayImage)
            if testImage == False:
                while testImage == False:
                    session.query(BirthdayImages).filter(
                        BirthdayImages.bdayImage == birthdayImage.bdayImage
                    ).delete()
                    session.commit()
                    birthdayImage = random.choice(session.query(BirthdayImages).all())
                    testImage = BirthdayChecker.validateImage(birthdayImage)

            bdayMessage = {
                "message": birthdayMessage.bdayMessage,
                "author": birthdayMessage.author,
                "birthdayImage": birthdayImage.bdayImage,
                "message_id": birthdayMessage.id,
                "birthdayImage_id": birthdayImage.id,
            }

            return bdayMessage

    def validateImage(image: str):
        """Check if resource exist?"""
        if not image:
            raise ValueError("url is required")
        try:
            resp = requests.head(image.bdayImage)
            return True
        except Exception as e:
            return False

    @classmethod
    def getAllBirthdays(cls, guild) -> list:
        with session_scope() as session:
            all_birthdays = (
                session.query(DiscordUser)
                .filter(
                    extract("month", DiscordUser._birthday) == datetime.today().month,
                    extract("day", DiscordUser._birthday) == datetime.today().day,
                    DiscordUser.guild == guild.id,
                )
                .all()
            )
            session.expunge_all()
        return all_birthdays


class BirthdayCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.hybrid_command(
        name="today", description="Displays everyoen with birthdays for the day."
    )
    async def today(self, ctx):
        guildId = ctx.message.guild
        todayBdays = DiscordUser.getAll(guild=guildId)
        month = datetime.today().month
        day = datetime.today().day
        numBdays = 1
        embed = discord.Embed(
            title=f"Todays Birthday's - {month}/{day}",
            description="List of people with birthdays today:",
            color=discord.Color.red(),
        )
        await ctx.send(embed=embed)
        for birthdays in todayBdays:
            userAge = birthdays.birthday.getAge()
            user = await ctx.guild.query_members(user_ids=[int(birthdays.discord_ID)])
            user = user[0]
            embed2 = discord.Embed(
                title=f"{birthdays.username}",
                description=f"is {userAge} today!",
                color=discord.Color.red(),
            )
            embed2.set_image(url=user.avatar.url)
            embed2.set_footer(text=f"{numBdays}/{len(todayBdays)}")
            numBdays += 1
            await ctx.send(embed=embed2)

    @commands.hybrid_command(
        name="tomorrow", description="Displays users birthdays for tomorrow."
    )
    async def tomorrow(self, ctx):
        await ctx.send("coming soon...")

    @commands.hybrid_command(
        name="thismonth", description="Displays users birthdays for the month."
    )
    async def thismonth(self, ctx):
        await ctx.send("coming soon...")


async def setup(bot):
    await bot.add_cog(BirthdayCommands(bot))
