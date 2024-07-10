# Auto login & authentication

from webdriver import get_driver, terminate_driver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

driver = get_driver()


# Login function, handles MFA
def login(username, password):
    try:

        driver.get("https://digital.fidelity.com/prgw/digital/login/full-page")
        WebDriverWait(driver, 30).until(EC.element_to_be_clickable((By.ID, "dom-username-input"))).send_keys(
            username)
        driver.find_element(By.ID, "dom-pswd-input").send_keys(password)
        driver.find_element(By.ID, "dom-login-button").click()
        WebDriverWait(driver, 30).until(EC.element_to_be_clickable((By.ID, "dom-push-primary-button"))).click()
        WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.CLASS_NAME, "summary-print-area")))
        print("Login successful")

        # Keep browser open indefinitely
        input("Press enter to continue...")

    except Exception as e:
        print("Login failed:", e)
        terminate_driver(driver)
