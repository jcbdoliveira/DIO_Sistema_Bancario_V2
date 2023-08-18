import textwrap
import os
import time

def menu():
    
    menu = """\n
    \033[1;31;40m=========SANTANDER DIO BANK===========
    ================ MENU ================\033[0m
    [d]\tDepositar
    [s]\tSacar
    [e]\tExtrato
    [nc]\tNova conta
    [lc]\tListar contas
    [nu]\tNovo usuário
    [q]\tSair
    => """
    return input(textwrap.dedent(menu))

def depositar(saldo, valor, extrato, /):
    if valor > 0:
        saldo += valor
        extrato += f"(\033[0;32m+\033[0m)Depósito:\tR$ {valor:.2f}\n"
        mostra_mensagem(1, "===Depósito realizado com sucesso!====")

    else:
        mostra_mensagem(0, "Operação falhou!\nO valor informado é inválido." )

    return saldo, extrato

def sacar(*, saldo, valor, extrato, limite, numero_saques, limite_saques):
    excedeu_saldo = valor > saldo
    excedeu_limite = valor > limite
    excedeu_saques = numero_saques >= limite_saques

    if excedeu_saldo:
        mostra_mensagem(0, "Operação falhou!\nVocê não tem saldo suficiente.")

    elif excedeu_limite:
        mostra_mensagem(0, "Operação falhou!\nO valor do saque excede o limite.")

    elif excedeu_saques:
        mostra_mensagem(0, "Operação falhou!\nNúmero máximo de saques excedido.")

    elif valor > 0:
        saldo -= valor
        extrato += f"(\033[1;31m-\033[0m)Saque:\tR$ {valor:.2f}\n"
        numero_saques += 1
        mostra_mensagem(1, "====Saque realizado com sucesso!======")

    else:
         mostra_mensagem(0, "Operação falhou!\nO valor informado é inválido.")

    return saldo, extrato

def exibir_extrato(saldo, /, *, extrato):
    print("\n================ EXTRATO ================")
    print("Não foram realizadas movimentações." if not extrato else extrato)
    print(f"\n(=)Saldo:\tR$ {saldo:.2f}")
    print("==========================================")
    os.system("pause")

def criar_usuario(usuarios):
    cpf = input("Informe o CPF (somente número): ")
    usuario = filtrar_usuario(cpf, usuarios)

    if usuario:
        mostra_mensagem(0, "Já existe usuário com esse CPF!")
        return

    nome = input("Informe o nome completo: ")
    data_nascimento = input("Informe a data de nascimento (dd-mm-aaaa): ")
    endereco = input("Informe o endereço (logradouro, nro - bairro - cidade/sigla estado): ")

    usuarios.append({"nome": nome, "data_nascimento": data_nascimento, "cpf": cpf, "endereco": endereco})

    mostra_mensagem(1, "=== Usuário criado com sucesso! ===")

def filtrar_usuario(cpf, usuarios):
    usuarios_filtrados = [usuario for usuario in usuarios if usuario["cpf"] == cpf]
    return usuarios_filtrados[0] if usuarios_filtrados else None

def criar_conta(agencia, numero_conta, usuarios):
    cpf = input("Informe o CPF do usuário: ")
    usuario = filtrar_usuario(cpf, usuarios)

    if usuario:
        mostra_mensagem(1, "=== Conta criada com sucesso! ===")
        return {"agencia": agencia, "numero_conta": numero_conta, "usuario": usuario}

    mostra_mensagem(0, "Usuário não encontrado,\nfluxo de criação de conta encerrado!")

def listar_contas(contas):
    for conta in contas:
        linha = f"""\
            Agência:\t{conta['agencia']}
            C/C:\t\t{conta['numero_conta']}
            Titular:\t{conta['usuario']['nome']}
        """
        print("=" * 100)
        print(textwrap.dedent(linha))

    os.system("pause")

def mostra_mensagem(tipo, texto):
    titulo = ""
    rodape =""

    if tipo == 0:
        titulo = "\033[1;31;40m===============ATENÇÂO================\033[0m"     
        rodape = "\033[1;31;40m======================================\033[0m"             
    elif tipo == 1:
        titulo = "\033[1;34m=============INFORMAÇÃO===============\033[0m"
        rodape = "\033[1;34m======================================\033[0m"

    print(titulo)
    print(textwrap.dedent(texto))
    print(rodape)
    time.sleep(5)

def main():
    LIMITE_SAQUES = 3
    AGENCIA = "0001"

    saldo = 0
    limite = 500
    extrato = ""
    numero_saques = 0
    usuarios = []
    contas = []

    while True:
        os.system('cls')
        opcao = menu()

        if opcao == "d":
            valor = float(input("Informe o valor do depósito: "))

            saldo, extrato = depositar(saldo, valor, extrato)

        elif opcao == "s":
            valor = float(input("Informe o valor do saque: "))

            saldo, extrato = sacar(
                saldo=saldo,
                valor=valor,
                extrato=extrato,
                limite=limite,
                numero_saques=numero_saques,
                limite_saques=LIMITE_SAQUES,
            )

        elif opcao == "e":
            exibir_extrato(saldo, extrato=extrato)

        elif opcao == "nu":
            criar_usuario(usuarios)

        elif opcao == "nc":
            numero_conta = len(contas) + 1
            conta = criar_conta(AGENCIA, numero_conta, usuarios)

            if conta:
                contas.append(conta)

        elif opcao == "lc":
            listar_contas(contas)

        elif opcao == "q":
            os.system('cls')
            break

        else:
            print("Operação inválida, por favor selecione novamente a operação desejada.")

main()
