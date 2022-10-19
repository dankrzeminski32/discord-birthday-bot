import discord
from sqlalchemy import union
from BirthdayBot.Models import DiscordUser
from BirthdayBot.Birthday import Birthday
import pytz


class BaseView(discord.ui.View):
    def __init__(self, *, timeout=180, author: discord.User):
        super().__init__(timeout=timeout)
        self.author = author
        self.timed_out: bool

    async def interaction_check(self, inter: discord.MessageInteraction) -> bool:
        if inter.user != self.author:
            await inter.response.send_message(
                content=f"{self.invalidInteractionCheckMsg}", ephemeral=True
            )
            return False
        return True


class BaseYesOrNoView(BaseView):
    def __init__(self, author: discord.User):
        super().__init__(author=author)
        self.labels: dict[str, str] = {"no": "No! 👎", "yes": "Yes! 👍"}
        self.button_colors: dict[str, discord.ButtonStyle] = {
            "no": discord.ButtonStyle.red,
            "yes": discord.ButtonStyle.green,
        }
        self.responseMessages: dict[str, str]
        self.userConfirmation: bool = None
        self.invalidInteractionCheckMsg: str = (
            "You don't have permission to press this button."
        )
        self.YES_BUTTON_ID: str = (
            "yesConfirmationButton"  # used to overwrite callback in subclasses
        )
        self.NO_BUTTON_ID: str = (
            "noConfirmationButton"  # used to overwrite callback in subclasses
        )
        self.addButtons()

    def addButtons(self):
        no_button = discord.ui.Button(
            style=self.button_colors["no"], label=self.labels["no"]
        )
        no_button.custom_id = self.NO_BUTTON_ID
        yes_button = discord.ui.Button(
            style=self.button_colors["yes"], label=self.labels["yes"]
        )
        yes_button.custom_id = self.YES_BUTTON_ID

        async def no_button_callback(interaction: discord.Interaction):
            await interaction.response.send_message(f"{self.responseMessages['no']}")
            self.userConfirmation = False
            self.stop()

        async def yes_button_callback(interaction: discord.Interaction):
            await interaction.response.send_message(
                f"{self.responseMessages['yes']}"
            )  # Ephermal = True if we only want user to see, tbd
            self.userConfirmation = True
            self.stop()

        no_button.callback = no_button_callback
        yes_button.callback = yes_button_callback

        self.add_item(no_button)
        self.add_item(yes_button)

    def get_button(self, id: str) -> discord.ui.Button:
        for button in self.children:
            if button.custom_id == id:
                return button


###################### REGISTRATION VIEWS ######################
class RegisterUserButton(BaseView):
    def __init__(self, author: discord.User):
        super().__init__(author=author)
        self.Modal: BirthdayInputModal
        self.addButton()

    def addButton(self):
        open_modal_button = discord.ui.Button(
            style=discord.ButtonStyle.green, label="Sign Up!"
        )

        async def open_modal_button_callback(interaction: discord.Interaction):
            regModal = BirthdayInputModal(title="Register User:")
            await interaction.response.send_modal(regModal)
            self.Modal = regModal
            self.stop()

        open_modal_button.callback = open_modal_button_callback
        self.add_item(open_modal_button)


class RegisterConfirmationButtons(BaseYesOrNoView):
    def __init__(self, author: discord.User):
        super().__init__(author=author)
        self.userConfirmation = None
        self.responseMessages = {
            "no": "Please try again... (mm/dd/yyyy)",
            "yes": "Confirming...",
        }
        self.no_button = self.get_button(self.NO_BUTTON_ID)
        self.no_button.callback = self.openRegisterUserModal_callback
        self.Modal: BirthdayInputModal

    async def openRegisterUserModal_callback(self, interaction: discord.Interaction):
        Modal = BirthdayInputModal(title="Register:")
        await interaction.response.send_modal(Modal)
        self.userConfirmation = False
        self.stop()
        self.Modal = Modal


