menu = """
=====MENU=====

[d] Depositar
[s] Sacar
[e] Extrato
[q] Sair
 
=> """

saldo = 9852.23
limite = 500.00
extrato = ""
numero_saques = 0
LIMITE_SAQUES = 3

while True:

    opcao = input(menu)

    if opcao == "d":
        deposito = float(input("Digite o valor do depósito:"))
        if deposito > 0:
            saldo += deposito
            extrato += f"Depósito: R$ {deposito:.2f}\n"
        else:
            print("Falha na operação! Valor inválido para depósito!")
    elif opcao == "s":
        saque = float(input("Digite o valor do saque:"))
        
        saldo_insuficiente = saque > saldo
        limite_excedido = saque > limite
        excedeu_saques = numero_saques >= LIMITE_SAQUES
        
        if saldo_insuficiente:
            print("Falha na operação! Saldo insuficiente!")
        elif limite_excedido:
            print("Falha na operação! Limite de saque excedido!")
        elif excedeu_saques:
            print("Falha na operação! Número de saques excedido!")
        elif saque > 0:
            saldo -= saque
            extrato += f"Saque: R$ {saque:.2f}\n"
            numero_saques += 1
        else:
            print("Falha na operação! Valor inválido para saque!")
    elif opcao == "e":
        print("EXTRATO".center(30,"="))
        print("Não houve movimentações!" if not extrato else extrato)
        print(f"\nSaldo final: R$ {saldo:.2f}")
        print('='*30)
    elif opcao == "q":
        break
    else:
        print("Opção inválida, tente novamente.")
