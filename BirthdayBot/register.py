import discord

class Register:
    """
    Provides functionality for users to register their birthdays into the bot
    """

    def __init__(self, bot):
        self.bot = bot    

@client.command()
async def bday(ctx):
    embed = discord.Embed(
        title = "Please enter your Birthday (Ex:07/11/01)",
        description = "This will store your birthday in our database",
        color = discord.Color.blue()
    )
    await ctx.send(embed=embed)

    

    def check(msg):
        return msg.author == ctx.author and msg.channel == ctx.channel and msg.content.startswith("0")
        
    msg = await client.wait_for('message', check=check)
    if msg.content.startswith("0"):
        await ctx.send("Your birthday has been stored in our database!")

    await ctx.send(msg.content)    
    user = ctx.author
    userBirthday = msg.content
    await ctx.send(ctx.author)
    
    with open('DiscordBirthdays.csv', "a", newline="") as file:
        myFile = csv.writer(file)
        myFile.writerow([user, userBirthday])
