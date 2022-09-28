import asyncio
import discord
from BirthdayBot.Utils import session_scope, logger, recreateDB
from BirthdayBot.Seeder import Seeder
from discord.ext import commands, tasks
from config import (
    DISCORD_BOT_TOKEN,
    DATABASE_URI,
    PATH_TO_BIRTHDAY_IMGS,
    PATH_TO_BIRTHDAY_QUOTES,
)
from BirthdayBot.BirthdayChecker import BirthdayChecker
from datetime import datetime, timedelta
from BirthdayBot.Models import BirthdayImages
from BirthdayBot.Models import BirthdayMessages

# Create permission intents, state what our bot should be able to do
intents = discord.Intents.default()
intents.message_content = True

# DISCORD BOT OBJECT
bot = commands.Bot(command_prefix=".bday ", intents=intents)

# MAIN SEEDER OBJECT
mainSeeder = Seeder(PATH_TO_BIRTHDAY_IMGS, PATH_TO_BIRTHDAY_QUOTES)


def seedDBIfEmpty() -> None:
    try:
        with session_scope() as s:
            if not s.query(BirthdayImages).all():
                logger.info("Birthday Images table was empty. Now seeding...")
                mainSeeder.imageSeed()
            else:
                logger.info("Birthday Images table is filled")

            if not s.query(BirthdayMessages).all():
                logger.info("Birthday Quotes table was empty. Now seeding...")
                mainSeeder.quoteSeed()
            else:
                print("Birthday Quotes table is filled")
    except Exception as e:
        logger.error("Database Seeding Issue, %s" % e)


@bot.event
async def on_ready():
    logger.info(f"We have logged in as {bot.user}")


async def load_extensions():
    extensions = [
        "BirthdayBot.Cogs.Registration",
        "BirthdayBot.Cogs.UserAgeInfo",
        "BirthdayBot.Cogs.Help",
    ]
    for filename in extensions:
        await bot.load_extension(filename)


@tasks.loop(seconds=30)
async def birthdayAnnouncements():
    await bot.wait_until_ready()
    bdaychecker = BirthdayChecker(bot)
    channel = None
    for guild in bot.guilds:
        bdays = bdaychecker.getAllBirthdays(guild)
        for channel in guild.text_channels:
            if channel.name == "birthdays":
                bday_channel = channel.id
                channel = bot.get_channel(bday_channel)
        # what if channel got deleted?
        if channel.name != "birthdays" or channel == None:
            logger.warning("birthdays channel not found in %s" % guild)
            logger.info("Attempting to create 'birthdays' channel in %s" % guild)
            new_channel = await guild.create_text_channel("birthdays")
            channel = bot.get_channel(new_channel.id)
        await bdaychecker.sendBirthdayMessages(bdays, channel)


# Runs at 6:00 am everyday, timezone is the servers timezone, unless changed...
# @birthdayAnnouncements.before_loop
# async def before_birthdayAnnouncements():
#     hour = 18
#     minute = 39
#     await bot.wait_until_ready()
#     now = datetime.now()
#     print(now)
#     future = datetime(now.year, now.month, now.day, hour, minute)
#     if now.hour >= hour and now.minute > minute:
#         future += timedelta(days=1)
#     await asyncio.sleep((future - now).seconds)


async def main():
    async with bot:
        birthdayAnnouncements.start()
        # recreateDB()
        seedDBIfEmpty()
        await load_extensions()
        await bot.start(DISCORD_BOT_TOKEN)


# Main Bot Cycle
asyncio.run(main())
