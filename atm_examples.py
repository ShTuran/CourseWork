# adding account

from atm import Account, Bank

bank = Bank()

account_number = input("Enter the account number: ")
balance = float(input("Enter the initial balance: "))
account_holder = input("Enter the account holder's name: ")
account_pin = input ("Enter the account pin: ")

account = Account(account_number, balance, account_holder, account_pin)

bank.add_account(account)

print("Successfully added account") 


