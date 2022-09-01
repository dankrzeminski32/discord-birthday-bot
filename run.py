import asyncio
import discord
from discord.ext import commands
from config import DISCORD_BOT_TOKEN
from BirthdayBot.database import Database
from BirthdayBot.database import BirthdayChecker
from os import path
import sys

# Create permission intents, state what our bot should be able to do
intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix = ".", intents = intents)

@bot.event
async def on_ready():
    print(f'We have logged in as {bot.user}')

async def load_extensions():
    extensions = ['BirthdayBot.commands.register', "UserInfo"]
    for filename in extensions:
            await bot.load_extension(filename)

async def create_database():
    if path.exists("DiscordBirthdays.csv"):
        pass
    else:
        Database("DiscordBirthdays.csv")

async def main():
    async with bot:
        await create_database()
        await load_extensions()
        await bot.start(DISCORD_BOT_TOKEN)

#Main Bot Cycle
asyncio.run(main())