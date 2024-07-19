# Basic data visualization

from user_portfolio import get_all_user_balances, get_all_user_positions, get_user_accounts


# Display user's Fidelity dashboard
def dashboard():
    accounts = get_user_accounts()
    balances = get_all_user_balances()
    user_positions = get_all_user_positions()
    num_accounts = len(balances)

    print("All accounts")

    print(balances[0])

    print()

    balance_tracker = 1
    account_tracker = 0
    while account_tracker < num_accounts - 1:

        accounts[account_tracker][0], accounts[account_tracker][1] = accounts[account_tracker][1], accounts[account_tracker][0]
        print(accounts[account_tracker])

        if balance_tracker == num_accounts:
            break
        else:
            print(balances[balance_tracker][1])
            balance_tracker += 1

        for j in range(len(user_positions[account_tracker][1])):
            print(user_positions[account_tracker][1][j])

        print()

        account_tracker += 1
