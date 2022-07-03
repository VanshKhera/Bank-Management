import sqlite3
import os
from rich.console import Console
from rich.markdown import Markdown
from rich.theme import Theme
from rich.table import Table

custom_theme = Theme({"success": "green", "error": "bold red"})

console = Console(theme=custom_theme)

# function to clear the terminal
def clearTerminal():
    os.system('cls')

# making sure that the input isn't empty
def strCheck(arg, err_msg):
    if len(str(arg)) == 0:
        console.print(f"'{err_msg}' can't be empty!", style="error")
        exit(1)

# For fields like first_name and last_name making sure that they dont contain numbers, because no one has numbers in their name- or maybe they do, anyway who cares
def has_numbers(inputString):
    condition = any(char.isdigit() for char in inputString)
    if condition:
        console.print("Cannot contain numbers!", style="error")
        exit(1)

# Connecting Database with Python
connection = sqlite3.connect("database.db")
c = connection.cursor()

# Creating Table
'''
c.execute("""
            CREATE TABLE Customer(
                first_name text,  
                last_name text,
                email text,
                account_no integer UNIQUE, 
                pin integer,
                balance real DEFAULT 0.0
            )   
            """)
'''

MARKDOWN = '''
# Bank Management System
'''
md = Markdown(MARKDOWN)

def newAccount():
    clearTerminal()
    console.print(md)
    console.print("New Account\n", style="bold underline green")

    print("Please enter the following information:\n")

    first_name = input("First Name: ")
    strCheck(first_name, "First name")
    has_numbers(first_name)

    last_name = input("Last Name: ")
    strCheck(last_name, "Last name")
    has_numbers(first_name)

    email = input("Email: ")
    strCheck(email, "Email")

    try:
        account_number = int(input("Account Number: "))
        strCheck(account_number, "Account Number")
    except ValueError:
        console.print("Account Number can only be an integer!", style="error")
        exit(1)

    try:
        account_pin = int(input("Account Pin: "))
        strCheck(account_pin, "Account Pin")
    except ValueError:
        console.print("Account Number can only be an integer!", style="error")
        exit(1)

    details = (first_name, last_name, email, account_number,account_pin, 0.0)
    try:
        c.execute("INSERT INTO Customer VALUES (?, ?, ?, ?, ?, ?)", details)
    # If the account number isn't unique
    except sqlite3.IntegrityError as err:
        console.print("This account no. already exists, Please try again with a different account number!", style="error")
        exit(1)
    connection.commit()
    connection.close()
    console.print("\nAccount created successfully!", style="success")

def depositMoney():
    clearTerminal()
    console.print(md)
    console.print("Deposit Money\n", style="bold underline green")

    try:
        acc_no = int(input("Enter your account number: "))
    except ValueError:
        console.print("Account Number can only be an integer!", style="error")
        exit(1)
    try:
        acc_pin = int(input("Enter your pin: "))
    except ValueError:
        console.print("Account Pin can only be an integer!", style="error")
        exit(1)
    c.execute("SELECT * FROM Customer WHERE account_no = ? AND account_pin = ?", (acc_no, acc_pin,))
    rows = c.fetchall()

    if rows == []:
        console.print("Account doesnt exist!", style="error")
        exit(1)

    for row in rows:
        name = str(row[0] + " " + row[1])
        email = str(row[2])
        account_no = str(row[3])
        balance = str(row[5])

        table = Table(title="Account details")

        table.add_column("Name", style="cyan")
        table.add_column("Email", style="red")
        table.add_column("Account No.", style="blue")
        table.add_column("Balance", style="yellow")

        table.add_row(name, email, account_no, balance)
        console.print(table)

    try:
        amount = float(input("Enter the amount to deposit: "))
    except ValueError:
        console.print("Amount can only be an integer!", style="error")
        exit(1)

    for b in rows:
        e_bal = b[5] + amount

    c.execute("UPDATE Customer SET balance = ? WHERE account_no = ? AND account_pin = ? ", (e_bal, acc_no, acc_pin,))
    console.print(f"\nCurrent Balance: {e_bal}", style="success")

    connection.commit()
    connection.close()


def withdrawMoney():
    clearTerminal()
    console.print(md)
    console.print("Withdraw Money\n", style="bold underline green")
    try:
        acc_no = int(input("Enter your account number: "))
    except ValueError:
        console.print("Account Number can only be an integer!", style="error")
        exit(1)
    try:
        acc_pin = int(input("Enter your pin: "))
    except ValueError:
        console.print("Account Pin can only be an integer!", style="error")
        exit(1)

    c.execute("SELECT * FROM Customer WHERE account_no = ? AND account_pin = ?", (acc_no, acc_pin,))
    rows = c.fetchall()

    if rows == []:
        console.print("Account doesnt exist!", style="error")
        exit(1)

    for row in rows:
        name = str(row[0] + " " + row[1])
        email = str(row[2])
        account_no = str(row[3])
        balance = str(row[5])

        table = Table(title="Account details")

        table.add_column("Name", style="cyan")
        table.add_column("Email", style="red")
        table.add_column("Account No.", style="blue")
        table.add_column("Balance", style="yellow")

        table.add_row(name, email, account_no, balance)
        console.print(table)

    c.execute("SELECT balance FROM Customer WHERE account_no = ? AND account_pin = ?", (acc_no, acc_pin,))
    a = c.fetchall()
    try:
        amount = float(input("Enter the amount to withdraw: "))
    except ValueError:
        console.print("Amount can only be an integer!", style="error")
        exit(1)

    for b in a:
        e_bal = b[0] - amount

    c.execute("UPDATE Customer SET balance = ? WHERE account_no = ? AND account_pin = ? ", (e_bal, acc_no, acc_pin,))
    console.print(f"\nRemaining Balance: {e_bal}", style="success")

    connection.commit()
    connection.close()

