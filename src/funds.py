# Data for funds

from webdriver import get_driver, terminate_driver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup

driver = get_driver()


# Get fund performance data at regular intervals
def get_fund_performance(fund):
    return 0


# Get fund profile data
def get_fund_profile(fund):
    try:
        driver.get(f"https://digital.fidelity.com/prgw/digital/research/quote/dashboard/summary?symbol={fund}")

    except Exception as e:
        print("Getting fund profile failed:", e)
        terminate_driver(driver)


# Get fund detail data
def get_fund_details(fund):
    details = []

    try:
        driver.get(f"https://digital.fidelity.com/prgw/digital/research/quote/dashboard/summary?symbol={fund}")
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, 'info')))
        soup = BeautifulSoup(driver.page_source, 'html.parser')
        info_container = soup.find('div', class_='info')

        if info_container:
            rows = info_container.find_all('div', class_=['item', 'item ng-star-inserted'])

            for row in rows:
                row_data = []
                left = row.find('div', class_=['left', 'left xl-label', 'left ng-star-inserted', 'left market-tier'])
                as_of_date = row.find('div', class_='as-of-date ng-star-inserted')
                right = row.find('div', class_=['right', 'right ng-star-inserted', 'right nre-green ng-star-inserted',
                                                'right market-tier ng-star-inserted'])

                if left:
                    row_data.append(left.text.strip())

                if as_of_date:
                    row_data.append(as_of_date.text.strip())

                if right:
                    row_data.append(right.text.strip())

                if row_data:
                    details.append(row_data)
                    print(f"Row {i}: {row_data}")

            else:
                print("No fund details found")

    except Exception as e:
        print("Getting fund details failed:", e)
        terminate_driver(driver)

    return details


# Get fund holdings
def get_fund_holdings(fund):
    holdings = []

    try:
        driver.get(f"https://research2.fidelity.com/fidelity/screeners/etf/etfholdings.asp?symbol={fund}&view=Holdings")
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, 'results-table')))
        soup = BeautifulSoup(driver.page_source, 'html.parser')
        table = soup.find('table', class_='results-table sortable')

        if table:
            print(f'{fund}')
            headers = [th.text.strip() for th in table.find('thead').find_all('th')]
            print(headers)
            holdings.append(headers)

            for row in table.find('tbody').find_all('tr'):
                cols = row.find_all('td')
                data = [col.text.strip() for col in cols]
                print(data)
                holdings.append(data)
        else:
            print("Table not found in the HTML content")

    except Exception as e:
        print("Getting fund holdings failed:", e)
        terminate_driver(driver)

    return holdings
