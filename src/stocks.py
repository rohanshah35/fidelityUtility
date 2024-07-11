# Data utility for stocks

from webdriver import get_driver, terminate_driver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup

driver = get_driver()


def get_stock_profile(stock):
    return 0


def get_stock_performance(stock):
    return 0


def get_stock_details(stock):
    details = [stock]

    try:
        url = f"https://digital.fidelity.com/prgw/digital/research/quote/dashboard/summary?symbol={stock}"
        driver.get(url)
        WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.TAG_NAME, 'body')))
        print(stock)
        WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.CLASS_NAME, 'detailed-quote-body')))
        soup = BeautifulSoup(driver.page_source, 'html.parser')
        quote_body = soup.find('div', class_='detailed-quote-body')

        if quote_body:
            items = quote_body.find_all('div', class_=['item', 'item ng-star-inserted'])

            for i, item in enumerate(items, 1):
                if i == 5 or i == 3:
                    continue

                row_data = []
                left = item.find('div', class_='left')
                as_of_date = item.find('div', class_='as-of-date ng-star-inserted')
                right = item.find('div', class_=['right', 'right ng-star-inserted', 'right nre-green ng-star-inserted'])

                if left:
                    left_text = left.text.strip()
                    if "Estimated dividend rate/yield" in left_text:
                        left_text = "Estimated dividend rate/yield"
                    row_data.append(left_text)
                if as_of_date:
                    row_data.append(as_of_date.text.strip())
                if right:
                    right_text = right.text.strip()
                    if "Communication Services\n\n\n" in right_text:
                        right_text = "Communication Services"
                    if "Consumer Discretionary\n\n\n" in right_text:
                        right_text = "Consumer Discretionary"
                    if "Consumer Staples\n\n\n" in right_text:
                        right_text = "Consumer Staples"
                    if "Energy \n\n\n" in right_text:
                        right_text = "Energy"
                    if "Financials\n\n\n" in right_text:
                        right_text = "Financials"
                    if "Health Care \n\n\n" in right_text:
                        right_text = "Health Care"
                    if "Industrials\n\n\n" in right_text:
                        right_text = "Industrials"
                    if "Information Technology\n\n\n" in right_text:
                        right_text = "Information Technology"
                    if "Materials\n\n\n" in right_text:
                        right_text = "Materials"
                    if "Real Estate\n\n\n" in right_text:
                        right_text = "Real Estate"
                    if "Utilities\n\n\n" in right_text:
                        right_text = "Utilities"
                    row_data.append(right_text)
                else:
                    row_data.append("NO DATA")

                if row_data:
                    details.append(row_data)
                    # Print row
                    print(f"{row_data}")

    except Exception as e:
        print("Getting stock details failed:", e)
        terminate_driver(driver)

    if not details:
        print("No stock details found")

    return details