def transferMoney():
    clearTerminal()
    console.print(md)
    console.print("Transfer Money\n", style="bold underline green")

    console.print("ENTER 'FROM' A/C DETAILS", style="cyan")

    try:
        acc_no = int(input("Enter your account number: "))
    except ValueError:
        console.print("Amount can only be an integer!", style="error")
        exit(1)
    try:
        acc_pin = int(input("Enter your pin: "))
    except ValueError:
        console.print("Amount can only be an integer!", style="error")
        exit(1)

    c.execute("SELECT * FROM Customer WHERE account_no = ? AND account_pin = ?", (acc_no, acc_pin,))
    rows = c.fetchall()

    if rows == []:
        console.print("Account doesnt exist!", style="error")
        exit(1)

    for row in rows:
        name = str(row[0] + " " + row[1])
        email = str(row[2])
        account_no = str(row[3])
        balance = str(row[5])

        table = Table(title="Account details")

        table.add_column("Name", style="cyan")
        table.add_column("Email", style="red")
        table.add_column("Account No.", style="blue")
        table.add_column("Balance", style="yellow")

        table.add_row(name, email, account_no, balance)
        console.print(table)

    c.execute("SELECT balance FROM Customer WHERE account_no = ? AND account_pin = ?", (acc_no, acc_pin,))
    a = c.fetchall()

    try:
        amount = float(input("Enter the amount to transfer: "))
    except ValueError:
        console.print("Amount can only be an integer!", style="error")
        exit(1)

    if amount < 1:
        console.print("Minimum amount for a transaction is $1.0", style="error")
        exit(1)

    console.print("\nENTER 'TO' A/C DETAILS", style="cyan")
    try:
        to_acc_no = int(input("Enter account number: "))
    except ValueError:
        console.print("Account number can only be an integer!", style="error")
        exit(1)

    # checking if the account exists or not
    c.execute("SELECT account_no FROM Customer WHERE account_no == ?", (to_acc_no, ))
    z = c.fetchall()

    if z == []:
        console.print("Account doesnt exist!", style="error")
        exit(1)

    permission = input(f"Are you sure, you want to transfer ${amount} from A/C no. {acc_no} to A/C no. {to_acc_no} (y/n)?\n")
    if permission == 'y' or permission == 'Y':

        # deducting money
        for b in a:
            altered_amount = b[0] - amount
        c.execute("UPDATE Customer SET balance = ? WHERE account_no = ? AND account_pin = ? ", (altered_amount, acc_no, acc_pin,))

        # crediting money
        # fetching balance
        c.execute("SELECT balance FROM Customer WHERE account_no = ?", (to_acc_no, ))
        to_bal = c.fetchall()

        # adding money
        for x in to_bal:
            crediting_amount = x[0] + amount

        c.execute("UPDATE Customer SET balance = ? WHERE account_no = ?", (crediting_amount, to_acc_no, ))

        print("----------------------------------------------------------------------")
        console.print("TRANSACTION SUCCESSFUL\n", style="success")
        print(f"${amount} transferred from A/C no. {acc_no} to A/C no. {to_acc_no}")
        print("----------------------------------------------------------------------")

        connection.commit()
        connection.close()
        exit(0)
    exit(1)

def calculateLoan():
    print("LOAN CALCULATOR")
    print('''
    Calculate for:
    1) Interest
    2) Principle
    3) Rate
    4) Time (per year)
    ''')
    choice = input("Select an option: ")
    if choice in ['1', '2', '3', '4',]:
        if choice == '1':
            P = float(input("Enter the principle/base amount: "))
            R = float(input("Enter the Rate per year: "))
            T = float(input("Enter the time in years: "))

            SI = (P*R*T)/100

            print(f"\nYou'll have to pay ${SI} extra as interest in {T} year(s)\n${SI + P} in total")

        if choice == '2':
            I = float(input("Enter the Interest per year: "))
            R = float(input("Enter the Rate per year: "))
            T = float(input("Enter the time in years: "))

            r = R/100
            P = I / (r*T)

            print("\nPrinciple/Base Amount: $%.2f" % round(P, 2))

        if choice == '3':
            P = float(input("Enter the principle/base amount: "))
            I = float(input("Enter the Interest per year: "))
            T = float(input("Enter the time in years: "))

            r = I / (P * T)
            R = r * 100

            print(f"\nRate on Principal: ${P}, Interest: ${I}, Time: {T} year(s), is {R}% PER YEAR")

        if choice == '4':
            P = float(input("Enter the principle/base amount: "))
            I = float(input("Enter the Interest per year: "))
            R = float(input("Enter the Rate per year: "))

            r = R/100
            T = I / (P * r)

            print(f"\nTime: {T} year(s) about {round(T)} year(s)")