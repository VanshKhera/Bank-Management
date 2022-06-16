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
        print(row)

    #TODO
    # if the user entered wrong details, want to display a message how trash they are at remembering things

    c.execute("SELECT balance FROM Customer WHERE account_no = ? AND account_pin = ?", (acc_no, acc_pin, ))
    a = c.fetchall()
    amount = int(input("Enter the amount to deposit: "))

    for b in a:
        e_bal = b[0] + amount

    c.execute("UPDATE Customer SET balance = ? WHERE account_no = ? AND account_pin = ? ", (e_bal, acc_no, acc_pin, ))

    connection.commit()
    connection.close()