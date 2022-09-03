from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager as CM
import config
import time
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

def login_youtube(email,password):
    try:
        driver = webdriver.Chrome(CM().install())
        driver.get(r'https://accounts.google.com/signin/v2/identifier?continue='+\
        'https%3A%2F%2Fmail.google.com%2Fmail%2F&service=mail&sacu=1&rip=1'+\
        '&flowName=GlifWebSignIn&flowEntry = ServiceLogin')
        driver.implicitly_wait(15)
    
        loginBox = driver.find_element_by_xpath('//*[@id ="identifierId"]')
        loginBox.send_keys(email)
    
        nextButton = driver.find_elements_by_xpath('//*[@id ="identifierNext"]')
        nextButton[0].click()
    
        passWordBox = driver.find_element_by_xpath(
            '//*[@id ="password"]/div[1]/div / div[1]/input')
        passWordBox.send_keys(password)
    
        nextButton = driver.find_elements_by_xpath('//*[@id ="passwordNext"]')
        nextButton[0].click()
    
        print('Login Successful...!!')
        return driver
    except:
        print('Login Failed')