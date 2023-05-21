import mysql.connector

class Account:
    def __init__(self, account_number, balance, account_holder, pin):
        self.account_number = account_number
        self.balance = balance
        self.account_holder = account_holder
        self.pin = pin

    def withdraw(self, amount):
        if self.balance >= amount:
            self.balance -= amount
            return True
        else:
            return False

    def deposit(self, amount):
        self.balance += amount



class Bank:
    def __init__(self):
        self.db = mysql.connector.connect(
            host="localhost",
            user="user1",
            password="123456",
            database="atm_db"
        )
        self.cursor = self.db.cursor()
        self.create_table()

    def create_table(self):
        self.cursor.execute("CREATE TABLE IF NOT EXISTS accounts (account_number VARCHAR(20) PRIMARY KEY, balance FLOAT, account_holder VARCHAR(100), pin VARCHAR(4))")

    def add_account(self, account):
        sql = "INSERT INTO accounts (account_number, balance, account_holder,pin) VALUES (%s, %s, %s, %s)"
        values = (account.account_number, account.balance, account.account_holder, account.pin)
        self.cursor.execute(sql, values)
        self.db.commit()

    def authenticate(self, account_number, pin):
        sql = "SELECT * FROM accounts WHERE account_number = %s AND pin = %s"
        values = (account_number, pin)
        self.cursor.execute(sql, values)
        result = self.cursor.fetchone()
        if result:
            account = Account(result[0], result[1], result[2], result[3])
            if account.pin == pin:
                return account
            else:
                print(" *** Invalid PIN. Please try again. ***")
        return None
    

    def get_balance(self, account):
        return account.balance

    def withdraw(self, account, amount):
        if account.withdraw(amount):
            sql = "UPDATE accounts SET balance = %s WHERE account_number = %s"
            values = (account.balance, account.account_number)
            self.cursor.execute(sql, values)
            self.db.commit()
            return True
        else:
            return False

    def deposit(self, account, amount):
        account.deposit(amount)
        sql = "UPDATE accounts SET balance = %s WHERE account_number = %s"
        values = (account.balance, account.account_number)
        self.cursor.execute(sql, values)
        self.db.commit()
  
    def update_account(self, account):
        sql = "UPDATE accounts SET account_holder = %s, pin = %s WHERE account_number = %s"
        values = (account.account_holder, account.pin, account.account_number)
        self.cursor.execute(sql, values)
        self.db.commit()
        
    def lock_account(self, account):
        account.is_locked = True
        print(" *** Account locked due to multiple unsuccessful login attempts. \n Please contact the bank to unlock your account. ***")

        

class ATM:
    
    def __init__(self, bank):
        self.bank = bank

    
    def insert_card(self):
        while True:
            account_number = input("Enter your account number: ")
            pin = input("Enter your PIN: ")

            account = self.bank.authenticate(account_number, pin)
            if account:
                self.transaction_menu(account)
                break
            else:
                print(" *** Invalid card or PIN. Please try again. *** ")

    def transaction_menu(self, account):
        while True:
            print("1. Balance Inquiry")
            print("2. Withdrawal")
            print("3. Deposit")
            print("4. Update Account Information")
            print("5. Exit")
            choice = input("Enter your choice: ")

            if choice == "1":
                self.balance_inquiry(account)
            elif choice == "2":
                self.withdrawal(account)
            elif choice == "3":
                self.deposit(account)
            elif choice == "4":
                self.update_account_info(account)
            elif choice == "5":
                print(" *** Thanks for using our bank! ***")
                break
            else:
                print(" *** Invalid choice. Please try again. *** ")

    def balance_inquiry(self, account):
        balance = self.bank.get_balance(account)
        print(f" *** Your balance is:  {balance} ***")

    def withdrawal(self, account):
        amount = float(input("Enter the amount to withdraw: "))
        if self.bank.withdraw(account, amount):
            print(" *** Transaction successful. Please take your cash. ***")
        else:
            print(" *** Insufficient balance. *** ")

    def deposit(self, account):
        amount = float(input("Enter the amount to deposit: "))
        self.bank.deposit(account, amount)
        print(" *** Deposit successful. ***")
        

    def update_account_info(self, account):
        print(" *** Update Account Information ***")
        new_account_holder = input("Enter new account holder name: ")
        new_pin = input("Enter new PIN: ")

        updated_account = Account(
            account_number=account.account_number,
            balance=account.balance,
            account_holder=new_account_holder,
            pin=new_pin
        )

        self.bank.update_account(updated_account)

        print(" *** Account information updated successfully. ***")

        # Prompt the user to enter the account credentials again
        account_number = input("Enter your account number: ")
        pin = input("Enter your PIN: ")

        self.insert_card(account_number, pin)
        

    def insert_card(self, account_number, pin):
        account = self.bank.authenticate(account_number, pin)
        if account:
            if account.is_locked:
                return
            self.transaction_menu(account)
        else:
            print(" *** Invalid card or PIN. Please try again. *** ")

