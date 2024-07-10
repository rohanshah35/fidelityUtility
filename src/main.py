# pip install -r requirements.txt

from auth import login
from funds import get_fund_holdings


# Initialize project
def initialize():
    print("Before running the program, make sure your phone is handy to verify the Fidelity push notification.")

    username = input("Enter your username: ")
    password = input("Enter your password: ")

    print()

    login(username, password)

    print()
    # Modify functions you call here for what you want the program to do

    # example_func1()
    # example_func2()
    get_fund_holdings('VOO')


initialize()
