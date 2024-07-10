from webdriver import get_driver, terminate_driver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup

driver = get_driver()


def get_fund_profile(fund):
    return 0


def get_fund_details(fund):
    return 0


def get_fund_holdings(fund):
    try:
        driver.get(f"https://research2.fidelity.com/fidelity/screeners/etf/etfholdings.asp?symbol={fund}&view=Holdings")

        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, 'results-table')))

        soup = BeautifulSoup(driver.page_source, 'html.parser')

        table = soup.find('table', class_='results-table sortable')

        if table:
            print(f'{fund}')
            headers = [th.text.strip() for th in table.find('thead').find_all('th')]
            print(headers)

            for row in table.find('tbody').find_all('tr'):
                cols = row.find_all('td')
                data = [col.text.strip() for col in cols]
                print(data)
        else:
            print("Table not found in the HTML content")

    except Exception as e:
        print("Getting fund holdings failed:", e)
        terminate_driver(driver)
