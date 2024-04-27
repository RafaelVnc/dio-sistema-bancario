menu = """
=====MENU=====

[d] Deposit
[w] Withdraw
[s] Statement
[q] Quit
 
=> """

balance = 9852.23
limit = 500.00
statement = ""
withdrawal_count = 0
WITHDRAWAL_LIMIT = 3

while True:

    choice = input(menu)

    if choice == "d":
        deposit = float(input("Enter deposit amount:"))
        if deposit > 0:
            balance += deposit
            statement += f"Deposit: $ {deposit:.2f}\n"
        else:
            print("Operation failed! Invalid deposit amount!")
    elif choice == "w":
        withdrawal = float(input("Enter withdrawal amount:"))
        
        insufficient_balance = withdrawal > balance
        exceeded_limit = withdrawal > limit
        exceeded_withdrawals = withdrawal_count >= WITHDRAWAL_LIMIT
        
        if insufficient_balance:
            print("Operation failed! Insufficient balance!")
        elif exceeded_limit:
            print("Operation failed! Withdrawal limit exceeded!")
        elif exceeded_withdrawals:
            print("Operation failed! Exceeded number of withdrawals!")
        elif withdrawal > 0:
            balance -= withdrawal
            statement += f"Withdrawal: $ {withdrawal:.2f}\n"
            withdrawal_count += 1
        else:
            print("Operation failed! Invalid withdrawal amount!")
    elif choice == "s":
        print("STATEMENT".center(30,"="))
        print("No transactions yet!" if not statement else statement)
        print(f"\nFinal balance: $ {balance:.2f}")
        print('='*30)
    elif choice == "q":
        break
    else:
        print("Invalid option, please try again.")
