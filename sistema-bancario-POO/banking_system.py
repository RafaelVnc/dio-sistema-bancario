import textwrap
from abc import ABC, abstractmethod
from datetime import datetime


class Client:
    def __init__(self, address):
        self.address = address
        self.accounts = []
    
    def perform_transaction(self, account, transaction):
        transaction.register(account)
    
    def add_account(self, account):
        self.accounts.append(account)


class Individual(Client):
    def __init__(self, address, cpf, name, birth_date):
        super().__init__(address)
        self.cpf = cpf
        self.name = name
        self.birth_date = birth_date


class Account:
    def __init__(self, number, client):
        self._balance = 0
        self._number = number
        self._agency = "0001"
        self._client = client
        self._history = History()

    @classmethod
    def new_account(cls, client, number):
        return cls(number, client)
    
    @property
    def balance(self):
        return self._balance
    
    @property
    def number(self):
        return self._number
    
    @property
    def agency(self):
        return self._agency
    
    @property
    def client(self):
        return self._client
    
    @property
    def history(self):
        return self._history
    
    def withdraw(self, amount):
        balance = self._balance
        exceeded_balance = amount > balance

        if exceeded_balance:
            print("\n@@@ Operation failed! Insufficient balance. @@@")
        
        elif amount > 0:
            self._balance -= amount
            print("\n=== Withdrawal successful! ===")
            return True
        
        else:
            print("\n@@@ Operation failed! Invalid amount. @@@")

            return False
        
    def deposit(self, amount):
        if amount > 0:
            self._balance += amount
            print("\n=== Deposit successful! ===")
        else:
            print("\n@@@ Operation failed! Invalid amount. @@@")
            return False

        return True
    

class CheckingAccount(Account):
    def __init__(self, number, client, limit=500, withdrawal_limit=3):
        super().__init__(number, client)
        self.limit = limit
        self.withdrawal_limit = withdrawal_limit
    
    def withdraw(self, amount):
        withdrawal_count = len(
            [transaction for transaction in self.history.transactions if transaction["type"] == Withdrawal.__name__]
        )

        exceeded_limit = amount > self.limit
        exceeded_withdrawals = withdrawal_count >= self.withdrawal_limit

        if exceeded_limit:
            print("\n@@@ Operation failed! Withdrawal amount exceeds the limit. @@@")

        elif exceeded_withdrawals:
            print("\n@@@ Operation failed! Maximum number of withdrawals exceeded. @@@")
        
        else:
            return super().withdraw(amount)
        
        return False
    
    def __str__(self):
        return f"""\
            Agency:\t{self.agency}
            Account:\t{self.number}
            Holder:\t{self.client.name}
        """
    

class History:
    def __init__(self):
        self._transactions = []
    
    @property
    def transactions(self):
        return self._transactions
    
    def add_transaction(self, transaction):
        self._transactions.append(
            {
                "type": transaction.__class__.__name__,
                "amount": transaction.amount,
             }
        )


class Transaction(ABC):
    @property 
    @abstractmethod
    def amount(self):
        pass
    
    @classmethod 
    @abstractmethod
    def register(self, account):
        pass


class Withdrawal(Transaction):
    def __init__(self, amount):
        self._amount = amount
    
    @property
    def amount(self):
        return self._amount

    def register(self, account):
        successful_transaction = account.withdraw(self.amount)

        if successful_transaction:
            account.history.add_transaction(self)


class Deposit(Transaction):
    def __init__(self, amount):
        self._amount = amount
    
    @property
    def amount(self):
        return self._amount
    
    def register(self, account):
        successful_transaction = account.deposit(self.amount)

        if successful_transaction:
            account.history.add_transaction(self)


def menu():  
    menu = """\n
    ================ MENU ================
    [d]\tDeposit
    [w]\tWithdraw
    [e]\tStatement
    [nc]\tNew account
    [nu]\tNew user
    [lc]\tList accounts
    [q]\tQuit
    => """
    return input(textwrap.dedent(menu))


def filter_client(cpf, clients):
    result = [client for client in clients if client.cpf == cpf]
    return result[0] if result else None


def get_client_account(client):
    if not client.accounts:
        print("\n@@@ Client does not have an account! @@@")
        return
    
    return client.accounts[0]


def deposit(clients):
    cpf = input("Enter the client's CPF: ")
    client = filter_client(cpf, clients)

    if not client:
        print("\n@@@ Client not found! @@@")
        return
    
    amount = float(input("Enter the deposit amount: "))
    transaction = Deposit(amount)

    account = get_client_account(client)
    if not account:
        return
    
    client.perform_transaction(account, transaction)


def withdraw(clients):
    cpf = input("Enter the client's CPF: ")
    client = filter_client(cpf, clients)

    if not client:
        print("\n@@@ Client not found! @@@")
        return
    
    amount = float(input("Enter the withdrawal amount: "))
    transaction = Withdrawal(amount)

    account = get_client_account(client)
    if not account:
        return
    
    client.perform_transaction(account, transaction)


def show_statement(clients):
    cpf = input("Enter the client's CPF: ")
    client = filter_client(cpf, clients)

    if not client:
        print("\n@@@ Client not found! @@@")
        return

    account = get_client_account(client)
    if not account:
        return

    print("\n================ STATEMENT ================")
    transactions = account.history.transactions

    statement = ""
    if not transactions:
        statement = "No transactions have been made."
    else:
        for transaction in transactions:
            statement += f"\n{transaction['type']}:\n\tR$ {transaction['amount']:.2f}"

    print(statement)
    print(f"\nBalance:\n\tR$ {account.balance:.2f}")
    print("============================================")


def create_client(clients):
    cpf = input("Enter the CPF (numbers only): ")
    client = filter_client(cpf, clients)

    if client:
        print("\n@@@ A client with this CPF already exists! @@@")
        return

    name = input("Enter the full name: ")
    birth_date = input("Enter the birth date (dd-mm-yyyy): ")
    address = input("Enter the address (street, number - neighborhood - city/state): ")

    client = Individual(name=name, birth_date=birth_date, cpf=cpf, address=address)

    clients.append(client)

    print("\n=== Client created successfully! ===")


def create_account(account_number, clients, accounts):
    cpf = input("Enter the client's CPF: ")
    client = filter_client(cpf, clients)

    if not client:
        print("\n@@@ Client not found, account creation flow terminated! @@@")
        return

    account = CheckingAccount.new_account(client=client, number=account_number)
    accounts.append(account)
    client.accounts.append(account)

    print("\n=== Account created successfully! ===")


def list_accounts(accounts):
    for account in accounts:
        print("=" * 100)
        print(textwrap.dedent(str(account)))


def main():
    clients = []
    accounts = []

    while True:
        option = menu()

        if option == "d":
            deposit(clients)

        elif option == "w":
            withdraw(clients)

        elif option == "e":
            show_statement(clients)

        elif option == "nu":
            create_client(clients)

        elif option == "nc":
            account_number = len(accounts) + 1
            create_account(account_number, clients, accounts)

        elif option == "lc":
            list_accounts(accounts)

        elif option == "q":
            break

        else:
            print("\n@@@ Invalid operation, please select the desired operation again. @@@")


main()
