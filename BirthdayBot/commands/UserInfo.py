import csv
import discord
from csv import reader
from datetime import datetime
from datetime import date
from discord.ext import commands
from discord.utils import get
from db_settings import session_scope

# Create permission intents, state what our bot should be able to do
intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix = ".", intents = intents)

class UserAgeInfo(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    """ ---- COMMANDS ---- """
    @commands.command()
    async def age(self, ctx, arg):

        def check(arg):
            return arg.author == ctx.author and arg.channel == ctx.channel
        
        arg = arg[2:len(arg)]
        arg = arg[:-1]

        birthdate = "dan"
        argName = argName[:-5]
        userAge = self.getUserAge(birthdate)
        numDays = self.daysAway(birthdate)
        await ctx.send("```css\n" + argName +" is currently "+ str(userAge)+ " years old. Days until birthday: "+ str(numDays) + "```")
    
    """ ---- HELPERS ---- """
    def getUserAge(self, Birthday):
        
        month = Birthday.month
        year = Birthday.year
        day = Birthday.day
        today = date.today()
        
        age = today.year - year - ((today.month, today.day) < (month, day))
        return age

    def daysAway(self, birthdate):
        if birthdate[0] == "0":
            birthMonth = birthdate[1]
        else:
            birthMonth = birthdate[:1]

        today = datetime.now()
        date1 = datetime(today.year, int(birthMonth), int(birthdate[3:5]))
        date2 = datetime(today.year+1, int(birthMonth), int(birthdate[3:5]))
        days = ((date1 if date1 > today else date2) - today).days
        return days

async def setup(bot):
    await bot.add_cog(UserAgeInfo(bot))
#test = UserAgeInfo("DiscordBirthdays.csv", bot)