###################### UPDATE VIEWS ######################
class UpdateUserButtons(BaseYesOrNoView):
    def __init__(self, author: discord.User, existing_user: DiscordUser):
        super().__init__(author=author)
        self.daysUntilBirthday: int = existing_user.birthday.daysUntil()
        self.responseMessages = {
            "no": f"Sounds good! Only {self.daysUntilBirthday} Days from your birthday!",
            "yes": "Please Provide a new Birthday...(mm/dd/yyyy)",
        }
        self.yes_button = self.get_button(self.YES_BUTTON_ID)
        self.yes_button.callback = self.openUpdateUserModal_callback
        self.Modal: BirthdayInputModal

    async def openUpdateUserModal_callback(self, interaction: discord.Interaction):
        Modal = BirthdayInputModal(title="Update User:")
        await interaction.response.send_modal(Modal)
        self.userConfirmation = True
        self.Modal = Modal
        self.stop()


class UpdateConfirmationButtons(BaseYesOrNoView):
    def __init__(self, author: discord.User):
        super().__init__(author=author)
        self.userConfirmation = None
        self.responseMessages = {
            "no": "Please try again... (mm/dd/yyyy)",
            "yes": "Confirming...",
        }
        self.no_button = self.get_button(self.NO_BUTTON_ID)
        self.no_button.callback = self.openUpdateUserModal_callback
        self.Modal: BirthdayInputModal

    async def openUpdateUserModal_callback(self, interaction: discord.Interaction):
        Modal = BirthdayInputModal(title="Update User:")
        await interaction.response.send_modal(Modal)
        self.userConfirmation = False
        self.Modal = Modal
        self.stop()


###################### USE WITH BOTH UPDATE AND REGISTRATION VIEWS ######################
class tryAgainView(BaseView):
    def __init__(self, author: discord.User, update: bool):
        super().__init__(author=author)
        self.userConfirmation: bool = None
        self.update = update
        self.Modal: BirthdayInputModal
        self.tryAgainButton()

    def tryAgainButton(self):
        retry_button = discord.ui.Button(
            style=discord.ButtonStyle.green, label="Try Again!"
        )

        async def retry_button_callback(interaction: discord.Interaction):
            Modal = (
                BirthdayInputModal(title="Update Birthday:")
                if self.update
                else BirthdayInputModal(title="Register Birthday:")
            )
            await interaction.response.send_modal(Modal)
            self.userConfirmation = False
            self.Modal = Modal
            self.stop()

        retry_button.callback = retry_button_callback
        self.add_item(retry_button)


class BirthdayInputModal(discord.ui.Modal):
    def __init__(self, *, title: str):
        super().__init__(title=title)
        self.birthdayTextInput = discord.ui.TextInput(
            label="Birthday",
            placeholder="MM/DD/YYYY",
            style=discord.TextStyle.short,
            min_length=10,
            max_length=10,
        )
        self.timezoneInput = discord.ui.TextInput(
            label="Timezone",
            placeholder="America/Chicago",
            style=discord.TextStyle.short,
            min_length=2,
            max_length=100,
        )
        self.on_submit_interaction: discord.Interaction
        self.birthdayValue: Birthday
        self.timezoneValue: str
        self.recievedValidBirthdayValue: bool
        self.recievedValidTimezone: bool
        self.timed_out: bool
        self.custom_id = "BirthdayInputModal"
        self.add_item(self.birthdayTextInput)
        self.add_item(self.timezoneInput)

    async def on_submit(self, interaction: discord.Interaction):
        # Attempt to create Birthday datetime object from user text input
        try:
            self.birthdayValue = Birthday.fromUserInput(str(self.birthdayTextInput))
            self.recievedValidBirthdayValue = True
        except:
            self.recievedValidBirthdayValue = False

        # Attempt to create timezone object from user text input
        try:
            pytz.timezone(str(self.timezoneInput))
            self.timezoneValue = self.timezoneInput.value
            self.recievedValidTimezone = True
        except:
            self.recievedValidTimezone = False

        self.on_submit_interaction = interaction
        await interaction.response.defer()
        self.stop()
