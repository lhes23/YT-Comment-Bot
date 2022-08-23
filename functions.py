import os
import time
from random import randint
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import numpy as np
from selenium.common.exceptions import NoSuchElementException
from bs4 import BeautifulSoup
from webdriver_manager.chrome import ChromeDriverManager as CM
from selenium_stealth import stealth
import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
import geckodriver_autoinstaller
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
import ssl
from selenium.webdriver.common.action_chains import ActionChains
import config


# login bot===================================================================================================
def youtube_login(email, password):
    ssl._create_default_https_context = ssl._create_unverified_context
    op = webdriver.ChromeOptions()
    op.add_argument('--disable-dev-shm-usage')
    op.add_argument('--disable-gpu')
    op.add_argument("--disable-infobars")
    op.add_argument("--log-level=3")
    op.add_argument("--disable-extensions")
    op.add_argument("window-size=1200x600")

    # driver = webdriver.Chrome(options=op, executable_path=CM().install())

    driver = uc.Chrome(use_subprocess=True,options=op, executable_path=CM().install())
    driver.execute_script("document.body.style.zoom='80%'")

    driver.get('https://accounts.google.com/signin/v2/identifier?service=youtube&uilel=3&passive=true&continue=https%3A%2F%2Fwww.youtube.com%2Fsignin%3Faction_handle_signin%3Dtrue%26app%3Ddesktop%26hl%3Den%26next%3Dhttps%253A%252F%252Fwww.youtube.com%252F&hl=en&ec=65620&flowName=GlifWebSignIn&flowEntry=ServiceLogin')

    print("=============================================================================================================")
    print("Google Login")

    # finding email field and putting our email on it
    email_field = driver.find_element(By.XPATH,'//*[@id="identifierId"]')
    email_field.send_keys(email)

    driver.find_element(By.ID,"identifierNext").click()
    
    time.sleep(randint(2,5))
    print("email - done")

    # finding pass field and putting our pass on it
    find_pass_field = (By.XPATH, '//*[@id="password"]/div[1]/div/div[1]/input')
    WebDriverWait(driver, 50).until(EC.presence_of_element_located(find_pass_field))
    pass_field = driver.find_element(*find_pass_field)
    WebDriverWait(driver, 50).until(EC.element_to_be_clickable(find_pass_field))
    pass_field.send_keys(password)
    driver.find_element(By.ID,"passwordNext").click()

    time.sleep(randint(2, 5))
    print("password - done")

    WebDriverWait(driver, 200).until(EC.presence_of_element_located((By.CSS_SELECTOR, "ytd-masthead button#avatar-btn")))
    print("Successfully login")
    print("============================================================================================================")

    return driver
# ==============================================================================================================


# comment bot===================================================================================================
def comment_page(driver, urls, comment):

    if len(urls) == 0:
        print("============================================================================================================")
        print('Finished keyword jumping to next one...')
        return []

    # gettin a video link from the list
    url = urls.pop()

    driver.get(url)
    print("Video url:" + url)
    driver.implicitly_wait(1)

    # checking if video is unavailable
    if not check_exists_by_xpath(driver, '//*[@id="movie_player"]'):
        print("skipped")
        return comment_page(driver, urls, random_comment())

    time.sleep(2)
    # You can add like function by uncommenting 4 lines below
    # like_button = EC.presence_of_element_located(By.XPATH, '/html/body/ytd-app/div/ytd-page-manager/ytd-watch-flexy/div[4]/div[1]/div/div[5]/div[2]/ytd-video-primary-info-renderer/div/div/div[3]/div/ytd-menu-renderer/div/ytd-toggle-button-renderer[1]/a/yt-icon-button/button/yt-icon')
    # WebDriverWait(driver, 50).until(EC.element_to_be_clickable(like_button)).click()
    # print('Liked')
    # time.sleep(1)
    driver.execute_script("window.scrollTo(0, window.scrollY + 500)")
    time.sleep(1)

    # checking if comments are disabled
    if not check_exists_by_xpath(driver, '//*[@id="simple-box"]/ytd-comment-simplebox-renderer'):
        print("skipped")
        return comment_page(driver, urls, random_comment())

    # checking if video is a livestream
    if check_exists_by_xpath(driver, '//*[@id="contents"]/ytd-message-renderer'):
        print("skipped")
        return comment_page(driver, urls, random_comment())

    # finding comment box and submiting our comment on it
    comment_box = EC.presence_of_element_located(
        (By.CSS_SELECTOR, '#placeholder-area'))
    WebDriverWait(driver, 4).until(comment_box)
    comment_box1 = driver.find_element(By.CSS_SELECTOR,'#placeholder-area')

    
    ActionChains(driver).move_to_element(
        comment_box1).click(comment_box1).perform()
    
    add_comment_onit = driver.find_element(By.CSS_SELECTOR,'#contenteditable-root')
    
    add_comment_onit.send_keys(comment)
    driver.find_element(By.CSS_SELECTOR,'#submit-button').click()
    print("done")

    time.sleep(randint(2, 5))

    return comment_page(driver, urls, random_comment())
# ==============================================================================================================

# comment section
def random_comment():
    # You can edit these lines if you want to add more comments===================================
    comments = [
        'Loved it',
        'Hello',
        '-loved it-',
        '_good job_'

    ]
    r = np.random.randint(0, len(comments))

    return comments[r]
# =============================================================================================

def check_exists_by_xpath(driver, xpath):
    try:
        driver.find_element(By.XPATH,xpath)
    except NoSuchElementException:
        return False

    return True