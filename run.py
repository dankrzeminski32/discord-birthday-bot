import asyncio
import discord
from BirthdayBot.Utils import session_scope, logger, recreateDB
from BirthdayBot.Seeder import Seeder
from discord.ext import commands, tasks
from config import (
    DISCORD_BOT_TOKEN,
    PATH_TO_BIRTHDAY_IMGS,
    PATH_TO_BIRTHDAY_QUOTES,
)

# Create permission intents, state what our bot should be able to do
intents = discord.Intents.default()
intents.message_content = True

# DISCORD BOT OBJECT
bot = commands.Bot(command_prefix=".bday ", intents=intents, help_command=None)

# MAIN SEEDER OBJECT
mainSeeder = Seeder(PATH_TO_BIRTHDAY_IMGS, PATH_TO_BIRTHDAY_QUOTES)


async def load_extensions():
    extensions = [
        "BirthdayBot.Cogs.Registration",
        "BirthdayBot.Cogs.UserAgeInfo",
        "BirthdayBot.Cogs.Help",
        "BirthdayBot.Cogs.Events",
    ]
    for filename in extensions:
        await bot.load_extension(filename)


async def main():
    async with bot:
        recreateDB()
        mainSeeder.seedDBIfEmpty()
        await load_extensions()
        await bot.start(DISCORD_BOT_TOKEN)


# Main Bot Cycle
asyncio.run(main())
