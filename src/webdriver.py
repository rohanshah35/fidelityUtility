# Creating web driver for scraping

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from fake_useragent import UserAgent

# Randomize driver agent to dodge website bot detection
ua = UserAgent()
user_agent = ua.random

options = Options()
options.add_argument(f'--user-agent={user_agent}')
options.add_argument('--disable-blink-features=AutomationControlled')
options.add_experimental_option('useAutomationExtension', False)
options.add_experimental_option('excludeSwitches', ['enable-automation'])

driver = webdriver.Chrome(options=options)
driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")


def get_driver():
    return driver


def terminate_driver(driver):
    if driver:
        driver.quit()
