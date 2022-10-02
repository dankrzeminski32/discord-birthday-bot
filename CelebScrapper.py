from pydoc import source_synopsis
from bs4 import BeautifulSoup
from selenium import webdriver
import requests
import time
from BirthdayBot.Utils import session_scope, logger
from BirthdayBot.Models import Base, CelebrityBirthdays

# Has to be lower case months or wont work.
monthsWith29 = ["february"]
monthsWith30 = ["april", "june", "september", "november"]
monthsWith31 = ["december", "march", "january", "may", "july", "august", "october"]


"""for month in monthsWith29:
    for i in range(29):
        url = f"https://www.famousbirthdays.com/{month}{i}.html"
for month in monthsWith30:
    for i in range(30):
        url = f"https://www.famousbirthdays.com/{month}{i}.html"
for month in monthsWith31:
    for i in range(31):
        url = f"https://www.famousbirthdays.com/{month}{i}.html"
"""
# url = "https://www.famousbirthdays.com/september11.html"
ScrollNumber = 5
sleepTimer = 5

options = webdriver.ChromeOptions()
options.add_argument("start-maximized")
options.add_argument("disable-infobars")
options.add_argument("--disable-extensions")
options.add_experimental_option("excludeSwitches", ["enable-logging"])

driver = webdriver.Chrome(options=options)  # path=r'to/chromedriver.exe'

for month in monthsWith29:
    for i in range(1, 29, 1):
        celebBirthdate = month + " " + str(i)
        url = f"https://www.famousbirthdays.com/{month}{i}.html"
        driver.get(url)

        soup = BeautifulSoup(driver.page_source, "html.parser")

        for link in soup.find_all("a", class_="face person-item clearfix"):
            for link2 in link.find_all("div", class_="info"):
                celebName = link2.find("div", class_="name").text
                node = link2.find("div", class_="title hidden-xs")
                if node is not None:
                    celebJob = node.text
                else:
                    celebJob = "Celebrity"
                celebName = celebName.replace(",", "")

                celebAge = celebName[-3:]
                celebName = celebName[:-3]

                celebInfo = CelebrityBirthdays(
                    celebName=celebName,
                    celebAge=celebAge,
                    celebJob=celebJob,
                    celebBirthdate=celebBirthdate,
                )

                try:
                    with session_scope() as s:
                        s.add(celebInfo)
                except Exception as e:
                    logger.error("Scrapper Logger has failed, %s" % e)
        time.sleep(sleepTimer)
