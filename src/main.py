# pip install -r requirements.txt

# Currently available functionality
#
# dashboard:
# dashboard()
#
# funds:
# get_fund_profile(fund)
# get_fund_holdings(fund)
# get_fund_performance(fund)
# get_fund_details(fund)
#
# stocks:
# get_stock_details(stock)
# get_stock_profile(stock)
# get_stock_performance(stock)
#
# user portfolio:
# get_user_accounts()
# get_all_user_balances()
# get_all_user_positions()
# get_user_account_balance(account_number)
# get_user_account_positions(account_number)
#
# stats:
# total_standard_deviation()
# account_standard_deviation()
# total_beta()
# account_beta()
# total_sharpe_ratio()
# account_sharpe_ratio()


from auth import login
from dashboard import dashboard

import user_portfolio
import funds
import stocks
import stats


# Initialize project
def initialize():
    print("Before running the program, make sure your phone is handy to verify the Fidelity push notification.")

    print()

    username = input("Enter your username: ")
    password = input("Enter your password: ")

    print()

    login(username, password)

    print()

    # The program does not run headless currently due to Fidelity bot detection
    # Modify functions you call here for what you want the program to do

    dashboard()


initialize()
