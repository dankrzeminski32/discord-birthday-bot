from pydoc import source_synopsis
from bs4 import BeautifulSoup
from selenium import webdriver
import requests
import time


url = "https://tenor.com/search/birthday-gifs"
url2 = "https://www.myhappybirthdaywishes.com/best-happy-birthday-images/"
ScrollNumber = 5
sleepTimer = 2

options = webdriver.ChromeOptions()
options.add_argument("start-maximized")
options.add_argument("disable-infobars")
options.add_argument("--disable-extensions")
options.add_experimental_option("excludeSwitches", ["enable-logging"])

# file_object = open("BirthdayImages.txt", "a")

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
        # file_object.write(link.get("src") + "\n")
        print(link.get("src"))
        count += 1
    # print(link.get('alt'))

print(count)
# file_object.close()
