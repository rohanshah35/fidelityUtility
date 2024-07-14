# Data utility for funds

from webdriver import get_driver, terminate_driver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup

driver = get_driver()


# Get fund profile
def get_fund_profile(fund):
    profile = [fund]

    try:
        url = f"https://digital.fidelity.com/prgw/digital/research/quote/dashboard/summary?symbol={fund}"
        driver.get(url)
        WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.TAG_NAME, 'body')))
        WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.CLASS_NAME, 'profile-card-item')))

        WebDriverWait(driver, 30).until(EC.element_to_be_clickable((By.CLASS_NAME, "stated-objectives-modal-link"))).click()
        soup = BeautifulSoup(driver.page_source, 'html.parser')
        modal_content = soup.find('div', {'class': 'f2-app-dialog stated-objectives-modal'})
        if modal_content:
            objective_text = modal_content.find('div', {'class': 'body'}).find('p')
            if objective_text:
                profile.append(objective_text.text.strip())
        WebDriverWait(driver, 30).until(EC.element_to_be_clickable((By.CLASS_NAME, "f2-dialog-close"))).click()

        soup = BeautifulSoup(driver.page_source, 'html.parser')

        # Currently not working
        # holdings = soup.find('div', class_='profile-card-item profile-holdings')
        # if holdings:
        #     items = holdings.find_all('li')
        #     for item in items:
        #         name = item.find('h3').text.strip() if item.find('h3') else ''
        #         value = item.find('span').text.strip() if item.find('span') else ''
        #         profile.append([name, value])

        structure = soup.find('div', class_='profile-card-item profile-structure')
        if structure:
            table = structure.find('table')
            if table:
                rows = table.find_all('tr')
                for row in rows:
                    name = row.find('th').text.strip() if row.find('th') else ''
                    value = row.find('td').text.strip() if row.find('td') else ''
                    profile.append([name, value])
            else:
                print("No table found in structure")

    except Exception as e:
        print(f"Getting fund profile failed:", e)

    print(profile)
    return profile


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
            performance.append(" ")

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
                    row_data.append(" ")

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
