from pydoc import source_synopsis
from bs4 import BeautifulSoup
from selenium import webdriver
import requests
import time
from BirthdayBot.Utils import session_scope, logger
from BirthdayBot.Models import Base, CelebrityBirthdays
import datetime
from datetime import datetime

from webdriver_manager.chrome import (
    ChromeDriverManager,
)  # import doesnt work even after pip install webdriver_manager. Noted By:Ethan
import re


def ScrapeIt():

    # Has to be lower case months or wont work.
    monthsWith29 = ["february"]
    monthsWith30 = ["april", "june", "september", "november"]
    monthsWith31 = ["october", "december", "march", "january", "may", "july", "august"]

    options = webdriver.ChromeOptions()
    options.add_argument("start-maximized")
    options.add_argument("disable-infobars")
    options.add_argument("--disable-extensions")
    options.add_experimental_option("excludeSwitches", ["enable-logging"])

    driver = webdriver.Chrome(ChromeDriverManager().install(), options=options)

    # driver = webdriver.Chrome(options=options)  # Usable for Ethan Windows
    sleepTimer = 2

    class CelebrityScraper(object):
        EXPR = r"https:\/\/www.famousbirthdays.com\/thumbnails\/.*\)"
        DEFAULT_IMG_EXPR = r"https:\/\/www.famousbirthdays.com\/faces\/.*\)"

        def Scrape(month, day):
            i = 0
            numMonth = datetime.strptime(month, "%B")
            numMonth = str(numMonth.month)
            numDay = str(day)
            celebBirthdate = numMonth + "/" + numDay + "/" + str(2000)

            celebBirthdate = datetime.strptime(celebBirthdate, "%m/%d/%Y")

            url = f"https://www.famousbirthdays.com/{month}{day}.html"
            driver.get(url)

            soup = BeautifulSoup(driver.page_source, "html.parser")

            for link in soup.find_all("a", class_="face person-item clearfix"):

                match = CelebrityScraper.get_regex_img_link_match(link=link)

                for link2 in link.find_all("div", class_="info"):
                    celebName = link2.find("div", class_="name").text

                    celebName = celebName.replace("\n", "")
                    if celebName.endswith("months"):
                        pass
                    elif celebName.endswith("days"):
                        pass
                    else:
                        node = link2.find("div", class_="title hidden-xs")

                        if node is not None:
                            celebJob = node.text
                        else:
                            celebJob = "Celebrity"

                        if celebName.endswith(")"):
                            lifeSpan = celebName.split("(")[1]
                            if len(lifeSpan) != 10:
                                pass
                            else:
                                celebName = celebName.split("(")[0]
                                lifeSpan = lifeSpan[:-1]
                                celebAge = int(lifeSpan[5:]) - int(lifeSpan[:4])
                        else:
                            lifeSpan = "Null"

                            cName = celebName.split(",")
                            if len(cName) != 2:
                                pass
                            else:
                                celebName = cName[0]
                                celebAge = cName[1]

                        celebInfo = CelebrityBirthdays(
                            celebName=celebName,
                            celebAge=celebAge,
                            celebJob=celebJob,
                            _celebBirthdate=celebBirthdate,
                            celebLifeSpan=lifeSpan,
                            celebImgLink=match,
                        )

                        try:
                            with session_scope() as s:
                                s.add(celebInfo)
                        except Exception as e:
                            logger.error("Scraper Logger has failed, %s" % e)
                        i += 1
            i += i
            print(i)

        def get_regex_img_link_match(link):
            get_result: re.Match = re.search(
                CelebrityScraper.EXPR, str(link.get("style"))
            )
            if get_result:
                result = get_result.group()
                result = result[:-1]
                print(result)
                return result
            else:
                get_default_match: re.Match = re.search(
                    CelebrityScraper.DEFAULT_IMG_EXPR, str(link.get("style"))
                )
                if get_default_match:
                    result = get_default_match.group()
                    result = result[:-1]
                    print(result)
                    return result
                else:
                    print("No Match Found")
                    return None

    for month in monthsWith31:
        for i in range(1, 32, 1):
            CelebrityScraper.Scrape(month, i)
            time.sleep(sleepTimer)
    for month in monthsWith29:
        for i in range(1, 30, 1):
            CelebrityScraper.Scrape(month, i)
            time.sleep(sleepTimer)
    for month in monthsWith30:
        for i in range(1, 31, 1):
            CelebrityScraper.Scrape(month, i)
            time.sleep(sleepTimer)


# ScrapeIt()
