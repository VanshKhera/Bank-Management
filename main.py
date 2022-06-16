from functions import *

#TODO
commands = [
    '1',
    '2',
    '3'
]

print("Bank Management System")

with open("help.txt", "r") as f:
    content = f.read()
    print(content)

user_input = input("\nPlease select an option between 1-10: ")

while user_input != '10':
    if user_input in commands:
        if user_input == "1":
            newAccount()
            break
        elif user_input == "2":
            pass
            break

    user_input = input("Please select an option between 1-10: ")

