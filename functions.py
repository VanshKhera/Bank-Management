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

