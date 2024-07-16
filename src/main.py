# Run code here
# pip install -r requirements.txt

from auth import login
from funds import get_fund_details, get_fund_holdings, get_fund_performance, get_fund_profile
from user_portfolio import get_user_accounts, get_user_balances
from stocks import get_stock_details, get_stock_profile, get_stock_performance


# Initialize project
def initialize():
    print("Before running the program, make sure your phone is handy to verify the Fidelity push notification.")

    print()

    username = input("Enter your username: ")
    password = input("Enter your password: ")

    print()

    login(username, password)

    print()
    # Modify functions you call here for what you want the program to do

    # example_func1()
    # example_func2()
    print(get_user_balances())


initialize()
