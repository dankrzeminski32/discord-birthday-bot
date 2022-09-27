import discord


async def on_guild_join(guild):
    embed = discord.Embed(
        title="**======== *Thanks For Adding Me!* ========**",
        description=f"Thanks for adding me to {guild.name}"
        + "!You can use the `.bday helpme` command to get started!",
        color=0xD89522,
    )
    await guild.text_channels[0].send(embed=embed)
