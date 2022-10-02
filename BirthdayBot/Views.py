import discord
from BirthdayBot.Models import DiscordUser
import traceback
import sys
from BirthdayBot.Birthday import Birthday


class BaseView(discord.ui.View):
    def __init__(self, *, timeout=180, author: discord.User):
        super().__init__(timeout=timeout)
        self.author = author

    async def interaction_check(self, inter: discord.MessageInteraction) -> bool:
        if inter.user != self.author:
            await inter.response.send_message(
                content=f"{self.invalidInteractionCheckMsg}",
                ephemeral=True,
            )
            return False
        return True

class BaseYesOrNoView(BaseView):
    def __init__(self, author: discord.User):
        super().__init__(author=author)
        self.labels: dict[str, str] = {"no": "No! 👎", "yes": "Yes! 👍"}
        self.button_colors: dict[str, discord.ButtonStyle] = {"no": discord.ButtonStyle.red, "yes": discord.ButtonStyle.green}
        self.responseMessages: dict[str, str]
        self.userConfirmation: bool = None
        self.invalidInteractionCheckMsg: str = "You don't have permission to press this button."
        self.YES_BUTTON_ID: str = "yesConfirmationButton" #used to overwrite callback in subclasses
        self.NO_BUTTON_ID: str = "noConfirmationButton" #used to overwrite callback in subclasses
        self.addButtons()

    def addButtons(self):
        no_button = discord.ui.Button(style=self.button_colors['no'],label=self.labels['no'])
        no_button.custom_id = self.NO_BUTTON_ID
        yes_button = discord.ui.Button(style=self.button_colors['yes'],label=self.labels['yes'])
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

    def get_button(self,id: str) -> discord.ui.Button:
        for button in self.children:
            if button.custom_id == id:
                return button
        
class RegistrationConfirmationButtons(BaseYesOrNoView):
    def __init__(self, author: discord.User):
        super().__init__(author=author)
        self.userConfirmation = None
        self.responseMessages = {"no": "Please try again... (mm/dd/yyyy)", "yes": "Confirming..."}


class RegistrationOpenModalButton(BaseView):
    def __init__(self, author: discord.User):
        super().__init__(author=author)
        self.Modal: RegistrationModal = None
        self.addButton()
        
    def addButton(self):
        open_modal_button = discord.ui.Button(style=discord.ButtonStyle.green,label='Sign Up!')

        async def open_modal_button_callback(interaction: discord.Interaction):
            regModal = RegistrationModal()
            await interaction.response.send_modal(regModal)
            self.Modal = regModal
            self.stop()

        open_modal_button.callback = open_modal_button_callback
        self.add_item(open_modal_button)



class RegistrationModal(discord.ui.Modal, title="Registration Modal"):
    birthdayInput = discord.ui.TextInput(label='Birthday', placeholder="MM/DD/YYY", style=discord.TextStyle.short, min_length=8, max_length=10)
    birthday: Birthday = None
    on_submit_interaction: discord.Interaction
    

    async def on_submit(self, interaction: discord.Interaction):
        try:
            self.on_submit_interaction = interaction
            self.birthday = Birthday.fromUserInput(str(self.birthdayInput))
            await interaction.response.defer()
            self.stop()
        except:
            self.on_submit_interaction = interaction
            self.stop()


class ExistingUserButtons(BaseYesOrNoView):
    def __init__(self, author: discord.User, existing_user: DiscordUser):
        super().__init__(author=author)
        self.daysUntilBirthday: int = existing_user.birthday.daysUntil()
        self.responseMessages = {"no": f"Sounds good! Only {self.daysUntilBirthday} Days from your birthday!", "yes": "Please Provide a new Birthday...(mm/dd/yyyy)"}
        self.yes_button = self.get_button(self.YES_BUTTON_ID)
        self.yes_button.callback = self.openUpdateUserModal_callback
        self.Modal: UpdateUserModal

    async def openUpdateUserModal_callback(self,interaction: discord.Interaction):
        Modal = UpdateUserModal()
        await interaction.response.send_modal(Modal)
        self.userConfirmation = True
        self.stop()
        self.Modal = Modal

class UpdateUserModal(discord.ui.Modal, title="Registration Modal"):
    birthdayInput = discord.ui.TextInput(label='Birthday', placeholder="MM/DD/YYY", style=discord.TextStyle.short, min_length=8, max_length=10)
    updatedBirthday: Birthday = None
    on_submit_interaction: discord.Interaction

    async def on_submit(self, interaction: discord.Interaction):
        try:
            self.on_submit_interaction = interaction
            self.updatedBirthday = Birthday.fromUserInput(str(self.birthdayInput))
            await interaction.response.defer()
            self.stop()
        except:
            self.on_submit_interaction = interaction
            self.stop()
