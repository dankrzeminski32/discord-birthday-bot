import csv
import discord
from dateutil.parser import parse

class bdayConfig:

    def bdayFinder():
        rows = []

        with open("DiscordBirthdays.csv", 'r') as file:
            csvreader = csv.reader(file)
            header = next(csvreader)
            for row in csvreader:
                rows.append(row)

        for i in range(len(rows)):
                for j in range(len(rows[i])):
                        print(rows[i][j])

        for myline in csvreader:
            header=myline
            break

        for myline in csvreader:
            for myColIndex in range(len(myline)):
                if (parse(myline[myColIndex])):
                    print("column = {0}".format(myColIndex))
                    
    bdayFinder()
    