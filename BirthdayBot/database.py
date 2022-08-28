import discord
import csv
import os
from discord.ext import commands
from os.path import exists

class Database(object):
    """Handles operations relating to our csv database"""    
    def __init__(self, fileName):
        self.csvFile = open(fileName, "w", newline="")
        self.csvWriter = csv.writer(self.csvFile)
        self.createColumnHeaders()

    def createColumnHeaders(self):
        self.csvWriter.writerow(["DiscordName", "Birthday"])