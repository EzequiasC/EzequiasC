import pytz
from datetime import datetime

usuarios = []
contas = []

AGENCIA = "0001"
LIMITE_SAQUES = 3
LIMITE_TRANSACOES_DIARIAS = 10

saldo = 0
limite = 500
extrato = ""
numero_saques = 0
transacoes_hoje = 0

fuso_brasil = pytz.timezone("America/Sao_Paulo")

# ===== Funções =====

def filtrar_usuario_por_cpf(cpf):
    for usuario in usuarios:
        if usuario["cpf"] == cpf:
            return usuario
    return None

def criar_usuario():
    cpf = input("Informe o CPF (somente números): ").strip()

    if not cpf.isdigit() or len(cpf) != 11:
        print("⚠️ CPF inválido. Deve conter apenas 11 números.")
        return

    if filtrar_usuario_por_cpf(cpf):
        print("⚠️ Já existe um usuário com esse CPF!")
        return

    nome = input("Informe o nome completo: ")
    data_nascimento = input("Informe a data de nascimento (dd/mm/aaaa): ")

    logradouro = input("Informe o logradouro (Rua, Avenida etc.): ")
    bairro = input("Informe o bairro: ")
    cidade_estado = input("Informe a cidade e sigla do estado (ex: Belo Horizonte/MG): ")

    endereco = {
        "logradouro": logradouro,
        "bairro": bairro,
        "cidade_estado": cidade_estado
    }

    usuarios.append({
        "nome": nome,
        "data_nascimento": data_nascimento,
        "cpf": cpf,
        "endereco": endereco
    })

    print("✅ Usuário criado com sucesso!")

def criar_conta():
    cpf = input("Informe o CPF do usuário: ").strip()
    usuario = filtrar_usuario_por_cpf(cpf)

    if not usuario:
        print("⚠️ Usuário não encontrado. Crie um usuário primeiro.")
        return

    numero_conta = len(contas) + 1
    contas.append({
        "agencia": AGENCIA,
        "numero": numero_conta,
        "usuario": usuario
    })

    print(f"✅ Conta criada com sucesso! Agência: {AGENCIA} | Número da conta: {numero_conta}")

# ===== Menu principal =====

menu = """
========= MENU =========

[1] Depositar
[2] Sacar
[3] Extrato
[4] Criar Usuário
[5] Criar Conta Corrente
[0] Sair

========================
=> """

while True:
    opcao = input(menu)

    agora = datetime.now(fuso_brasil)
    data_hora_formatada = agora.strftime('%d/%m/%Y %H:%M:%S')

    if opcao in ['1', '2'] and transacoes_hoje >= LIMITE_TRANSACOES_DIARIAS:
        print("⚠️ Operação falhou! Você excedeu o limite diário de transações.")
        continue

    if opcao == "1":
        valor = float(input("Informe o valor do depósito: "))

        if valor > 0:
            saldo += valor
            extrato += f"[{data_hora_formatada}] Depósito: R$ {valor:.2f}\n"
            transacoes_hoje += 1
            print("✅ Depósito realizado com sucesso.")
        else:
            print("⚠️ Operação falhou! Valor inválido.")

    elif opcao == "2":
        valor = float(input("Informe o valor do saque: "))
        excedeu_saldo = valor > saldo
        excedeu_limite = valor > limite
        excedeu_saques = numero_saques >= LIMITE_SAQUES

        if excedeu_saldo:
            print("⚠️ Operação falhou! Saldo insuficiente.")
        elif excedeu_limite:
            print("⚠️ Operação falhou! Valor excede o limite por saque.")
        elif excedeu_saques:
            print("⚠️ Operação falhou! Número máximo de saques diários excedido.")
        elif valor > 0:
            saldo -= valor
            extrato += f"[{data_hora_formatada}] Saque: R$ {valor:.2f}\n"
            numero_saques += 1
            transacoes_hoje += 1
            print("✅ Saque realizado com sucesso.")
        else:
            print("⚠️ Operação falhou! Valor inválido.")

    elif opcao == "3":
        print("\n========== EXTRATO ==========")
        print("Nenhuma movimentação registrada." if not extrato else extrato)
        print(f"Saldo atual: R$ {saldo:.2f}")
        print("=============================\n")

    elif opcao == "4":
        criar_usuario()

    elif opcao == "5":
        criar_conta()

    elif opcao == "0":
        print("🏦 Obrigado por usar nosso sistema bancário. Até logo!")
        break

    else:
        print("⚠️ Opção inválida! Tente novamente.")
