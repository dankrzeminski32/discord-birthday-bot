from asyncio.windows_events import NULL
import csv
from email import message
from types import NoneType
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
from BirthdayBot.Birthday import Birthday


class BirthdayChecker(object):
    """Handles the checking of birthdays for the day"""

    def __init__(self, bot):
        self.bot = bot

    async def sendBirthdayMessages(self, todays_birthdays: list, channel) -> None:
        todays_birthdays = DiscordUser.getAll(_birthday=Birthday(datetime.today()))
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
            userAge = UserAgeInfo.getUserAge(birthdays.Birthday)
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
        name="tomorrow",
        description="Displays users birthdays for tomorrow.",
    )
    async def tomorrow(self, ctx):
        await ctx.send("coming soon...")

    @commands.hybrid_command(
        name="thismonth",
        description="Displays users birthdays for the month.",
    )
    async def thismonth(self, ctx):
        await ctx.send("coming soon...")


async def setup(bot):
    await bot.add_cog(BirthdayCommands(bot))
