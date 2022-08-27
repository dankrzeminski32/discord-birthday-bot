import discord
import csv
import os
from config import DiscordBotToken
from discord.ext import commands

file_path = "DiscordBirthdays.csv"

intents = discord.Intents.default()
intents.message_content = True

client = commands.Bot(command_prefix = ".", intents = intents)

if os.stat(file_path).st_size == 0:
    with open('DiscordBirthdays.csv', "w", newline="") as file:
        myFile =csv.writer(file)

        myFile.writerow(["DiscordName","Birthday"])

@client.event
async def on_ready():
    print(f'We have logged in as {client.user}')

@client.command()
async def test(ctx):
    await ctx.send("Hello World!")

@client.command(name="bday")
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

client.run(DiscordBotToken)
