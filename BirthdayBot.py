import asyncio
from tabnanny import check
import discord
from config import DiscordBotToken
from discord.ext import commands

intents = discord.Intents.default()
intents.message_content = True

client = commands.Bot(command_prefix = ".", intents = intents)

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

client.run(DiscordBotToken)
