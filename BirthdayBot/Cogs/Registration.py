from contextvars import Context
import discord
from discord.ext import commands
import datetime
from datetime import datetime
from BirthdayBot.Utils import session_scope, logger
from BirthdayBot.Models import DiscordUser
from BirthdayBot.Views import BirthdayInputModal, UpdateUserButtons,UpdateConfirmationButtons, RegisterUserButton, RegisterConfirmationButtons, tryAgainView
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
        #Handles Existing User
        if DiscordUser.does_user_exist(discord_id=ctx.author.id):
            existing_user = DiscordUser.get(discord_id=ctx.author.id)
            await self.handleExistingUser(ctx, existing_user)
            return None

        button_feedback: RegisterUserButton = await self.sendRegistrationView(ctx)

        if button_feedback.timed_out:
            ctx.send("Timed Out")
            return None
        
        modal_input: BirthdayInputModal = await self.waitForModalView()

        if modal_input.timed_out:
            ctx.send("Timed Out")
            return None
        
        if modal_input.recievedValidBirthdayValue is False:
            retry_feedback = self.sendInvalidBirthdayInputRetry(ctx=ctx, update=False)
            if retry_feedback.timed_out:
                ctx.send("Timed Out")
            else:
                
        

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


    async def handleInvalidBirthdayConfirmation(self,ctx, validBirthday: Birthday,*, existing_user: DiscordUser = None):
        while userConfirmation == False and validBirthday == False
            TryAgainView()


    async def sendInvalidBirthdayInputView(self, ctx, *, update: bool) -> tryAgainView:
        try_again_view = tryAgainView(author = ctx.author, update=update)
        await ctx.send(
            f"Invalid Date Format, please try again. (mm/dd/yyyy)",
            view=try_again_view,
        )
        try_again_view.timed_out: bool = await try_again_view.wait()
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


    async def sendRegistrationView(self, ctx) -> RegisterUserButton:
        view = RegisterUserButton(author=ctx.author)
        embed = discord.Embed(
            title="Please enter your Birthday (mm/dd/yyyy)",
            description="This will store your birthday in our database",
            color=discord.Color.red()
        )
        await ctx.send(embed=embed, view=view)
        view.timed_out : bool = await view.wait()
        return view

    async def waitForModalView(modal: BirthdayInputModal) -> BirthdayInputModal:
        modal.timed_out: bool = await modal.wait()
        return modal

    async def getModalFeedback(self, modal: BirthdayInputModal) -> Birthday:
        if modal.recievedValidBirthdayValue:
            return modal.birthdayValue
        else:
            return None


async def setup(bot):
    await bot.add_cog(Registration(bot))
