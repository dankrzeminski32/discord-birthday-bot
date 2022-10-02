import discord
from discord.ext import commands, tasks
from BirthdayBot.Utils import logger
from BirthdayBot.BirthdayChecker import BirthdayChecker
from datetime import datetime
from BirthdayBot.Models import DiscordUser
from BirthdayBot.Birthday import Birthday


class Events(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.birthdayAnnouncements.start()

    @commands.Cog.listener()
    async def on_guild_join(self, guild):
        new_channel = await guild.create_text_channel("birthdays")
        channel = guild.get_channel(new_channel.id)
        await channel.send(
            f"Hello {guild.name}! I am BirthdayBot. Thank you for inviting me.\n\n"
        )
        logger.info(f"Bot successfully joined {guild.name} and sent a join message!")

    @commands.Cog.listener()
    async def on_ready(self):
        logger.info(f"We have logged in as {self.bot.user}")

    @tasks.loop(hours=24)
    async def birthdayAnnouncements(self):
        await self.bot.wait_until_ready()
        bdaychecker = BirthdayChecker(self.bot)
        channel = None
        for guild in self.bot.guilds:
            bdays = DiscordUser.getAll(_birthday=Birthday(datetime.today()))
            for channel in guild.text_channels:
                if channel.name == "birthdays":
                    bday_channel = channel.id
                    channel = self.bot.get_channel(bday_channel)
            # what if channel got deleted?
            if channel.name != "birthdays" or channel == None:
                logger.warning("birthdays channel not found in %s" % guild)
                logger.info("Attempting to create 'birthdays' channel in %s" % guild)
                new_channel = await guild.create_text_channel("birthdays")
                channel = self.bot.get_channel(new_channel.id)
            await bdaychecker.sendBirthdayMessages(bdays, channel)

    # Runs at 6:00 am everyday, timezone is the servers timezone, unless changed...
    # @birthdayAnnouncements.before_loop
    # async def before_birthdayAnnouncements():
    #     hour = 18
    #     minute = 39
    #     await self.bot.wait_until_ready()
    #     now = datetime.now()
    #     print(now)
    #     future = datetime(now.year, now.month, now.day, hour, minute)
    #     if now.hour >= hour and now.minute > minute:
    #         future += timedelta(days=1)
    #     await asyncio.sleep((future - now).seconds)

async def setup(bot):
    await bot.add_cog(Events(bot))
