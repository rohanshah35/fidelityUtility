# Scripts for statistics
# Note: all data gleaned from these scripts are rough estimates within the 52-week window due to lack of historical data
# If you do add code here, make sure to process the data first

import math
import re

from user_portfolio import get_all_user_positions, get_user_account_positions
from webdriver import get_driver

driver = get_driver()


# Prepares all account balance data for scripts
def process_total_balances(balances):

    for item in balances:
        if isinstance(item, list):
            for sub_item in item:
                if isinstance(sub_item, list):
                    value = sub_item[1]
                    if isinstance(value, str):
                        value = value.replace('$', '').replace(',', '').replace('%', '')
                        if value.lower() == 'no change':
                            value = '0'
                        try:
                            sub_item[1] = float(value)
                        except ValueError:
                            sub_item[1] = value
                elif isinstance(sub_item, str):
                    for account_detail in item[1:]:
                        if isinstance(account_detail, list):
                            for detail in account_detail:
                                value = detail[1]
                                if isinstance(value, str):
                                    value = value.replace('$', '').replace(',', '').replace('%', '')
                                    if value.lower() == 'no change':
                                        value = '0'
                                    try:
                                        detail[1] = float(value)
                                    except ValueError:
                                        detail[1] = value

    return balances


# Prepares account balance data for scripts
def process_account_balances(balances):
    processed_accounts = []
    account_id = balances[0]
    sub_categories = balances[1]

    processed_sub_categories = []
    for sub_category in sub_categories:
        sub_category_name = sub_category[0]
        sub_category_value = sub_category[1]

        cleaned_value = re.sub(r'[^\d.-]', '', sub_category_value)
        double_value = float(cleaned_value)

        processed_sub_categories.append([sub_category_name, double_value])

    processed_accounts.append([account_id, processed_sub_categories])

    return processed_accounts


# Prepares all account position data for scripts
# Warning:
# 52-week ranges are strings, make sure to use 'convert_range()' on '['52-Week Range', 'A-B']' to avoid errors
def process_total_positions(positions):

    for account in positions:
        if isinstance(account, list) and len(account) > 1:
            holdings = account[1]
            for holding in holdings:
                if isinstance(holding, list) and len(holding) > 2:
                    stats = holding[2]
                    for stat in stats:
                        if isinstance(stat, list) and len(stat) > 1:
                            value = stat[1]
                            if isinstance(value, str):
                                value = value.replace('$', '').replace(',', '').replace('%', '').replace('/ Share', '')
                                if value.lower() == 'no change':
                                    value = '0'
                                try:
                                    stat[1] = float(value)
                                except ValueError:
                                    stat[1] = value

    return positions


# Prepares account position data for scripts
# Warning:
# 52-week ranges are strings, make sure to use 'convert_range()' on '['52-Week Range', 'A-B']' to avoid errors
def process_account_positions(positions):
    holdings = positions[1]

    for holding in holdings:
        if isinstance(holding, list) and len(holding) > 2:
            stats = holding[2]
            for stat in stats:
                if isinstance(stat, list) and len(stat) > 1:
                    value = stat[1]
                    if isinstance(value, str):
                        if stat[0] == '52-Week Range':
                            stat[1] = value.replace('$', '')
                        else:
                            value = value.replace('$', '').replace(',', '').replace('%', '').replace('/ Share', '')
                            if value.lower() == 'no change':
                                value = '0'
                            try:
                                stat[1] = float(value)
                            except ValueError:
                                stat[1] = value

    return positions


# Convert range into digestible data types
def convert_range(range):
    low, high = range[1].split('-')
    low = float(low)
    high = float(high)

    return low, high


# Total portfolio standard deviation (52 wks)
def total_standard_deviation():
    data = process_total_positions(get_all_user_positions())

    def calculate_volatility(low, high):
        return (high - low) / ((high + low) / 2)

    def extract_52_week_range(holding_data):
        for item in holding_data:
            if item[0] == '52-Week Range':
                low, high = convert_range(item)
                return low, high
        return None, None

    def extract_current_value(holding_data):
        for item in holding_data:
            if item[0] == 'Current Value':
                return item[1]
        return 0

    total_portfolio_value = 0
    volatilities = []

    for account in data:
        for holding in account[1]:
            if len(holding) > 2:
                holding_data = holding[2]
                low, high = extract_52_week_range(holding_data)
                current_value = extract_current_value(holding_data)

                if low is not None and high is not None:
                    volatility = calculate_volatility(low, high)
                    volatilities.append((volatility, current_value))
                    total_portfolio_value += current_value

    weighted_avg_volatility = sum(v * (cv / total_portfolio_value) for v, cv in volatilities)

    variance = sum((v - weighted_avg_volatility)**2 * (cv / total_portfolio_value) for v, cv in volatilities)

    std_dev = math.sqrt(variance)

    return std_dev


# Account standard deviation (52 wks)
def account_standard_deviation(account_number):
    data = process_account_positions(get_user_account_positions(account_number))

    for i in range(len(data)):
        if data[i][0] == account_number:
            data = data[i]

    def calculate_volatility(low, high):
        return (high - low) / ((high + low) / 2)

    def extract_52_week_range(holding_data):
        for item in holding_data:
            if item[0] == '52-Week Range':
                low, high = convert_range(item)
                return low, high
        return None, None

    def extract_weight(holding_data):
        for item in holding_data:
            if item[0] == '% of Account':
                return item[1] / 100
        return None

    def extract_current_value(holding_data):
        for item in holding_data:
            if item[0] == 'Current Value':
                return item[1]
        return 0

    total_account_value = 0
    weighted_volatilities = []

    for holding in data[1]:
        if len(holding) > 2:
            holding_data = holding[2]
            low, high = extract_52_week_range(holding_data)
            weight = extract_weight(holding_data)
            current_value = extract_current_value(holding_data)

            if low is not None and high is not None and weight is not None:
                volatility = calculate_volatility(low, high)
                weighted_volatilities.append((volatility, weight, current_value))
                total_account_value += current_value

    weighted_avg_volatility = sum(v * (w * cv / total_account_value) for v, w, cv in weighted_volatilities)

    variance = sum((v - weighted_avg_volatility)**2 * (w * cv / total_account_value) for v, w, cv in weighted_volatilities)

    std_dev = math.sqrt(variance)

    return std_dev


