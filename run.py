import asyncio
import discord
from discord.ext import commands
from config import DISCORD_BOT_TOKEN
from BirthdayBot.database import Database
import sys

# Create permission intents, state what our bot should be able to do
intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix = ".", intents = intents)

@bot.event
async def on_ready():
    print(f'We have logged in as {bot.user}')

async def load_extensions():
    extensions = ['BirthdayBot.commands.Register']
    for filename in extensions:
            await bot.load_extension(filename)

async def load_database():
    bot_database = Database("DiscordBirthdays.csv")

async def main():
    async with bot:
        await load_database()
        await load_extensions()
        await bot.start(DISCORD_BOT_TOKEN)


asyncio.run(main())