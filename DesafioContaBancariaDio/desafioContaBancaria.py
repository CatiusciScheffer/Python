from colorama import Fore, Back, Style

menu = """
[d] Depósito
[s] Saque
[e] Extrato
[q] Sair

Escolha a operação desejada: \n"""

saldo = 0
limite = 500
extrato = ''
numeroSaque = 0

LIMITE_SAQUE = 3

while True:
    print('')
    print(Back.WHITE + Fore.BLACK + Style.BRIGHT + f"{'ESCOLHA UMA DAS OPÇÕES ABAIXO:':^45}" + Style.RESET_ALL)
    
    opcao = str(input(menu).lower().strip())
    
    if opcao == 'd':
        print(Back.WHITE + Fore.BLACK + Style.BRIGHT + f"{'DEPÓSITO R$':^45}" + Style.RESET_ALL)
        valor = float(input(f"{'':>35}"))
        print('')

        if valor > 0:
            saldo += valor
            extrato += f'Depóstito R$ {valor:>25.2f}(+)\n'
            print(Fore.BLUE + Style.BRIGHT + 'Depósito realizado com sucesso!' + Style.RESET_ALL)
        else:
            print(Fore.RED + 'Operação falhou!\nO valor informado é inválido.' + Style.RESET_ALL)
            print('')

    elif opcao == 's':
        print(Back.WHITE + Fore.BLACK + Style.BRIGHT + f"{'SAQUE R$':^45}" + Style.RESET_ALL)
        valor = float(input(f"{'':>35}"))

        if valor > limite:
            print(Fore.RED + 'Operação Falhou"\nValor excede ao limit  de R$ 500,00' + Style.RESET_ALL)
        elif numeroSaque > LIMITE_SAQUE:
            print(Fore.RED + 'Operação Falhou!\nNúmero de saques/dia excedido.')
        elif valor > saldo:
            print(Fore.RED + f'Operação Falhou!\nValor solicitado excede o limite de R${saldo} disponível no momento.' + Style.RESET_ALL)
        elif valor > 0:
            saldo -= valor
            extrato += f'Saque     R$ {valor:>25.2f}(-)\n'
            print(Fore.YELLOW + Style.BRIGHT + 'Saque realizado com sucesso!' + Style.RESET_ALL)
            numeroSaque += 1
        else:
            print(Fore.RED + 'Operação falhou!\nValor informado é inválido' + Style.RESET_ALL)

    elif opcao == 'e':
        print(Back.WHITE + Fore.BLACK + Style.BRIGHT + f"{'EXTRATO':^45}" + Style.RESET_ALL)
        print("Não foram realizadas movimentações." if not extrato else extrato)
        print(Style.BRIGHT + f"Saldo: R${saldo:>25.2f}" + Style.RESET_ALL)
        print("_" * 45)

    elif opcao == 'q':
        close = input(Back.WHITE + Fore.BLACK + Style.BRIGHT + f'''{'Deseja realmente sair?':^45}'''+ Style.RESET_ALL + '''\n[x] SAIR\n[v] VOLTAR\n''').lower().strip()
        if close == 'x':
            break
        else:
            continue
    else:
        print(Fore.RED + 'Operação inválida, escolha novamente a operação desejada.' + Style.RESET_ALL)
