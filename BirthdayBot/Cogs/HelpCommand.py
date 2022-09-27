import discord


async def helpList(ctx):
    embed = discord.Embed(
        title="Bot Commands:",
        description="A list of commands with descriptions that can be used with Bday Bot.",
        color=discord.Color.blue(),
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
