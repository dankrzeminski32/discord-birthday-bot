import asyncio
import discord
from BirthdayBot.Utils import recreateDB
from BirthdayBot.Seeder import Seeder
from discord.ext import commands, tasks
from config import (
    DISCORD_BOT_TOKEN,
    PATH_TO_BIRTHDAY_IMGS,
    PATH_TO_BIRTHDAY_QUOTES,
)

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix=".danbday ", intents=intents, help_command=None)

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
        #recreateDB()
        mainSeeder.seedDBIfEmpty()
        await load_extensions()
        await bot.start(DISCORD_BOT_TOKEN)


# Main Bot Cycle
asyncio.run(main())
