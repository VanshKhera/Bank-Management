import sqlite3
import os
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
                account_no integer, 
                pin integer
            )   
            """)
'''
def newAccount():
    print("\nNew Account\t\n")
    print("Please enter the following information:\n")
    first_name = input("First Name: ")
    last_name = input("Last Name: ")
    email = input("Email: ")
    account_number = input("Account Number: ")
    account_pin = input("Account Pin: ")

    details = (first_name, last_name, email, account_number,account_pin)

    try:
        c.execute("INSERT INTO Customer VALUES (?, ?, ?, ?, ?)", details)
    except:
        print("Please select a different account number and try again")
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
        print("Minimum amount for a transaction is ₹1.0")
        exit(1)

    print("\n****ENTER 'TO' A/C DETAILS****")
    to_acc_no = int(input("Enter account number: "))

    permission = input(f"Are you sure, you want to transfer ₹{amount} from A/C no. {acc_no} to A/C no. {to_acc_no} (y/n)?\n")
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
        print(f"₹{amount} transferred from A/C no. {acc_no} to A/C no. {to_acc_no}")
        print("----------------------------------------------------------------------")

        connection.commit()
        connection.close()
        exit(0)
    exit(1)