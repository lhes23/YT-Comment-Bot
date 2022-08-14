# import os
import time
import random
import spintax
import requests
import config
# import numpy as np
# from bs4 import BeautifulSoup
# from selenium import webdriver
# from selenium.webdriver.common.by import By
# from selenium.webdriver.support.ui import WebDriverWait
# from random import randint, randrange
from selenium.webdriver.common.action_chains import ActionChains
# from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
# from selenium.common.exceptions import NoSuchElementException
# from webdriver_manager.chrome import ChromeDriverManager as CM
from functions import *


# running bot------------------------------------------------------------------------------------
if __name__ == '__main__':

    driver = youtube_login(config.email, config.password)

    while True:
        key = driver.find_element_by_name('search_query')

        # get keyword list and extract each key
        with open('keywords.txt', 'r') as f:
            keywords = [line.strip() for line in f]
            random_keyword = random.choice(keywords)
            keys = spintax.spin(random_keyword)

            # send keyword in the search box
            for char in keys:
                key.send_keys(char)

        time.sleep(1)

        # click search icon
        driver.find_element_by_css_selector(
            '#search-icon-legacy > yt-icon').click()
        time.sleep(3)
        # click filter button to filter the videos for the recently uploaded, you can remove or edit this option
        driver.find_element_by_css_selector(
            '#container > ytd-toggle-button-renderer > a').click()
        time.sleep(3)

        # filtering for last hour
        driver.find_element_by_xpath(
            "(//yt-formatted-string[@class='style-scope ytd-search-filter-renderer'])[1]").click()
        time.sleep(3)

        # grabbing videos titles
        for i in range(2):
            ActionChains(driver).send_keys(Keys.END).perform()
            time.sleep(1)
        titles = driver.find_elements_by_xpath('//*[@id="video-title"]')

        urls = []

        # getting url from href attribute in title
        for i in titles:
            if i.get_attribute('href') != None:
                urls.append(i.get_attribute('href'))
            else:
                continue

        # checking if we have links or not
        if urls == []:
            print("There is not videos for this keyword at the moment")
        else:
            comment_page(driver, urls, random_comment())
