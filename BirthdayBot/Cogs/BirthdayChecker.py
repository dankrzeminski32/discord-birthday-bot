from types import NoneType
import discord
import random
from discord.ext import commands
from datetime import datetime, timedelta
from datetime import date
from BirthdayBot.Utils import session_scope, logger
from BirthdayBot.Models import CelebrityBirthdays, CommandCounter, DiscordUser
from BirthdayBot.Models import BirthdayImages
from BirthdayBot.Models import BirthdayMessages
from BirthdayBot.Birthday import Birthday
from BirthdayBot.Models import CelebrityBirthdays
from sqlalchemy import extract
import requests


class BirthdayChecker(object):
    """Handles the checking of birthdays for the day"""

    def __init__(self, bot):
        self.bot = bot

    @staticmethod
    def getAllBirthdays(
        *,
        guildid: int = None,
        date: datetime = datetime.today(),
        checks_only_month: bool = False,
        celeb: bool = False,
    ) -> list:
        """
        Gets all birthdays on the date specified


        Args:
            guildid (int, optional): guildid of birthdays you wish to search for in
            date (datetime, optional): date you wish to get birthdays matched to. Defaults to datetime.today().
            checks_only_month (bool, optional): If true, disregards the day of your date paramater,returning users with bdays in a given month. Defaults to False.
        Returns:
            list: All birthdays
        """

        with session_scope() as session:
            if celeb is False:
                if guildid is None:
                    if checks_only_month is False:
                        all_birthdays = (
                            session.query(DiscordUser)
                            .filter(
                                extract("month", DiscordUser._birthday) == date.month,
                                extract("day", DiscordUser._birthday) == date.day,
                            )
                            .all()
                        )
                    else:
                        all_birthdays = (
                            session.query(DiscordUser)
                            .filter(
                                extract("month", DiscordUser._birthday) == date.month,
                            )
                            .all()
                        )
                else:
                    if checks_only_month is False:
                        all_birthdays = (
                            session.query(DiscordUser)
                            .filter(
                                extract("month", DiscordUser._birthday) == date.month,
                                extract("day", DiscordUser._birthday) == date.day,
                                DiscordUser.guild == guildid,
                            )
                            .all()
                        )
                    else:
                        all_birthdays = (
                            session.query(DiscordUser)
                            .filter(
                                extract("month", DiscordUser._birthday) == date.month,
                                DiscordUser.guild == guildid,
                            )
                            .all()
                        )
            else:
                if checks_only_month is False:
                    all_birthdays = (
                        session.query(CelebrityBirthdays)
                        .filter(
                            extract("month", CelebrityBirthdays._celebBirthdate)
                            == date.month,
                            extract("day", CelebrityBirthdays._celebBirthdate)
                            == date.day,
                        )
                        .all()
                    )
                else:
                    all_birthdays = (
                        session.query(CelebrityBirthdays)
                        .filter(
                            extract("month", CelebrityBirthdays._celebBirthdate)
                            == date.month,
                        )
                        .all()
                    )
            session.expunge_all()
        return all_birthdays

    async def sendBirthdayMessages(self, todays_birthdays: list, channel) -> None:
        defaultImage = "https://ia803204.us.archive.org/4/items/discordprofilepictures/discordblue.png"
        guild = channel.guild
        for birthday in todays_birthdays:
            user = await guild.query_members(user_ids=[int(birthday.discord_id)])
            user = user[0]
            random_msg_details = self.generateRandomMessage()
            embed = discord.Embed(
                title="🎈🎂Happy Birthday!🎂🎈",
                description=f"🎂 <@{birthday.discord_id}> 🎂",
                color=discord.Color.red(),
            )
            embed.add_field(
                name="Quote:",
                value=random_msg_details["message"]
                + "\n ~ 🤵"
                + random_msg_details["author"],
                inline=False,
            )
            if user.avatar.url == NoneType:
                embed.set_thumbnail(url=defaultImage)
            else:
                embed.set_thumbnail(url=user.avatar.url)
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
            return True  # TODO - Are we logging failures?
        except Exception as e:
            return False


class BirthdayCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.hybrid_command(
        name="today",
        description="Displays everyone with birthdays for the day.",
    )
    async def today(self, ctx):
        todayBdays = BirthdayChecker.getAllBirthdays(guildid=ctx.message.guild.id)
        month = datetime.today().month
        day = datetime.today().day
        numBdays = 1
        embed = discord.Embed(
            title=f"__Todays Birthday's - {month}/{day}__",
            description="List of people with birthdays **today**:",
            color=discord.Color.red(),
        )
        await ctx.send(embed=embed)
        for birthdays in todayBdays:
            defaultImage = "https://ia803204.us.archive.org/4/items/discordprofilepictures/discordblue.png"
            userAge = birthdays.birthday.getAge()
            user = await ctx.guild.query_members(user_ids=[int(birthdays.discord_id)])
            user = user[0]
            embed2 = discord.Embed(
                title=f"{birthdays.username}",
                description=f"is **{userAge}** today! 🎂",
                color=discord.Color.red(),
            )
            if user.avatar.url == NoneType:
                embed2.set_image(url=defaultImage)
            else:
                embed2.set_thumbnail(url=user.avatar.url)
            embed2.set_footer(text=f"{numBdays}/{len(todayBdays)} 🎈")
            numBdays += 1
            await ctx.send(embed=embed2)
        CommandCounter.incrementCommand("today")

    @commands.hybrid_command(
        name="todayceleb",
        description="Displays a random celebrity with a birthday today.",
    )
    async def todayceleb(self, ctx):
        defaultImage = "https://ia803204.us.archive.org/4/items/discordprofilepictures/discordblue.png"
        todayBdays = BirthdayChecker.getAllBirthdays(celeb=True)
        randomBday = random.choice(todayBdays)
        month = datetime.today().month
        day = datetime.today().day
        embed = discord.Embed(
            title=f"__Celebrity Birthday - {month}/{day}__ 🎂🎈",
            description="A random Celebrity with a birthday **today**: ",
            color=discord.Color.red(),
        )
        celebAge = randomBday.celebAge
        celebName = randomBday.celebName
        embed.add_field(
            name=f"__{celebName}__", value=f"Age: **{celebAge}**", inline=True
        )
        if randomBday.celebImgLink == NoneType:
            embed.set_image(url=defaultImage)
        else:
            embed.set_image(url=randomBday.celebImgLink)
        await ctx.send(embed=embed)
        CommandCounter.incrementCommand("todayceleb")

    @commands.hybrid_command(
        name="tomorrow",
        description="Displays users birthdays for tomorrow.",
    )
    async def tomorrow(self, ctx):
        defaultImage = "https://ia803204.us.archive.org/4/items/discordprofilepictures/discordblue.png"
        tomorrowDate = datetime.now() + timedelta(days=1)
        tomorrowBdays = BirthdayChecker.getAllBirthdays(
            guildid=ctx.message.guild.id, date=tomorrowDate
        )
        month = datetime.today().month
        day = datetime.today().day
        numBdays = 1
        embed = discord.Embed(
            title=f"__Tomorrows Birthday's - {month}/{day+1}__",
            description="List of people with birthdays **tomorrow**:",
            color=discord.Color.red(),
        )
        await ctx.send(embed=embed)
        for birthdays in tomorrowBdays:
            userAge = birthdays.birthday.getAge()
            user = await ctx.guild.query_members(user_ids=[int(birthdays.discord_id)])
            user = user[0]
            embed2 = discord.Embed(
                title=f"{birthdays.username}",
                description=f"is **{userAge}** tomorrow!",
                color=discord.Color.red(),
            )
            if user.avatar.url == NoneType:
                embed2.set_image(url=defaultImage)
            else:
                embed2.set_image(url=user.avatar.url)
            embed2.set_footer(text=f"{numBdays}/{len(tomorrowBdays)}")
            numBdays += 1
            await ctx.send(embed=embed2)
        CommandCounter.incrementCommand("tomorrow")

    @commands.hybrid_command(
        name="tomorrowceleb",
        description="Displays a random celebrity with a birthday tomorrow.",
    )
    async def tomorrowceleb(self, ctx):
        defaultImage = "https://ia803204.us.archive.org/4/items/discordprofilepictures/discordblue.png"
        tomorrowDate = datetime.now() + timedelta(days=1)
        tomorrowBdays = BirthdayChecker.getAllBirthdays(date=tomorrowDate, celeb=True)
        randomBday = random.choice(tomorrowBdays)
        month = datetime.today().month
        day = datetime.today().day
        embed = discord.Embed(
            title=f"__Celebrity Birthday That's Tomorrow - {month}/{day+1}__",
            description="A random Celebrity with a birthday **tomorrow**: ",
            color=discord.Color.red(),
        )
        celebAge = randomBday.celebAge
        celebName = randomBday.celebName
        embed.add_field(name=f"{celebName}", value=f"Age: **{celebAge}**", inline=True)
        if randomBday.celebImgLink == NoneType:
            embed.set_image(url=defaultImage)
        else:
            embed.set_image(url=randomBday.celebImgLink)
        await ctx.send(embed=embed)
        CommandCounter.incrementCommand("tomorrowceleb")

    @commands.hybrid_command(
        name="month",
        description="Displays users birthdays for the month.",
    )
    async def month(self, ctx):
        monthBdays = BirthdayChecker.getAllBirthdays(
            guildid=ctx.message.guild.id, checks_only_month=True
        )
        month = datetime.today().month
        month = datetime.strptime(str(month), "%m")
        month = month.strftime("%B")
        embed = discord.Embed(
            title=f"__{month} Birthday's__",
            description="List of people with birthdays this **month**:",
            color=discord.Color.red(),
        )
        for birthdays in monthBdays:
            embed.add_field(
                name=f"{birthdays.username}",
                value=f"Birthday: {birthdays.birthday.month}/{birthdays.birthday.day}",
                inline=False,
            )
        embed.set_footer(text=f"Total amount of birthdays: {len(monthBdays)}")
        await ctx.send(embed=embed)
        CommandCounter.incrementCommand("month")

    @commands.hybrid_command(
        name="monthceleb",
        description="Displays celebrity birthdays for the month.",
    )
    async def monthceleb(self, ctx):
        monthBdays = BirthdayChecker.getAllBirthdays(celeb=True, checks_only_month=True)
        month = datetime.today().month
        month = datetime.strptime(str(month), "%m")
        month = month.strftime("%B")
        embed = discord.Embed(
            title=f"__{month} Celebrity Birthday's__ 🎂🎈",
            description="List of 5 random Celebrity's with birthdays this **month**:",
            color=discord.Color.red(),
        )
        for randomBday in range(1, 6):
            randomBday = random.choice(monthBdays)
            embed.add_field(
                name=f"{randomBday.celebName}",
                value=f"➖ Birthday: {randomBday.celebBirthdate.month}/{randomBday.celebBirthdate.day}",
                inline=False,
            )
        await ctx.send(embed=embed)
        CommandCounter.incrementCommand("monthceleb")

    @commands.hybrid_command(
        name="me",
        description="Displays user infromation along with a random celebrity that shares the same brithday with the user.",
    )
    async def me(self, ctx):
        if DiscordUser.does_user_exist(discord_id=ctx.author.id):
            user = DiscordUser.get(discord_id=ctx.author.id)
            userBday = user.birthday
            celebs_matching_users_bday: list = BirthdayChecker.getAllBirthdays(
                celeb=True, date=user.birthday
            )
            celeb = random.choice(celebs_matching_users_bday)

            embed = discord.Embed(
                title="__--Infromation--__",
                description="Here is infromation regarding you.",
                color=discord.Color.red(),
            )
            embed.add_field(
                name="Birthday:",
                value=f"{userBday}",
                inline=False,
            )
            embed2 = discord.Embed(
                title="You Share A Birthday With",
                description=f"**{celeb.celebName}**",
                color=discord.Color.red(),
            )
            embed2.set_image(url=celeb.celebImgLink)
            embed2.set_footer(text=f"Occupation: {celeb.celebJob}")

            await ctx.send(embed=embed)
            await ctx.send(embed=embed2)
        else:
            await ctx.send(
                "ERROR: You don't have a birthday on file, make sure you use, '.bday reigster' to set one."
            )

        CommandCounter.incrementCommand("me")


async def setup(bot):
    await bot.add_cog(BirthdayCommands(bot))
