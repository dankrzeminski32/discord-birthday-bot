from contextvars import Context
import discord
from discord.ext import commands
import datetime
from datetime import datetime
from BirthdayBot.Utils import session_scope, logger
from BirthdayBot.Models import DiscordUser
from BirthdayBot.Views import ExistingUserButtons, RegistrationOpenModalButton, RegistrationConfirmationButtons
from BirthdayBot.Birthday import Birthday

class Registration(commands.Cog):
    """Class Dedicated to housing all commands related to registration"""
    def __init__(self, bot):
        self.bot = bot


    """ ---- COMMANDS ---- """
    @commands.hybrid_command(
        name="register",
        description="Prompts the user with a message to register their birthday.",
    )
    async def register(self, ctx):
        existing_user = DiscordUser.get(field = "discord_id", value = ctx.author.id)
        # If we have an existing user then throw them into their own "update" loop
        if existing_user is not None:
            await self.handleExistingUser(ctx, existing_user)
            return None

        modalView = RegistrationOpenModalButton(author=ctx.author)
        await self.sendRegistrationMessage(ctx, modalView)
        await modalView.Modal.wait()
        input_birthday: Birthday = modalView.Modal.birthday
        
        if input_birthday is not None:
            response = await self.sendConfirmationMessage(ctx, input_birthday)
            if response:
                DiscordUser.create(
                    username=ctx.author,
                    birthday=input_birthday,
                    discord_id=ctx.author.id,
                    guild = ctx.guild.id
                )
                logger.info(
                    "NEW USER REGISTERED: Author: {} Birthday: {} Discord ID: {}".format(
                    ctx.author, input_birthday, ctx.author.id
                    ))
            else:
                await ctx.send("Okay, Please try again. (mm/dd/yyyy)")
                await ctx.invoke(self.bot.get_command("register"))
                return None
        else:
            await ctx.send("Invalid date Format, Please try again. (mm/dd/yyyy).")
            await ctx.invoke(self.bot.get_command("register"))
            return None


    """ ---- HELPERS ---- """
    async def handleExistingUser(self, ctx, existing_user: DiscordUser):
        response: bool = self.sendUpdateQuestion(ctx, existing_user = existing_user)
        if response:
            #update the user
            try: #try to update
                pass
                #
            except: #invalid format or timeout failure 
                pass
        else: 
            #send already registered, no update message. 
            await ctx.send(f"Sounds good, see you in {existing_user.birthday.daysUntil()} days")
        
                

    async def sendUpdateQuestion(self, ctx, existing_user) -> bool:
        existing_user_view = ExistingUserButtons(
            author=ctx.author, existing_user=existing_user
            )
        await ctx.send(
            "You already have a birthday registered, would you like to update this information?",
            view=existing_user_view,
        )
        await existing_user_view.wait()
        return existing_user_view.userConfirmation

    async def sendConfirmationMessage(self, ctx, birthday: Birthday) -> bool:
        view = RegistrationConfirmationButtons(author=ctx.author)
        embed = discord.Embed(
            title="Confirmation:",
            description="Is this correct? - {}".format(birthday),
            color=discord.Color.red(),
        )
        await ctx.send(embed=embed, view=view)
        await view.wait()
        return view.userConfirmation

    async def sendRegistrationMessage(self, ctx, view):
        embed = discord.Embed(
            title="Please enter your Birthday (mm/dd/yyyy)",
            description="This will store your birthday in our database",
            color=discord.Color.red()
        )
        await ctx.send(embed=embed, view=view)
        await view.wait()
        


async def setup(bot):
    await bot.add_cog(Registration(bot))