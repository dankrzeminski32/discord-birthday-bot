from contextvars import Context
import discord
from discord.ext import commands
import datetime
from datetime import datetime
from BirthdayBot.Utils import session_scope, logger
from BirthdayBot.Models import DiscordUser
from BirthdayBot.Views import ExistingUserButtons, RegistrationOpenModalButton, RegistrationConfirmationButtons, UpdateConfirmationButtons, tryAgainView
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
                    username=ctx.author.name,
                    birthday=input_birthday,
                    discord_id=ctx.author.id,
                    guild = ctx.guild.id
                )
                await ctx.send("You have been successfully added to our database")
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
    async def handleExistingUser(self, ctx, existing_user: DiscordUser, second_iteration=False, response=None):
        if second_iteration:
            await self.handleBirthdayConfirmation(ctx,response, existing_user)
            return None

        response: bool = await self.sendUpdateQuestion(ctx, existing_user = existing_user)
        if response.userConfirmation is not None:
            if response.userConfirmation: # User wants to update
                await self.handleBirthdayConfirmation(ctx,response, existing_user)
            else: # User doesnt want to update
                return None
        else:
            ctx.send("Oops, Something went wrong, please try again.")


    async def handleBirthdayConfirmation(self,ctx,response: UpdateConfirmationButtons,existing_user: DiscordUser):
        try: 
            if response.Modal.updatedBirthday is not None:
                dateConfirmationResponse = await self.sendUpdateConfirmationMessage(ctx, response.Modal.updatedBirthday)
                if dateConfirmationResponse.userConfirmation and response.Modal.updatedBirthday != None:# New birthday looks good
                    existing_user.update(field = "birthday",new_value = response.Modal.updatedBirthday)
                    await ctx.send("user updated successfully")
                elif dateConfirmationResponse == False and response.Modal.updatedBirthday != None:# New birthday does not look good
                    await self.handleExistingUser(ctx,existing_user=existing_user, second_iteration=True, response=dateConfirmationResponse)
                else:
                    resp = await self.sendInvalidRetry(ctx, update=True)
                    await self.handleBirthdayConfirmation(ctx, resp, existing_user=existing_user)
            else: 
                resp = await self.sendInvalidRetry(ctx, update=True)
                await self.handleBirthdayConfirmation(ctx, resp, existing_user=existing_user)
        except:
            await ctx.send("Oops, Something went wrong, please try again.")


    async def sendInvalidRetry(self, ctx, update: bool):
        try_again_view = tryAgainView(author = ctx.author, update=update)
        await ctx.send(
            f"Invalid Date Format, please try again. (mm/dd/yyyy)",
            view=try_again_view,
        )
        await try_again_view.wait()
        await try_again_view.Modal.wait()
        return try_again_view

    async def sendUpdateQuestion(self, ctx, existing_user) -> ExistingUserButtons:
        existing_user_view = ExistingUserButtons(
            author=ctx.author, existing_user=existing_user
            )
        await ctx.send(
            f"You already have a birthday registered - {existing_user.birthday}, would you like to update this information?",
            view=existing_user_view,
        )
        await existing_user_view.wait()
        if existing_user_view.userConfirmation:
            await existing_user_view.Modal.wait()
            return existing_user_view
        return existing_user_view


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

    async def sendUpdateConfirmationMessage(self, ctx, birthday: Birthday) -> UpdateConfirmationButtons:
        view = UpdateConfirmationButtons(author=ctx.author)
        embed = discord.Embed(
            title="Confirmation:",
            description="Is this correct? - {}".format(birthday),
            color=discord.Color.red(),
        )
        await ctx.send(embed=embed, view=view)
        await view.wait()
        if view.userConfirmation:
            return view
        await view.Modal.wait()
        return view


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