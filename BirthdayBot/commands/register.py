import discord
from discord.ext import commands
import csv
from discord.ui import Button, View
from settings import session_scope
from BirthdayBot.models import DiscordUser

class Registration(commands.Cog):
    """Class Dedicated to housing all commands related to registration"""
    def __init__(self, bot):
        self.bot = bot

    """ ---- COMMANDS ---- """
    @commands.command()
    async def bday(self, ctx):
        await self.sendRegistrationMessage(ctx)

        #Need to improve this validation
        def check(msg):
            return msg.author == ctx.author and msg.channel == ctx.channel

        msg = await self.bot.wait_for('message', check=check)
        
        # await ctx.send("{}, Your birthday ({}) has been stored in our database!".format(msg.author,msg.content))
        view = RegistrationButtons()
        await self.sendConfirmationMessage(ctx,view, msg)
        if view.userConfirmation is None:
            await ctx.send("Timed out")
        elif view.userConfirmation:
            self.writeUserToDB(username = msg.author,birthday = msg.content, discord_id=msg.author.id)
            await ctx.send("{}, Your birthday ({}) has been stored in our database!".format(msg.author,msg.content))
        else:
            await self.retryLoop(ctx)
            
            
    """ ---- HELPERS ---- """
    async def retryLoop(self,ctx):
        #Already know userConfirmation == false
        # We want to generate a new view for each confirmation
        loop = True
        while loop:
            view = RegistrationButtons()
            view.userConfirmation = False
            def check(msg):
                return msg.author == ctx.author and msg.channel == ctx.channel
            msg = await self.bot.wait_for('message', check=check)
            await self.sendConfirmationMessage(ctx,view, msg)
            if view.userConfirmation != False:
                loop = False
                
        if view.userConfirmation is None:
            await ctx.send("Timed out")
        elif view.userConfirmation:
            self.writeUserToDB(username = msg.author,birthday = msg.content, discord_id= msg.author)
            await ctx.send("{}, Your birthday ({}) has been stored in our database!".format(msg.author,msg.content))
        else:
            print("failure")
        
    async def sendConfirmationMessage(self, ctx, view, msg):
        await ctx.send("Is this correct? {}".format(msg.content), view=view)
        await view.wait()
    
    async def sendRegistrationMessage(self, ctx):
        embed = discord.Embed(
            title = "Please enter your Birthday (Ex:07/11/01)",
            description = "This will store your birthday in our database",
            color = discord.Color.blue()
        )
        await ctx.send(embed=embed)
    
    @staticmethod
    def writeUserToDB(username: str, birthday: str, discord_id: str):
        try:
            with session_scope() as s:
                user = DiscordUser(username=str(username), Birthday=birthday, discord_ID=discord_id)
                s.add(user)
            print("success")
        except Exception as e:
            exception = e
            print(e)

async def setup(bot):
    await bot.add_cog(Registration(bot))


class RegistrationButtons(discord.ui.View):
    def __init__(self, *, timeout=180):
        super().__init__(timeout=timeout)
        self.userConfirmation = None 
        
    @discord.ui.button(label="Yes!",style=discord.ButtonStyle.green) # or .success
    async def yes(self,interaction:discord.Interaction,button:discord.ui.Button):
        await interaction.response.send_message("Confirming...") #Ephermal = True if we only want user to see, tbd
        self.userConfirmation = True
        self.stop()
        
    @discord.ui.button(label="No!",style=discord.ButtonStyle.red) # or .danger
    async def no(self,interaction:discord.Interaction,button:discord.ui.Button):
        await interaction.response.send_message("Please try again... (mm/dd/yyyy)")
        self.userConfirmation = False
        self.stop()