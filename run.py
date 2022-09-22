import asyncio
import discord
from discord.ext import commands, tasks
from config import DISCORD_BOT_TOKEN, DATABASE_URI
from BirthdayBot.BirthdayChecker import BirthdayChecker
from datetime import datetime, timedelta

# import schedule

# Create permission intents, state what our bot should be able to do
intents = discord.Intents.default()
intents.message_content = True
# intents.guilds = True
# intents.members = True

bot = commands.Bot(command_prefix=".", intents=intents)


@bot.event
async def on_ready():
    print(f"We have logged in as {bot.user}")


async def load_extensions():
    extensions = [
        "BirthdayBot.commands.Registration",
        "BirthdayBot.commands.UserAgeInfo",
    ]
    for filename in extensions:
        await bot.load_extension(filename)


@tasks.loop(hours=24)
async def my_task():
    await bot.wait_until_ready()
    bdaychecker = BirthdayChecker(bot)
    bdays = bdaychecker.getAllBirthdays()
    print(bdays)
    text_channel_list = []
    for guild in bot.guilds:
        for channel in guild.text_channels:
            text_channel_list.append(channel)
    print(text_channel_list)
    channel = bot.get_channel(1012844968903196792)
    await bdaychecker.sendBirthdayMessages(bdays, channel)


# Runs at 6:00 am everyday, timezone is the servers timezone, unless changed...
@my_task.before_loop
async def before_my_task():
    hour = 7
    minute = 0
    await bot.wait_until_ready()
    now = datetime.now()
    print(now)
    future = datetime(now.year, now.month, now.day, hour, minute)
    if now.hour >= hour and now.minute > minute:
        future += timedelta(days=1)
    await asyncio.sleep((future - now).seconds)


async def main():
    async with bot:
        my_task.start()
        await load_extensions()
        await bot.start(DISCORD_BOT_TOKEN)


# Main Bot Cycle
asyncio.run(main())
