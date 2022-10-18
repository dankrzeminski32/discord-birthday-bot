import asyncio
import discord
from BirthdayBot.Utils import recreateDB
from BirthdayBot.Seeder import Seeder
from discord.ext import commands, tasks
from config import (
    DISCORD_BOT_TOKEN,
    PATH_TO_BIRTHDAY_QUOTES,
)
from BirthdayBot.Scraper.CelebScraper import ScrapeIt
from BirthdayBot.Models import CommandCounter
from BirthdayBot.Scraper import ImageScraper

intents = discord.Intents.default()
intents.members = True
intents.message_content = True

bot = commands.Bot(command_prefix=".bday ", intents=intents, help_command=None)

mainSeeder = Seeder(PATH_TO_BIRTHDAY_QUOTES)

commandCounter = CommandCounter()


async def load_extensions():
    extensions = [
        "BirthdayBot.Cogs.Registration",
        "BirthdayBot.Cogs.Help",
        "BirthdayBot.Cogs.Events",
        "BirthdayBot.Cogs.BirthdayChecker",
    ]
    for filename in extensions:
        await bot.load_extension(filename)


async def main():
    async with bot:
        # recreateDB()
        mainSeeder.seedDBIfEmpty()
        # ScrapeIt()
        # ImageScraper.ImageScrapeIt()
        await load_extensions()
        await bot.start(DISCORD_BOT_TOKEN)


# Main Bot Cycle
asyncio.run(main())
