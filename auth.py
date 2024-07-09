import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


def login():
    try:
        driver = webdriver.Chrome()
        driver.get("https://login.fidelity.com/ftgw/Fas/Fidelity/RtlCust/Login/Init")
        WebDriverWait(driver, 30).until(EC.element_to_be_clickable((By.ID, "dom-username-input"))).send_keys("username")
        driver.find_element(By.ID, "dom-pswd-input").send_keys("pswd")
        driver.find_element(By.ID, "dom-login-button").click()
        time.sleep(5)

    except Exception as e:
        print("Login failed")

    finally:
        driver.quit()