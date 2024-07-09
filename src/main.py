from auth import login


# Initialize project
def initialize():
    print(
        "Before running the program, make sure your Fidelity app is open if you have MFA on in order to accept the push"
        " notification.")

    username = input("Enter your username: ")
    password = input("Enter your password: ")

    print()

    login(username, password)

    # Modify functions you call here for what you want the program to do

    # example_func1()
    # example_func2()


initialize()
