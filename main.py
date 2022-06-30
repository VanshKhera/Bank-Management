from functions import *
from rich.console import Console
from rich.markdown import Markdown

commands = [
    '1',
    '2',
    '3',
    '4',
    '5',
    '6',
]

# Pretty design
MARKDOWN = '''
# Bank Management System
'''

console = Console()
md = Markdown(MARKDOWN)
clearTerminal()
console.print(md)
console.print("Main Menu\n", style="bold underline green")

with open("help.txt", "r") as f:
    content = f.read()
    console.print(content)

user_input = input("\nPlease select an option between 1-5: ")

while user_input != '5':
    if user_input in commands:
        if user_input == "1":
            newAccount()
            break
        elif user_input == "2":
            depositMoney()
            break
        elif user_input == "3":
            withdrawMoney()
            break
        elif user_input == "4":
            transferMoney()
            break
        elif user_input == '5':
            calculateLoan()
            break
    user_input = input("Please select an option between 1-10: ")

