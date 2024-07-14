# Data utility for user portfolio

from webdriver import get_driver, terminate_driver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup

driver = get_driver()


# Get user account names and numbers
# Incomplete
def get_user_accounts():
    accounts = []

    try:
        url = "https://digital.fidelity.com/ftgw/digital/portfolio/positions"
        driver.get(url)
        soup = BeautifulSoup(driver.page_source, "html.parser")
        position_page = soup.find_all('div', class_='ag-cell ag-cell-not-inline-editing ag-cell-normal-height '
                                                    'ag-cell-last-left-pinned ag-column-first posweb-cell posweb-cell-row_header')

        for account in position_page:
            account_name = account.find('span', class_='posweb-cell-account_primary')
            account_number = account.find('span', class_='posweb-cell-account-secondary')

            if account_name and account_number:
                accounts.append([account_name.text.strip(), account_number.text.strip()])
            else:
                accounts.append([" "])

    except Exception as e:
        print(f"Getting user accounts failed:", e)

    print(accounts)
    return accounts


def get_user_positions():
    return 0


def get_user_balances():
    return 0


def get_user_orders(account_number, time_period):
    return 0
