import asyncio
import discord
from discord.ext import commands
from config import DISCORD_BOT_TOKEN, DATABASE_URI
from BirthdayBot.BirthdayChecker import BirthdayChecker


# Create permission intents, state what our bot should be able to do
intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix = ".", intents = intents)

@bot.event
async def on_ready():
    print(f'We have logged in as {bot.user}')

async def load_extensions():
    extensions = ['BirthdayBot.commands.register']
    for filename in extensions:
            await bot.load_extension(filename)

def getBirthdays():
    bdaychecker = BirthdayChecker()
    print(bdaychecker.getAllBirthdays())

async def main():
    async with bot:
        await load_extensions()
        getBirthdays()
        await bot.start(DISCORD_BOT_TOKEN)

#Main Bot Cycle
asyncio.run(main())