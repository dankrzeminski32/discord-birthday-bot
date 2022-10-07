from pydoc import source_synopsis
from bs4 import BeautifulSoup
from selenium import webdriver
import requests
import time
from BirthdayBot.Models import BirthdayImages

from BirthdayBot.Utils import session_scope, logger


def ImageScrapeIt():
    url = "https://tenor.com/search/birthday-gifs"
    url2 = "https://www.myhappybirthdaywishes.com/best-happy-birthday-images/"
    ScrollNumber = 5
    sleepTimer = 2

    options = webdriver.ChromeOptions()
    options.add_argument("start-maximized")
    options.add_argument("disable-infobars")
    options.add_argument("--disable-extensions")
    options.add_experimental_option("excludeSwitches", ["enable-logging"])

    driver = webdriver.Chrome(options=options)  # path=r'to/chromedriver.exe'
    driver.get(url)

    for _ in range(1, ScrollNumber):
        driver.execute_script("window.scrollTo(1,100000)")
        print("scrolling")
        time.sleep(sleepTimer)

    count = 0
    soup = BeautifulSoup(driver.page_source, "html.parser")

    for link in soup.find_all("img"):
        if link.get("src")[0:5] == "https":
            imageUrl = BirthdayImages(bdayImage=link.get("src"))
            try:
                with session_scope() as s:
                    s.add(imageUrl)
            except Exception as e:
                logger.error("Scraper Logger has failed, %s" % e)

            count += 1
    print(count)

    driver.get(url2)

    count = 0
    soup = BeautifulSoup(driver.page_source, "html.parser")

    for link in soup.find_all("img"):
        if link.get("src")[0:5] == "https":
            imageUrl = BirthdayImages(bdayImage=link.get("src"))
            try:
                with session_scope() as s:
                    s.add(imageUrl)
            except Exception as e:
                logger.error("Scraper Logger has failed, %s" % e)

            count += 1

    print(count)
