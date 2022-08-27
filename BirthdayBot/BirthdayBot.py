import discord
import csv
import os
from config import DiscordBotToken
from discord.ext import commands
from os.path import exists

file_path = "DiscordBirthdays.csv"
file_exists = os.path.exists('DiscordBirthdays.csv')

intents = discord.Intents.default()
intents.message_content = True

client = commands.Bot(command_prefix = ".", intents = intents)

if file_exists:
    if os.stat(file_path).st_size == 0:
        with open('DiscordBirthdays.csv', "w", newline="") as file:
            myFile =csv.writer(file)

            myFile.writerow(["DiscordName","Birthday"])
else:
    with open('DiscordBirthdays.csv', "w", newline="") as file:
            myFile =csv.writer(file)

            myFile.writerow(["DiscordName","Birthday"])