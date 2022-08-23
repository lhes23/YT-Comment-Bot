import time
import random
import spintax
import requests
import config
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from functions import *
from webdriver_manager.chrome import ChromeDriverManager as CM
from selenium.webdriver.common.by import By

# running bot------------------------------------------------------------------------------------
if __name__ == '__main__':

    while True:
        #### 1st option
        driver = youtube_login(config.email, config.password)
        
        #### 2nd option
        # driver = webdriver.Chrome(CM().install())
        
        #### 3rd option
        # driver = getDriver()
        # driver.get("https://youtube.com")

        key = driver.find_element(By.NAME,'search_query')

        # get keyword list and extract each key
        with open('keywords.txt', 'r') as f:
            keywords = [line.strip() for line in f]
            random_keyword = random.choice(keywords)
            keys = spintax.spin(random_keyword)

            # send keyword in the search box
            for char in keys:
                key.send_keys(char)

        time.sleep(10)

        # search_icon = driver.find_element(By.CSS_SELECTOR,'#search-icon-legacy > yt-icon')
        # WebDriverWait(driver, 50).until(EC.presence_of_element_located(search_icon))

        # click search icon
        driver.find_element(By.CSS_SELECTOR,'#search-icon-legacy > yt-icon').click()
        time.sleep(3)

        # click filter button to filter the videos for the recently uploaded, you can remove or edit this option
        # driver.find_element(By.CSS_SELECTOR,'#container > ytd-toggle-button-renderer > a').click()
        # time.sleep(3)

        # filtering for last hour
        # driver.find_element(By.XPATH,"(//yt-formatted-string[@class='style-scope ytd-search-filter-renderer'])[1]").click()
        # time.sleep(3)

        # grabbing videos titles
        for i in range(2):
            ActionChains(driver).send_keys(Keys.END).perform()
            time.sleep(3)
        titles = driver.find_elements(By.XPATH,'//*[@id="video-title"]')

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
