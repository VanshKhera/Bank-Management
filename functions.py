import sqlite3
import os

# function to clear the terminal
def clearTerminal():
    os.system('cls')

def asterisks(str):
    # TODO: soon going to center align the whole text :)
    print("***********************************************************************************")
    print(str)
    print("***********************************************************************************")

def strCheck(arg, err_msg):
    if len(arg) == 0:
        print(f"'{err_msg}' can't be empty!")
        exit(1)

# Connecting Database with Python
connection = sqlite3.connect("database.db")
c = connection.cursor()

# Creating Tables
# Sqlite3 datatypes: null, integer, real (float), text, blob (.png, .jpg, .mp3, .mp4, etc.)
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

def newAccount():
    clearTerminal()
    asterisks("New Account")

    print("Please enter the following information:\n")

    first_name = input("First Name: ")
    strCheck(first_name, "First name")

    last_name = input("Last Name: ")
    strCheck(last_name, "Last name")

    email = input("Email: ")
    strCheck(email, "Email")

    account_number = input("Account Number: ")
    strCheck(account_number, "Account Number")

    account_pin = input("Account Pin: ")
    strCheck(account_pin, "Account Pin")

    details = (first_name, last_name, email, account_number,account_pin, 0.0)
    try:
        c.execute("INSERT INTO Customer VALUES (?, ?, ?, ?, ?, ?)", details)
    except sqlite3.IntegrityError as err:
        asterisks("This account no. already exists, Please try again with a different account number!")
        exit(1)
    connection.commit()
    connection.close()
    print("\nAccount created successfully!")

def depositMoney():
    acc_no = int(input("Enter your account number: "))
    acc_pin = int(input("Enter your pin: "))

    c.execute("SELECT * FROM Customer WHERE account_no = ? AND account_pin = ?", (acc_no, acc_pin, ))
    rows = c.fetchall()
    for row in rows:
        print(f'''
    Name: {row[0]} {row[1]}
    Email: {row[2]}
    Account No. {row[3]}
    Balance: {row[5]} 
            ''')

    #TODO
    # if the user entered wrong details, want to display a message how trash they are at remembering things

    c.execute("SELECT balance FROM Customer WHERE account_no = ? AND account_pin = ?", (acc_no, acc_pin, ))
    a = c.fetchall()
    amount = float(input("Enter the amount to deposit: "))

    for b in a:
        e_bal = b[0] + amount

    c.execute("UPDATE Customer SET balance = ? WHERE account_no = ? AND account_pin = ? ", (e_bal, acc_no, acc_pin, ))
    print(f"\nCurrent Balance: {e_bal}")

    connection.commit()
    connection.close()

def withdrawMoney():
    acc_no = int(input("Enter your account number: "))
    acc_pin = int(input("Enter your pin: "))

    c.execute("SELECT * FROM Customer WHERE account_no = ? AND account_pin = ?", (acc_no, acc_pin,))
    rows = c.fetchall()
    for row in rows:
        print(f'''
    Name: {row[0]} {row[1]}
    Email: {row[2]}
    Account No. {row[3]}
    Balance: {row[5]} 
            ''')
    # TODO
    # exception for wrong details

    c.execute("SELECT balance FROM Customer WHERE account_no = ? AND account_pin = ?", (acc_no, acc_pin,))
    a = c.fetchall()
    amount = float(input("Enter the amount to withdraw: "))

    for b in a:
        e_bal = b[0] - amount

    c.execute("UPDATE Customer SET balance = ? WHERE account_no = ? AND account_pin = ? ", (e_bal, acc_no, acc_pin,))
    print(f"\nRemaining Balance: {e_bal}")

    connection.commit()
    connection.close()

def transferMoney():
    print("\nTRANSFER MONEY")
    print("\n****ENTER 'FROM' A/C DETAILS****")

    acc_no = float(input("Enter your account number: "))
    acc_pin = (input("Enter your pin: "))

    c.execute("SELECT * FROM Customer WHERE account_no = ? AND account_pin = ?", (acc_no, acc_pin,))
    rows = c.fetchall()
    for row in rows:
        print(f'''
    Name: {row[0]} {row[1]}
    Email: {row[2]}
    Account No. {row[3]}
    Balance: {row[5]} 
                ''')

    # TODO
    # exception for wrong details

    c.execute("SELECT balance FROM Customer WHERE account_no = ? AND account_pin = ?", (acc_no, acc_pin,))
    a = c.fetchall()

    amount = float(input("Enter the amount to transfer: "))
    if amount < 1:
        print("Minimum amount for a transaction is $1.0")
        exit(1)

    print("\n****ENTER 'TO' A/C DETAILS****")
    to_acc_no = int(input("Enter account number: "))

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
        print("TRANSACTION SUCCESSFUL\n")
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