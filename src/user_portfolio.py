# Data utility for user portfolio
import re
from webdriver import get_driver, terminate_driver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup

driver = get_driver()


# Get user account names and numbers
def get_user_accounts():
    accounts = []

    try:
        url = "https://digital.fidelity.com/ftgw/digital/portfolio/positions"
        driver.get(url)
        WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.TAG_NAME, "ap143528-portsum-dashboard-root")))
        WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.CLASS_NAME, 'ag-pinned-left-cols-container')))
        page_source = driver.page_source
        soup = BeautifulSoup(page_source, "html.parser")

        rows = soup.find_all('div', class_=[
            'ag-row-even ag-row-no-focus ag-row-not-inline-editing ag-row ag-row-level-0 ag-row-group ag-row-group-contracted posweb-row-account ag-row-position-absolute ag-row-first',
            'ag-row-odd ag-row-no-focus ag-row-not-inline-editing ag-row ag-row-level-0 ag-row-group ag-row-group-contracted posweb-row-account ag-row-position-absolute',
            'ag-row-even ag-row-no-focus ag-row-not-inline-editing ag-row ag-row-level-0 ag-row-group ag-row-group-contracted posweb-row-account ag-row-position-absolute',
            'ag-row-even ag-row-no-focus ag-row-not-inline-editing ag-row ag-row-level-0 ag-row-group ag-row-group-contracted posweb-row-position ag-row-position-absolute',
            'ag-row-odd ag-row-no-focus ag-row-not-inline-editing ag-row ag-row-level-0 ag-row-group ag-row-group-contracted posweb-row-position ag-row-position-absolute',
            'ag-row-odd ag-row-no-focus ag-row-not-inline-editing ag-row ag-row-level-0 ag-row-group ag-row-group-contracted posweb-row-grand_total ag-row-position-absolute ag-row-last'
        ])

        for row in rows:
            account_name = row.find('span', class_='posweb-cell-account_primary')
            account_number = row.find('span', class_='posweb-cell-account_secondary')

            if account_name and account_number:
                accounts.append([account_number.text.strip(), account_name.text.strip()])

    except Exception as e:
        print(f"Getting user accounts failed:", e)

    return accounts


# Get user balances, balance day changes, available to trade amt, available to withdraw amt, per account
def get_user_balances():
    balances = get_user_accounts()

    try:
        url = "https://digital.fidelity.com/ftgw/digital/portfolio/balances"
        driver.get(url)
        WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.TAG_NAME, "ap143528-portsum-dashboard-root")))
        WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.CLASS_NAME, 'balances-all-accounts')))
        page_source = driver.page_source
        soup = BeautifulSoup(page_source, "html.parser")

        rows = soup.find_all('div', class_=['balances-all-accounts'])

        account_balances = []
        day_changes = []
        available_to_trade_balances = []
        available_to_withdraw_balances = []

        for row in rows:
            account_balance = row.find('div',
                                       'pvd-grid__item pvd-grid__item--column-span-6 pvd-grid__item--column-span-3-at-960 expand-header-section__center-content__amount')
            account_balances.append(account_balance.text.strip())

            sub_balances = []
            balance_divs = row.find_all('div', id='balance')
            for balance_div in balance_divs:
                balance_span = balance_div.find('span', class_='sr-only')
                if balance_span:
                    balance = balance_span.find_next('span').text.strip()
                    sub_balances.append(balance)
            available_to_trade_balances.append(sub_balances[0])
            available_to_withdraw_balances.append(sub_balances[1])

        for i in range(len(account_balances)):
            numbers = re.findall(r'[+-]?\$\d+,\d+\.\d+|[+-]?\$\d+\.\d+', account_balances[i])
            if len(numbers) > 1:
                day_changes.append(numbers[1])
                account_balances[i] = account_balances[i].replace(numbers[1], '').strip()

        for i in range(len(balances)):
            if not day_changes:
                balances[i][1] = [['Balance', account_balances[i]], ['Day change', 'Past market time'],
                                  ['Available to trade', available_to_trade_balances[i]],
                                  ['Available to withdraw', available_to_withdraw_balances[i]]]
            else:
                balances[i][1] = [['Balance', account_balances[i]], ['Day change', day_changes[i]],
                                  ['Available to trade', available_to_trade_balances[i]],
                                  ['Available to withdraw', available_to_withdraw_balances[i]]]

        total_balance = soup.find('div',
                                  class_='pvd-grid__item pvd-grid__item--column-span-6 pvd-grid__item--column-span-3-at-960 total-balance__value pvd-grid--disable-padding')
        split_values = total_balance.text.strip().split(' ')
        if split_values[1] == '$0.00':
            balances.insert(0, [['Total balance', split_values[0]], ['Total day change', 'Past market time']])
        else:
            balances.insert(0, [['Total balance', split_values[0]], ['Total day change', split_values[1]]])

    except Exception as e:
        print(f"Getting user balances failed:", e)

    return balances


def get_user_positions():
    return 0


def get_user_events():
    return 0
