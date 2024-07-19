# Scripts for statistics
from user_portfolio import get_all_user_positions
from webdriver import get_driver
import math

driver = get_driver()


# Prepares balance data for scripts
def process_balances(balances):

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


# Prepares position data for scripts
# Warning:
# 52-week ranges are strings, make sure to use 'convert_range()' on '['52-Week Range', 'A-B']' to avoid errors
def process_positions(positions):

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


# Convert range into digestible data types
def convert_range(range):
    low, high = range[1].split('-')
    low = float(low)
    high = float(high)

    return low, high


# Portfolio standard deviation (52 wks)
def standard_deviation():
    data = process_positions(get_all_user_positions())

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

    total_portfolio_value = 0
    weighted_volatilities = []

    for account in data:
        for holding in account[1]:
            if len(holding) > 2:
                holding_data = holding[2]
                low, high = extract_52_week_range(holding_data)
                weight = extract_weight(holding_data)
                current_value = extract_current_value(holding_data)

                if low is not None and high is not None and weight is not None:
                    volatility = calculate_volatility(low, high)
                    weighted_volatilities.append((volatility, weight, current_value))
                    total_portfolio_value += current_value

    weighted_avg_volatility = sum(v * (w * cv / total_portfolio_value) for v, w, cv in weighted_volatilities)

    return weighted_avg_volatility


# Portfolio beta (52 wks)
# Make sure the market benchmarks you input are 52-week ranges
def beta(market_low, market_high):
    data = process_positions(get_all_user_positions())

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


# Portfolio Sharpe ratio (52 wks)
# Risk free rate should be in the same time frame as returns
def sharpe_ratio(risk_free_rate):
    data = process_positions(get_all_user_positions())

    sharpe = 0

    return sharpe


# Scans portfolio (funds + stocks), gives you dollar amount of each major stock you own (>$100)
def stock_dollar_volume():
    return 0

