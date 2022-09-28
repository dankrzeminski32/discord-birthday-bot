import discord
from discord.ext import commands
from BirthdayBot.Utils import logger


class Events(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_guild_join(self, guild):
        new_channel = await guild.create_text_channel("birthdays")
        channel = guild.get_channel(new_channel.id)
        await channel.send(
            f"Hello {guild.name}! I am BirthdayBot. Thank you for inviting me.\n\n"
        )
        logger.info(f"Bot successfully joined {guild.name} and sent a join message!")


async def setup(bot):
    await bot.add_cog(Events(bot))