# Total portfolio beta (52 wks)
# Make sure the market benchmarks you input are 52-week ranges
def total_beta(market_high, market_low):
    data = process_total_positions(get_all_user_positions())

    def calculate_volatility(low, high):
        return (high - low) / ((high + low) / 2)

    def extract_52_week_range(holding_data):
        for item in holding_data:
            if item[0] == '52-Week Range':
                low, high = convert_range(item)
                return low, high
        return None, None

    def extract_current_value(holding_data):
        for item in holding_data:
            if item[0] == 'Current Value':
                return item[1]
        return 0

    total_portfolio_value = 0
    weighted_volatilities = []

    for account in data:
        for holding in account[1]:
            if len(holding) > 2:
                holding_data = holding[2]
                low, high = extract_52_week_range(holding_data)
                current_value = extract_current_value(holding_data)

                if low is not None and high is not None:
                    volatility = calculate_volatility(low, high)
                    weighted_volatilities.append((volatility, current_value))
                    total_portfolio_value += current_value

    portfolio_volatility = sum(v * (cv / total_portfolio_value) for v, cv in weighted_volatilities)

    market_volatility = calculate_volatility(market_low, market_high)

    estimated_correlation = 0.6

    portfolio_beta = (portfolio_volatility / market_volatility) * estimated_correlation

    return portfolio_beta


# Account beta (52 wks)
# Make sure the market benchmarks you input are 52-week ranges
def account_beta(account_number, market_high, market_low):
    data = process_account_positions(get_user_account_positions(account_number))

    def calculate_volatility(low, high):
        return (high - low) / ((high + low) / 2)

    def extract_52_week_range(holding_data):
        for item in holding_data:
            if item[0] == '52-Week Range':
                low, high = convert_range(item)
                return low, high
        return None, None

    def extract_current_value(holding_data):
        for item in holding_data:
            if item[0] == 'Current Value':
                return item[1]
        return 0

    total_account_value = 0
    weighted_volatilities = []

    for holding in data[1]:
        if len(holding) > 2:
            holding_data = holding[2]
            low, high = extract_52_week_range(holding_data)
            current_value = extract_current_value(holding_data)

            if low is not None and high is not None:
                volatility = calculate_volatility(low, high)
                weighted_volatilities.append((volatility, current_value))
                total_account_value += current_value

    account_volatility = sum(v * (cv / total_account_value) for v, cv in weighted_volatilities)

    market_volatility = calculate_volatility(market_low, market_high)

    estimated_correlation = 0.6

    account_beta = (account_volatility / market_volatility) * estimated_correlation

    return account_beta


# Total portfolio Sharpe ratio (52 wks)
# Risk free rate should be in the same time frame as returns
def total_sharpe_ratio(risk_free_rate):
    data = process_total_positions(get_all_user_positions())

    def calculate_return(holding_data):
        for item in holding_data:
            if item[0] == 'Last Price':
                current_price = item[1]
            elif item[0] == 'Cost Basis Total':
                cost_basis = item[1]
        return (current_price - cost_basis) / cost_basis

    total_portfolio_value = 0
    holdings = []

    for account in data:
        for holding in account[1]:
            if len(holding) > 2:
                holding_data = holding[2]
                holding_value = [item[1] for item in holding_data if item[0] == 'Current Value'][0]
                total_portfolio_value += holding_value
                holdings.append((holding_data, holding_value))

    weighted_returns = 0
    for holding_data, holding_value in holdings:
        holding_return = calculate_return(holding_data)
        weighted_returns += holding_return * (holding_value / total_portfolio_value)

    portfolio_return = weighted_returns

    portfolio_stdev = total_standard_deviation()

    sharpe = (portfolio_return - risk_free_rate) / portfolio_stdev

    return sharpe


# Account Sharpe ratio (52 wks)
# Risk free rate should be in the same time frame as returns
def account_sharpe_ratio(account_number, risk_free_rate):
    data = process_account_positions(get_user_account_positions(account_number))

    def calculate_return(holding_data):
        for item in holding_data:
            if item[0] == 'Last Price':
                current_price = item[1]
            elif item[0] == 'Cost Basis Total':
                cost_basis = item[1]
        return (current_price - cost_basis) / cost_basis

    def extract_current_value(holding_data):
        for item in holding_data:
            if item[0] == 'Current Value':
                return item[1]
        return 0

    total_account_value = 0
    weighted_returns = 0
    weighted_squared_returns = 0

    for holding in data[1]:
        if len(holding) > 2:
            holding_data = holding[2]
            holding_return = calculate_return(holding_data)
            current_value = extract_current_value(holding_data)

            total_account_value += current_value
            weighted_returns += holding_return * (current_value / total_account_value)
            weighted_squared_returns += (holding_return ** 2) * (current_value / total_account_value)

    account_return = weighted_returns

    std_dev = account_standard_deviation(account_number)

    sharpe_ratio = (account_return - risk_free_rate) / std_dev if std_dev != 0 else 0

    return sharpe_ratio