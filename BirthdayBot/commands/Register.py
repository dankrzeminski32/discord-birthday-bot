import discord
from discord.ext import commands
import csv

class Register(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        
    @commands.command()
    async def bday(self, ctx):
        embed = discord.Embed(
            title = "Please enter your Birthday (Ex:07/11/01)",
            description = "This will store your birthday in our database",
            color = discord.Color.blue()
        )
        await ctx.send(embed=embed)

        def check(msg):
            return msg.author == ctx.author and msg.channel == ctx.channel and msg.content.startswith("0")

        msg = await self.bot.wait_for('message', check=check)
        if msg.content.startswith("0"):
            await ctx.send("Your birthday has been stored in our database!")

        await ctx.send(msg.content)    
        user = ctx.author
        userBirthday = msg.content
        await ctx.send(ctx.author)
        
        with open('DiscordBirthdays.csv', "a", newline="") as file:
            myFile = csv.writer(file)
            myFile.writerow([user, userBirthday])

async def setup(bot):
    await bot.add_cog(Register(bot))