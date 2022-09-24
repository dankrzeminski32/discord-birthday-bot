import csv
import discord
from csv import reader
from datetime import datetime
from datetime import date
from discord.ext import commands
from discord.utils import get
from BirthdayBot.Utils import session_scope
from BirthdayBot.Models import DiscordUser

# Create permission intents, state what our bot should be able to do
intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix=".", intents=intents)


class UserAgeInfo(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    """ ---- COMMANDS ---- """

    @commands.command()
    async def age(self, ctx, arg):
        def check(arg):
            return arg.author == ctx.author and arg.channel == ctx.channel

        arg = arg[2 : len(arg)]
        arg = arg[:-1]  # This is DiscordUser.discordID

        # Query db for requested user
        try:
            with session_scope() as session:
                requested_user = (
                    session.query(DiscordUser)
                    .filter(DiscordUser.discord_ID == arg)
                    .first()
                )
                birthdate = requested_user.Birthday
                argName = requested_user.username[:-5]
            userAge = self.getUserAge(birthdate)
            numDays = self.daysAway(birthdate)
            await ctx.send(
                "```css\n"
                + argName
                + " is currently "
                + str(userAge)
                + " years old. Days until birthday: "
                + str(numDays)
                + "```"
            )
        except:
            await ctx.send("Sorry, that user's information is not available.")

    """ ---- HELPERS ---- """

    def getUserAge(self, Birthday):

        month = Birthday.month
        year = Birthday.year
        day = Birthday.day
        today = date.today()

        age = today.year - year - ((today.month, today.day) < (month, day))
        return age

    def daysAway(self, birthdate):

        today = datetime.now()
        date1 = datetime(today.year, int(birthdate.month), int(birthdate.day))
        date2 = datetime(today.year + 1, int(birthdate.month), int(birthdate.day))
        days = ((date1 if date1 > today else date2) - today).days
        return days


async def setup(bot):
    await bot.add_cog(UserAgeInfo(bot))
