from contextvars import Context
import discord
from discord.ext import commands
import datetime
from datetime import datetime
from BirthdayBot.Utils import session_scope, logger
from BirthdayBot.Models import CommandCounter, DiscordUser
from BirthdayBot.Views import (
    BirthdayInputModal,
    UpdateUserButtons,
    UpdateConfirmationButtons,
    RegisterUserButton,
    RegisterConfirmationButtons,
    tryAgainView,
    TimezoneSelectView
)
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
        # Handles Existing User
        if DiscordUser.does_user_exist(discord_id=ctx.author.id):
            existing_user = DiscordUser.get(discord_id=ctx.author.id)
            await self.handleExistingUser(ctx, existing_user)
            return None

        button_feedback: RegisterUserButton = await self.sendRegistrationView(ctx)

        if button_feedback.timed_out:
            ctx.send("Timed Out")
            return None

        modal_input: BirthdayInputModal = await self.waitForModalView(
            button_feedback.Modal
        )

        if modal_input.timed_out:
            ctx.send("Timed Out")
            return None

        await self.handleBirthdayValidation(ctx, modal_input, update=False)
        CommandCounter.incrementCommand("register")
        return None


    @commands.hybrid_command(
        name="set",
        description="Prompts the user with a message to set the servers timezone",
    )
    async def set(self,ctx):
        await ctx.send("Please pick a timezone from the selection",view=TimezoneSelectView())

    """ ---- HELPERS ---- """

    async def handleExistingUser(self, ctx, existing_user: DiscordUser):
        view: UpdateUserButtons = await self.sendUpdateView(
            ctx, existing_user=existing_user
        )
        if view.timed_out == False:
            if view.userConfirmation:  # User wants to update
                modal_response = await self.waitForModalView(view.Modal)
                await self.handleBirthdayValidation(
                    ctx, modal_response, update=True, existing_user=existing_user
                )
                return None
            else:  # User doesnt want to update
                return None
        else:
            await ctx.send("Timed Out")

    async def handleBirthdayValidation(
        self,
        ctx,
        modalResponseObject: BirthdayInputModal,
        *,
        update: bool,
        existing_user: DiscordUser = None,
    ):
        userConfirmation = False
        validBirthday = False

        while validBirthday == False:
            if modalResponseObject.recievedValidBirthdayValue:
                while userConfirmation == False:
                    confirmation_view: discord.ui.View = (
                        await self.sendConfirmationView(
                            ctx, modalResponseObject.birthdayValue, update=update
                        )
                    )
                    if confirmation_view.userConfirmation == True:
                        if update == False:
                            DiscordUser.create(
                                username=ctx.author.name,
                                birthday=modalResponseObject.birthdayValue,
                                discord_id=ctx.author.id,
                                guild=ctx.guild.id,
                            )
                            await ctx.send(
                                "You have been successfully added to the database!"  # TODO, Make this look pretty
                            )
                        else:
                            DiscordUser.updateBirthday(
                                existing_user.discord_id,
                                modalResponseObject.birthdayValue,
                            )
                            await ctx.send(
                                "You have been updated in the database!"
                            )  # TODO, Make this look pretty
                        return None
                    elif confirmation_view.userConfirmation == False:
                        modalResponseObject = await self.waitForModalView(
                            confirmation_view.Modal
                        )
                        break
            else:
                view = await self.sendTryAgainView(ctx=ctx, update=update)
                modalResponseObject = await self.waitForModalView(view.Modal)

    async def sendTryAgainView(
        self,
        ctx,
        *,
        update: bool,
        preceding_message: str = "Please Try Again (mm/dd/yyyy)",
    ) -> tryAgainView:
        try_again_view = tryAgainView(author=ctx.author, update=update)
        await ctx.send(f"{preceding_message}", view=try_again_view)
        try_again_view.timed_out: bool = await try_again_view.wait()
        return try_again_view  # then doing try_again_view.modal will give you either RegisterModal or UpdateUserModal depending on update: bool

    async def sendUpdateView(self, ctx, existing_user) -> UpdateUserButtons:
        existing_user_view = UpdateUserButtons(
            author=ctx.author, existing_user=existing_user
        )
        await ctx.send(
            f"You already have a birthday registered - {existing_user.birthday}, would you like to update this information?",  # TODO, Make this look pretty
            view=existing_user_view,
        )
        existing_user_view.timed_out = await existing_user_view.wait()
        return existing_user_view

    async def sendConfirmationView(
        self, ctx, birthday: Birthday, *, update: bool
    ) -> discord.ui.View:
        if update:
            view = UpdateConfirmationButtons(author=ctx.author)
        else:
            view = RegisterConfirmationButtons(author=ctx.author)
        embed = discord.Embed(
            title="Confirmation:",
            description="Is this correct? - {}".format(birthday),
            color=discord.Color.red(),
        )
        await ctx.send(embed=embed, view=view)
        view.timed_out = await view.wait()
        return view

    async def sendRegistrationView(self, ctx) -> RegisterUserButton:
        view = RegisterUserButton(author=ctx.author)
        embed = discord.Embed(
            title="Please enter your Birthday (mm/dd/yyyy)",
            description="This will store your birthday in our database",
            color=discord.Color.red(),
        )
        await ctx.send(embed=embed, view=view)
        view.timed_out: bool = await view.wait()
        return view

    async def waitForModalView(self, modal: BirthdayInputModal) -> BirthdayInputModal:
        modal.timed_out: bool = await modal.wait()
        return modal


async def setup(bot):
    await bot.add_cog(Registration(bot))
