import discord
from discord.ext import commands
import csv
from discord.ui import Button, View

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
            return msg.author == ctx.author and msg.channel == ctx.channel and msg.content.startswith("0")

        msg = await self.bot.wait_for('message', check=check)
        # await ctx.send("{}, Your birthday ({}) has been stored in our database!".format(msg.author,msg.content))
        view = RegistrationButtons(author = ctx.author)
        await self.sendConfirmationMessage(ctx,view)
        if view.userConfirmation is None:
            await ctx.send("Timed out")
        elif view.userConfirmation:
            self.writeUserToCSV(username = msg.author,birthday = msg.content)
            await ctx.send("{}, Your birthday ({}) has been stored in our database!".format(msg.author,msg.content))
        else:
            await self.retryLoop(ctx)
            
            
    """ ---- HELPERS ---- """
    async def retryLoop(self,ctx):
        #Already know userConfirmation == false
        # We want to generate a new view for each confirmation
        loop = True
        while loop:
            view = RegistrationButtons(author = ctx.author)
            view.userConfirmation = False
            def check(msg):
                return msg.author == ctx.author and msg.channel == ctx.channel and msg.content.startswith("0")
            msg = await self.bot.wait_for('message', check=check)
            await self.sendConfirmationMessage(ctx,view)
            if view.userConfirmation != False:
                loop = False
                
        if view.userConfirmation is None:
            await ctx.send("Timed out")
        elif view.userConfirmation:
            self.writeUserToCSV(username = msg.author,birthday = msg.content)
            await ctx.send("{}, Your birthday ({}) has been stored in our database!".format(msg.author,msg.content))
        else:
            print("failure")
        
    async def sendConfirmationMessage(self, ctx, view):
        await ctx.send("Is this correct?", view=view)
        await view.wait()
    
    async def sendRegistrationMessage(self, ctx):
        embed = discord.Embed(
            title = "Please enter your Birthday (Ex:07/11/01)",
            description = "This will store your birthday in our database",
            color = discord.Color.blue()
        )
        await ctx.send(embed=embed)
    
    @staticmethod
    def writeUserToCSV(username: str, birthday: str):
        with open('DiscordBirthdays.csv', "a", newline="") as file:
            myFile = csv.writer(file)
            myFile.writerow([username, birthday])

async def setup(bot):
    await bot.add_cog(Registration(bot))


class RegistrationButtons(discord.ui.View):
    def __init__(self, *, timeout=180, author):
        super().__init__(timeout=timeout)
        self.userConfirmation = None 
        self.author = author
        
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

    async def interaction_check(self, inter: discord.MessageInteraction) -> bool:
        if inter.user != self.author:
            await inter.response.send_message(content="You don't have permission to press this button.", ephemeral=True)
            return False
        return True;