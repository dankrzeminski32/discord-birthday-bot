from ast import Break
import discord
from discord.ext import commands
import datetime
from datetime import datetime
from discord.ui import Button, View
from BirthdayBot.Utils import session_scope, logger
from BirthdayBot.Models import DiscordUser
from sqlalchemy.exc import SQLAlchemyError
from BirthdayBot.Cogs.UserAgeInfo import UserAgeInfo
from BirthdayBot.Cogs import Help

# NOTES:
##### MAKE IT SO THE MESSAGE SENDER SEE CONFIRMATION + PLEASE TRY AGAIN + EVERYTHING ELSE
#####SEND BIRTHDAY MESSAGE LOGIC FOR USERS IN OTHER DISCORDS
#####FOR every guild.id check the guild for names in the database if the name is in the database AND in the guild.id then they dont need to re-enter bday for that guild "You already entered your birthday in another guild"
class Registration(commands.Cog):
    """Class Dedicated to housing all commands related to registration"""

    def __init__(self, bot):
        self.bot = bot

    ##########################################################################
    async def test(self, ctx):
        await ctx.send("test")

    ##########################################################################
    """ ---- COMMANDS ---- """

    @commands.hybrid_command(
        name="register",
        description="Prompts the user with a message to register their birthday.",
    )
    async def register(self, ctx):

        username = ctx.author.name + "#" + ctx.author.discriminator

        with session_scope() as session:
            existing_user = (
                session.query(DiscordUser)
                .filter(DiscordUser.username == username)
                .first()
            )
            session.expunge_all()

        # If we have an existing user then throw them into their own "update" loop
        if existing_user is not None:
            existing_user_view = ExistingUserButtons(
                author=ctx.author, existing_user=existing_user
            )
            await ctx.send(
                "You already have a birthday registered, would you like to update this information?",
                view=existing_user_view,
            )
            await self.handleExistingUser(ctx, existing_user_view)
            return None

        await self.sendRegistrationMessage(ctx)

        # Need to improve this validation
        def check(msg):
            return msg.author == ctx.author and msg.channel == ctx.channel

        msg = await self.bot.wait_for("message", check=check)

        author = ctx.author

        # MM/DD/YYYY
        today = datetime.now()
        try:
            inputDate = datetime.strptime(msg.content, "%m/%d/%Y")
        except:
            await ctx.send("Invalid date format. Please try again!")
            await self.retryLoop(ctx)
            return None

        if inputDate > today:
            await ctx.send(
                "PAUSE! You have entered a birthday in the future. Please try again!"
            )
            await self.retryLoop(ctx)
            return None

        view = RegistrationButtons(author=author)
        await self.sendConfirmationMessage(ctx, view, msg)
        if view.userConfirmation is None:
            await ctx.send("Timed out")
        elif view.userConfirmation:
            try:
                self.writeUserToDB(
                    username=msg.author,
                    birthday=msg.content,
                    discord_id=msg.author.id,
                    guild=msg.guild.id,
                )
                await ctx.send(
                    "{}, Your birthday ({}) has been stored in our database!".format(
                        msg.author, msg.content
                    )
                )
                logger.info(
                    "NEW USER REGISTERED: Author: {} Birthday: {} Discord ID: {} Guild: {}".format(
                        msg.author, msg.content, msg.author, msg.guild.id
                    )
                )
            except:
                await ctx.send("Invalid date format... Please try again. (mm/dd/yyyy)")
                await self.retryLoop(ctx)
        else:
            await self.retryLoop(ctx)

    """ ---- HELPERS ---- """

    async def retryLoop(self, ctx):
        # Already know userConfirmation == false
        # We want to generate a new view for each confirmation
        outerLoop = True
        while outerLoop:
            loop = True
            while loop:
                author = ctx.author
                view = RegistrationButtons(author=author)
                view.userConfirmation = False

                def check(msg):
                    return msg.author == ctx.author and msg.channel == ctx.channel

                msg = await self.bot.wait_for("message", check=check)

                validInput = True
                today = datetime.now()
                try:
                    inputDate = datetime.strptime(msg.content, "%m/%d/%Y")
                except:
                    validInput = False

                if (inputDate > today) and validInput == True:
                    await ctx.send(
                        "PAUSE! You have entered a birthday in the future. Please try again."
                    )
                    validInput = False

                if validInput == True:
                    await self.sendConfirmationMessage(ctx, view, msg)
                    if view.userConfirmation != False:
                        loop = False

            if view.userConfirmation is None:
                await ctx.send("Timed out")
                outerLoop = False
            elif view.userConfirmation:
                try:
                    self.writeUserToDB(
                        username=msg.author,
                        birthday=msg.content,
                        discord_id=msg.author.id,
                    )
                    await ctx.send(
                        "{}, Your birthday ({}) has been stored in our database!".format(
                            msg.author, msg.content
                        )
                    )
                    logger.info(
                        "NEW USER REGISTERED: Author: {} Birthday: {} Discord ID: {}".format(
                            msg.author, msg.content, msg.author
                        )
                    )
                    outerLoop = False
                except:
                    await ctx.send(
                        "Invalid date format... Please try again. (mm/dd/yyyy)"
                    )
                    outerLoop = True
            else:
                print("failure")

    async def handleExistingUser(self, ctx, view):
        if view.userConfirmation == False:
            return None
        else:
            # Need to improve this validation
            def check(msg):
                return msg.author == ctx.author and msg.channel == ctx.channel

            msg = await self.bot.wait_for("message", check=check)
            # MM/DD/YYYY
            today = datetime.now()
            try:
                inputDate = datetime.strptime(msg.content, "%m/%d/%Y")
            except:
                await ctx.send("Invalid date format. Please try again!")
                await self.retryLoop(ctx)
                return None

            if inputDate > today:
                await ctx.send(
                    "PAUSE! You have entered a birthday in the future. Please try again!"
                )
                await self.retryLoop(ctx)
                return None

            registrationView = RegistrationButtons(author=ctx.author)
            await self.sendConfirmationMessage(ctx, registrationView, msg)

            if registrationView.userConfirmation is None:
                await ctx.send("Timed out")
            elif registrationView.userConfirmation:
                try:
                    self.updateUserInDB(username=msg.author, new_birthday=msg.content)
                    await ctx.send(
                        "{}, Your birthday ({}) has been updated in our database!".format(
                            msg.author, msg.content
                        )
                    )
                    logger.info(
                        "NEW USER REGISTERED: Author: {} Birthday: {} Discord ID: {}".format(
                            msg.author, msg.content, msg.author
                        )
                    )
                except:
                    await ctx.send(
                        "Invalid date format... Please try again. (mm/dd/yyyy)"
                    )
                    await self.retryLoop(ctx)
            else:
                await self.retryLoop(ctx)

    def updateUserInDB(username, new_birthday, discord_id):
        with session_scope() as session:
            user_to_update = (
                session.query(DiscordUser)
                .filter(DiscordUser.username == username)
                .first()
            )
            user_to_update.Birthday

    async def sendConfirmationMessage(self, ctx, view, msg):
        embed = discord.Embed(
            title="Confirmation:",
            description="Is this correct? {}".format(msg.content),
            color=discord.Color.blue(),
        )
        await ctx.send(embed=embed, view=view)
        await view.wait()

    async def sendRegistrationMessage(self, ctx):
        embed = discord.Embed(
            title="Please enter your Birthday (mm/dd/yyyy)",
            description="This will store your birthday in our database",
            color=discord.Color.blue(),
        )
        await ctx.send(embed=embed)

    @staticmethod
    def writeUserToDB(username: str, birthday: str, discord_id: str, guild: int):
        # session_scope will raise an exception if invalid, use this with try/except
        with session_scope() as s:
            user = DiscordUser(
                username=str(username),
                Birthday=birthday,
                discord_ID=discord_id,
                guild=guild,
            )
            s.add(user)


