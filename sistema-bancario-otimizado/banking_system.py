import textwrap


def menu():  
    menu = """\n
    ================ MENU ================
    [d]\tDeposit
    [w]\tWithdraw
    [s]\tStatement
    [nc]\tNew account
    [nu]\tNew user
    [lc]\tList accounts
    [q]\tQuit
    => """
    return input(textwrap.dedent(menu))


def deposit(balance, value, statement, /):
    if value > 0:
        balance += value
        statement += f"Deposit: $ {value:.2f}\n"
        print("\n=== Deposit successful! ===")
    else:
        print("Operation failed! The specified value is invalid.")
    
    return balance, statement


def withdraw(*, balance, value, statement, limit, num_withdrawals, withdrawal_limit):
    exceeded_balance = value > balance
    exceeded_limit = value > limit
    exceeded_withdrawals = num_withdrawals >= withdrawal_limit

    if exceeded_balance:
        print("\nOperation failed! You do not have enough balance.")

    elif exceeded_limit:
        print("\nOperation failed! The withdrawal amount exceeds the limit.")

    elif exceeded_withdrawals:
        print("\nOperation failed! Maximum number of withdrawals exceeded.")

    elif value > 0:
        balance -= value
        statement += f"Withdrawal: $ {value:.2f}\n"
        num_withdrawals += 1
        print("\n=== Withdrawal successful! ===")

    else:
        print("\nOperation failed! The specified value is invalid.")

    return balance, statement


def view_statement(balance, /, *, statement):
    print("\n================ STATEMENT ================")
    print("No transactions have been made." if not statement else statement)
    print(f"\nBalance: $ {balance:.2f}")
    print("===========================================")


def create_user(users):
    cpf = input("Enter the cpf numbers:")
    user = filter_users(cpf, users)

    if user:
        print("Error! CPF already associated with an account")
        return

    name = input("Enter the name:")
    date_of_birth = input("Enter the date of birth (dd-mm-yyyy):")
    address = input("Enter the address (street, number - neighborhood - city/state abbreviation):")
    
    users.append({"name":name, "date_of_birth":date_of_birth, "cpf":cpf, "address":address})
    
    print("=== User created successfully ===")


def filter_users(cpf, users):
    result = [user for user in users if user["cpf"] == cpf]
    return result[0] if result else None


def create_account(branch, account_number, users):
    cpf = input("Enter the cpf numbers:")
    user = filter_users(cpf, users)

    if user:
        print("\n=== Account created successfully! ===")
        return {"branch":branch, "account_number": account_number, "user": user}
    
    print("User not found! Account creation process terminated!")


def list_accounts(accounts):
    for account in accounts:
        line = f"""\
            Branch:\t{account['branch']}
            A/C:\t\t{account['account_number']}
            Holder:\t{account['user']['name']}
        """
        print("="*100)
        print(textwrap.dedent(line))


def main():
    WITHDRAWAL_LIMIT = 3
    BRANCH = "0001"

    balance = 0
    limit = 500
    statement = ""
    num_withdrawals = 0
    users = []
    accounts = []

    while True:
        option = menu()

        if option == "d":
            value = float(input("Enter the deposit amount: "))

            balance, statement = deposit(balance, value, statement)            

        elif option == "w":
            value = float(input("Enter the withdrawal amount: "))

            balance, statement = withdraw(
                balance=balance,
                value=value,
                statement=statement,
                limit=limit,
                num_withdrawals=num_withdrawals,
                withdrawal_limit=WITHDRAWAL_LIMIT,
            )
            
        elif option == "s":
            view_statement(balance, statement=statement)

        elif option == "nc":
            account_number = len(accounts) + 1
            account = create_account(BRANCH, account_number, users)

            if account:
                accounts.append(account)
        
        elif option == "nu":
            create_user(users)

        elif option == "lc":
            list_accounts(accounts)

        elif option == "q":
            break

        else:
            print("Invalid operation, please select the desired operation again.")


main()
