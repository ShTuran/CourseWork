# authenticate account
# transaction menu - update feature and many more.


from atm import ATM, Bank

MAX_LOGIN_ATTEMPTS = 3

bank = Bank()

login_attempts = 0
authenticated_account = None

while login_attempts < MAX_LOGIN_ATTEMPTS:
    account_number = input("Enter your account number: ")
    pin = input("Enter your PIN: ")

    authenticated_account = bank.authenticate(account_number, pin)

    if authenticated_account:
        print("Authentication successful.")
        atm = ATM(bank)
        atm.transaction_menu(authenticated_account)
        break
    else:
        login_attempts += 1
        print("Authentication failed. Please try again.")

if login_attempts == MAX_LOGIN_ATTEMPTS:
    print("Maximum login attempts exceeded. Your account has been blocked. Please contact the bank.")




