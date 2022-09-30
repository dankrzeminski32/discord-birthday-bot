import discord
from BirthdayBot.Models import DiscordUser

class BaseView(discord.ui.View):
    def __init__(self, *, timeout=180, author: discord.User):
        super().__init__(timeout=timeout)
        self.author = author
        self.labels: dict[str, str] = {"no": "No! 👎", "yes": "Yes! 👍"}
        self.button_colors: dict[str, discord.ButtonStyle] = {"no": discord.ButtonStyle.red, "yes": discord.ButtonStyle.green}
        self.responseMessages: dict[str, str]
        self.userConfirmation: bool = None
        self.invalidInteractionCheckMsg: str = "You don't have permission to press this button."
        self.addButtons()

    def addButtons(self):
        no_button = discord.ui.Button(style=self.button_colors['no'],label=self.labels['no'])
        yes_button = discord.ui.Button(style=self.button_colors['yes'],label=self.labels['yes'])

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

    async def interaction_check(self, inter: discord.MessageInteraction) -> bool:
        if inter.user != self.author:
            await inter.response.send_message(
                content=f"{self.invalidInteractionCheckMsg}",
                ephemeral=True,
            )
            return False
        return True


class RegistrationButtons(BaseView):
    def __init__(self, author: discord.User):
        super().__init__(author=author)
        self.userConfirmation = None
        self.responseMessages = {"no": "Please try again... (mm/dd/yyyy)", "yes": "Confirming..."}



class ExistingUserButtons(BaseView):
    def __init__(self, author: discord.User, existing_user: DiscordUser):
        super().__init__(author=author)
        self.daysUntilBirthday: int = existing_user.birthday.daysUntil()
        self.responseMessages = {"no": f"Sounds good! Only {self.daysUntilBirthday} Days from your birthday!", "yes": "Please Provide a new Birthday...(mm/dd/yyyy)"}