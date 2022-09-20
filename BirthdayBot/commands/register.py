import discord
from discord.ext import commands
import csv
from discord.ui import Button, View
from db_settings import session_scope
from BirthdayBot.models import DiscordUser
from sqlalchemy.exc import SQLAlchemyError

class Registration(commands.Cog):
    """Class Dedicated to housing all commands related to registration"""
    def __init__(self, bot):
        self.bot = bot
##########################################################################    
    @commands.command()
    async def test(self, ctx): 
        embed=discord.Embed(title="Happy Birthday,", color=0x0099FF)
        embed.set_image(url="https://www.birthdaywishes.expert/wp-content/uploads/2019/03/Smile-It-is-your-Special-Day-Funny-happy-birthday-image.jpg?ezimgfmt=ng%3Awebp%2Fngcb1%2Frs%3Adevice%2Frscb1-1")
        await ctx.send(embed=embed)
##########################################################################
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
            try:
                self.writeUserToDB(username = msg.author,birthday = msg.content, discord_id=msg.author.id)
                await ctx.send("{}, Your birthday ({}) has been stored in our database!".format(msg.author,msg.content))
            except:
                await ctx.send("Invalid date format... Please try again. (mm/dd/yyyy)")
                await self.retryLoop(ctx)
        else:
            await self.retryLoop(ctx)
            
            
    """ ---- HELPERS ---- """
    async def retryLoop(self,ctx):
        #Already know userConfirmation == false
        # We want to generate a new view for each confirmation
        outerLoop = True
        while outerLoop:
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
                outerLoop = False
            elif view.userConfirmation:
                try:
                    self.writeUserToDB(username = msg.author,birthday = msg.content, discord_id= msg.author.id)
                    await ctx.send("{}, Your birthday ({}) has been stored in our database!".format(msg.author,msg.content))
                    outerLoop = False
                except:
                    await ctx.send("Invalid date format... Please try again. (mm/dd/yyyy)")
                    outerLoop = True
            else:
                print("failure")
        
    async def sendConfirmationMessage(self, ctx, view, msg):
        await ctx.send("Is this correct? {}".format(msg.content), view=view)
        await view.wait()
    
    async def sendRegistrationMessage(self, ctx):
        embed = discord.Embed(
            title = "Please enter your Birthday (mm/dd/yyyy)",
            description = "This will store your birthday in our database",
            color = discord.Color.blue()
        )
        await ctx.send(embed=embed)
    
    @staticmethod
    def writeUserToDB(username: str, birthday: str, discord_id: str):
        # try:
        with session_scope() as s:
            user = DiscordUser(username=str(username), Birthday=birthday, discord_ID=discord_id)
            s.add(user)
        #     print("success")
        #     return True
        # except SQLAlchemyError as e:
        #     error= str(e.__dict__['orig'])
        #     print(error)
            
        #     return False

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