async def setup(bot):
    await bot.add_cog(Registration(bot))


class RegistrationButtons(discord.ui.View):
    def __init__(self, *, timeout=180, author):
        super().__init__(timeout=timeout)
        self.userConfirmation = None
        self.author = author

    @discord.ui.button(label="Yes! 👍", style=discord.ButtonStyle.green)  # or .success
    async def yes(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_message(
            "Confirming..."
        )  # Ephermal = True if we only want user to see, tbd
        self.userConfirmation = True
        self.stop()

    @discord.ui.button(label="No! 👎", style=discord.ButtonStyle.red)  # or .danger
    async def no(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_message("Please try again... (mm/dd/yyyy)")
        self.userConfirmation = False
        self.stop()

    async def interaction_check(self, inter: discord.MessageInteraction) -> bool:
        if inter.user != self.author:
            await inter.response.send_message(
                content="You don't have permission to press this button.",
                ephemeral=True,
            )
            return False
        return True


class ExistingUserButtons(discord.ui.View):
    def __init__(self, *, timeout=180, author, existing_user: DiscordUser):
        super().__init__(timeout=timeout)
        self.userConfirmation = None
        self.author = author
        self.existing_user_bday = existing_user.Birthday

    @discord.ui.button(label="Yes!", style=discord.ButtonStyle.green)  # or .success
    async def yes(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_message(
            "Please Provide a new Birthday...(mm/dd/yyyy)"
        )  # Ephermal = True if we only want user to see, tbd
        self.userConfirmation = True
        self.stop()

    @discord.ui.button(label="No!", style=discord.ButtonStyle.red)  # or .danger
    async def no(self, interaction: discord.Interaction, button: discord.ui.Button):
        daysAway = UserAgeInfo.daysAway(birthdate=self.existing_user_bday)
        await interaction.response.send_message(
            "Sounds good! Only {} Days from your birthday!".format(daysAway)
        )
        self.userConfirmation = False
        self.stop()

    async def interaction_check(self, inter: discord.MessageInteraction) -> bool:
        if inter.user != self.author:
            await inter.response.send_message(
                content="You don't have permission to press this button.",
                ephemeral=True,
            )
            return False
        return True
