# Data utility for funds

from webdriver import get_driver, terminate_driver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup

driver = get_driver()


# Get fund profile
def get_fund_profile(fund):
    return 0


# Get fund performance data at regular intervals
def get_fund_performance(fund):
    performance = [fund]

    try:
        url = f"https://digital.fidelity.com/prgw/digital/research/quote/dashboard/summary?symbol={fund}"
        driver.get(url)
        WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.TAG_NAME, 'body')))
        WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.CLASS_NAME, 'totalReturns')))
        soup = BeautifulSoup(driver.page_source, 'html.parser')

        as_of_element = soup.find('span', class_='timestamp')
        if as_of_element:
            performance.append(as_of_element.text.strip())
        else:
            performance.append("No reference date")

        total_returns = soup.find('div', class_='profile-card-item profile-performance')
        if total_returns:
            rows = total_returns.find_all('tr')
            for row in rows:
                year_element = row.find('th')
                percentage_element = row.find('span', class_='text-pos')
                if year_element and percentage_element:
                    year = year_element.text.strip()
                    percentage = percentage_element.text.strip()
                    performance.append([year, percentage])

    except Exception as e:
        print(f"Getting fund performance failed:", e)

    if len(performance) == 1:
        print(f"No fund performance found for {fund}")

    print(performance)
    return performance


# Get fund specific details
def get_fund_details(fund):
    details = [fund]

    try:
        url = f"https://digital.fidelity.com/prgw/digital/research/quote/dashboard/summary?symbol={fund}"
        driver.get(url)
        WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.TAG_NAME, 'body')))
        WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.CLASS_NAME, 'detailed-quote-body')))
        soup = BeautifulSoup(driver.page_source, 'html.parser')
        quote_body = soup.find('div', class_='detailed-quote-body')

        if quote_body:
            items = quote_body.find_all('div', class_=['item', 'item ng-star-inserted'])

            for i, item in enumerate(items, 1):
                if i == 6:
                    continue

                row_data = []
                left = item.find('div', class_='left')
                as_of_date = item.find('div', class_='as-of-date ng-star-inserted')
                right = item.find('div', class_=['right', 'right ng-star-inserted', 'right nre-green ng-star-inserted'])

                if left:
                    left_text = left.text.strip()
                    if "Close Popover" in left_text:
                        left_text = "30-day SEC yield"
                    row_data.append(left_text)
                if as_of_date:
                    row_data.append(as_of_date.text.strip())
                if right:
                    row_data.append(right.text.strip())
                else:
                    row_data.append("NO DATA")

                if row_data:
                    details.append(row_data)

    except Exception as e:
        print("Getting fund details failed:", e)
        terminate_driver(driver)

    if not details:
        print("No fund details found")

    print(details)
    return details


# Get fund holdings
def get_fund_holdings(fund):
    holdings = [fund]

    try:
        driver.get(f"https://research2.fidelity.com/fidelity/screeners/etf/etfholdings.asp?symbol={fund}&view=Holdings")
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, 'results-table')))
        soup = BeautifulSoup(driver.page_source, 'html.parser')
        table = soup.find('table', class_='results-table sortable')

        if table:
            headers = [th.text.strip() for th in table.find('thead').find_all('th')]
            holdings.append(headers)

            for row in table.find('tbody').find_all('tr'):
                cols = row.find_all('td')
                data = [col.text.strip() for col in cols]
                holdings.append(data)
        else:
            print("Table not found in the HTML content")

    except Exception as e:
        print("Getting fund holdings failed:", e)
        terminate_driver(driver)

    print(holdings)
    return holdings
