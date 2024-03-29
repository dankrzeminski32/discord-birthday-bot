import discord
from discord.ext import commands
import platform
from discord.ext.commands import Context
from BirthdayBot.Utils import session_scope, logger
from BirthdayBot.Models import CommandCounter, IssueReports
import datetime
from datetime import date


class Help(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    """---- COMMANDS ----"""

    @commands.hybrid_command(
        name="help", description="Shows all the usable commands for BirthdayBot."
    )
    async def help(self, context: Context) -> None:
        prefix = self.bot.command_prefix
        embed = discord.Embed(
            title="Help", description="List of available commands:", color=0x9C84EF
        )
        for i in self.bot.cogs:
            if i == "Events":
                pass
            else:
                cog = self.bot.get_cog(i)
                commands = cog.get_commands()
                data = []
                for command in commands:
                    description = command.description.partition("\n")[0]
                    data.append(f"{prefix}{command.name} - {description}" + "\n")
                help_text = "\n".join(data)
                embed.add_field(
                    name=i.capitalize(), value=f"```{help_text}```", inline=False
                )
        await context.send(embed=embed)
        CommandCounter.incrementCommand("help")

    """ ---- HELPERS ---- """

    @commands.hybrid_command(
        name="botinfo",
        description="Get some useful (or not) information about the bot.",
    )
    async def botinfo(self, context: Context) -> None:
        """
        Get some useful (or not) information about the bot.

        :param context: The hybrid command context.
        """
        embed = discord.Embed(
            description="Birthday bot created with discord.py", color=0x9C84EF
        )
        embed.set_author(name="Bot Information")
        embed.add_field(
            name="Owner:", value="Dan Krzeminski & Ethan Kvachkoff", inline=True
        )
        embed.add_field(
            name="Python Version:", value=f"{platform.python_version()}", inline=True
        )
        embed.add_field(
            name="Prefix:",
            value=f"/ (Slash Commands) or {self.bot.command_prefix} for normal commands",
            inline=False,
        )
        embed.set_footer(text=f"Requested by {context.author}")
        await context.send(embed=embed)
        CommandCounter.incrementCommand("botinfo")

    @commands.hybrid_command(
        name="serverinfo",
        description="Get some useful (or not) information about the server.",
    )
    async def serverinfo(self, context: Context) -> None:
        """
        Get some useful (or not) information about the server.

        :param context: The hybrid command context.
        """
        roles = [role.name for role in context.guild.roles]
        if len(roles) > 50:
            roles = roles[:50]
            roles.append(f">>>> Displaying[50/{len(roles)}] Roles")
        roles = ", ".join(roles)

        embed = discord.Embed(
            title="**Server Name:**", description=f"{context.guild}", color=0x9C84EF
        )
        if context.guild.icon is not None:
            embed.set_thumbnail(url=context.guild.icon.url)
        embed.add_field(name="Server ID", value=context.guild.id)
        embed.add_field(name="Member Count", value=context.guild.member_count)
        embed.add_field(
            name="Text/Voice Channels", value=f"{len(context.guild.channels)}"
        )
        embed.add_field(name=f"Roles ({len(context.guild.roles)})", value=roles)
        embed.set_footer(text=f"Created at: {context.guild.created_at}")
        await context.send(embed=embed)
        CommandCounter.incrementCommand("serverinfo")

    @commands.hybrid_command(name="ping", description="Check if the bot is alive.")
    async def ping(self, context: Context) -> None:
        """
        Check if the bot is alive.

        :param context: The hybrid command context.
        """
        embed = discord.Embed(
            title="🏓 Pong!",
            description=f"The bot latency is {round(self.bot.latency * 1000)}ms.",
            color=0x9C84EF,
        )
        await context.send(embed=embed)
        CommandCounter.incrementCommand("ping")

    @commands.hybrid_command(
        name="invite",
        description="Get the invite link of the bot to be able to invite it.",
    )
    async def invite(self, context: Context) -> None:
        """
        Get the invite link of the bot to be able to invite it.

        :param context: The hybrid command context.
        """
        embed = discord.Embed(
            description=f"Invite me by clicking [here](https://discordapp.com/oauth2/authorize?&client_id={self.bot.application_id}&scope=bot+applications.commands&permissions=8).",
            color=0xD75BF4,
        )
        invitelink = await context.channel.create_invite(max_uses=1, unique=True)
        try:
            # To know what permissions to give to your bot, please see here: https://discordapi.com/permissions.html and remember to not give Administrator permissions.
            await context.author.send(embed=embed)
            await context.send("I sent you a private message!")
        except discord.Forbidden:
            await context.send(embed=embed)
        CommandCounter.incrementCommand("invite")

    @commands.hybrid_command(
        name="server",
        description="Get the invite link of the discord server of the bot for some support.",
    )
    async def server(self, context: Context) -> None:
        """
        Get the invite link of the discord server of the bot for some support.

        :param context: The hybrid command context.
        """
        embed = discord.Embed(
            description=f"Join the support server for the bot by clicking [here](https://discord.gg/XpTttCjTtj).",
            color=0xD75BF4,
        )
        try:
            await context.author.send(embed=embed)
            await context.send("I sent you a private message!")
        except discord.Forbidden:
            await context.send(embed=embed)
        CommandCounter.incrementCommand("server")

    async def helpList(ctx):
        embed = discord.Embed(
            title="Bot Commands:",
            description="A list of commands with descriptions that can be used with Bday Bot.",
            color=discord.Color.red(),
        )
        embed.add_field(
            name=".bday age @user",
            value="Gives the age of the user along with how many days until their birthday.",
            inline=False,
        ),
        embed.add_field(
            name=".bday register",
            value="Will prompt you to enter your birthday into the data base (mm/dd/yyyy) format.",
            inline=False,
        )
        # To add more commands just add mroe fields! max=25 fields 2/25
        await ctx.send(embed=embed)
        CommandCounter.incrementCommand("helpList")

    @commands.hybrid_command(
        name="report",
        description="used to report issues/bugs found with BirthdayBot.(EX:.bday report ISSUE HERE)",
    )
    async def report(self, ctx, arg) -> None:
        today = date.today()
        resolved = False

        def check(arg):
            return arg.author == ctx.author and arg.channel == ctx.channel

        try:
            with session_scope() as s:
                report = IssueReports(
                    dateCreated=today,
                    issues=arg,
                    guild=ctx.author.guild.id,
                    is_resolved=resolved,
                )
                s.add(report)
        except Exception as e:
            logger.error("Report had an error when being stored, %s" % e)

        await ctx.send("The issue has been reported and will be looked at.")
        CommandCounter.incrementCommand("report")


async def setup(bot):
    await bot.add_cog(Help(bot))
