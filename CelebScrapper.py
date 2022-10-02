from pydoc import source_synopsis
from bs4 import BeautifulSoup
from selenium import webdriver
import requests
import time
from BirthdayBot.Utils import session_scope, logger
from BirthdayBot.Models import Base, CelebrityBirthdays


url = "https://www.famousbirthdays.com/september11.html"
ScrollNumber = 5
sleepTimer = 2

options = webdriver.ChromeOptions()
options.add_argument("start-maximized")
options.add_argument("disable-infobars")
options.add_argument("--disable-extensions")
options.add_experimental_option("excludeSwitches", ["enable-logging"])

driver = webdriver.Chrome(options=options)  # path=r'to/chromedriver.exe'
driver.get(url)

soup = BeautifulSoup(driver.page_source, "html.parser")


for link in soup.find_all("a", class_="face person-item clearfix"):
    for link2 in link.find_all("div", class_="info"):
        celebName = link2.find("div", class_="name").text
        celebJob = link2.find("div", class_="title hidden-xs").text
        celebName = celebName.replace(",", "")

        celebAge = celebName[-3:]
        celebName = celebName[:-3]

        celebInfo = CelebrityBirthdays(
            celebName=celebName, celebAge=celebAge, celebJob=celebJob
        )

        try:
            with session_scope() as s:
                s.add(celebInfo)
        except Exception as e:
            logger.error("Scrapper Logger has failed, %s" % e)
