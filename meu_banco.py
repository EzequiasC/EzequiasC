import pytz
from datetime import datetime
from abc import ABC, abstractmethod

# Dados simulados
usuarios = []
contas = []

# Constantes do sistema
AGENCIA = "0001"
LIMITE_SAQUES = 3
LIMITE_TRANSACOES_DIARIAS = 10

# Fuso horário
fuso_brasil = pytz.timezone("America/Sao_Paulo")


# ========== CLASSES ==========
class Cliente:
    def __init__(self, endereco):
        self.endereco = endereco
        self.contas = []

    def realizar_transacao(self, conta, transacao):
        transacao.registrar(conta)

    def adicionar_conta(self, conta):
        self.contas.append(conta)


class PessoaFisica(Cliente):
    def __init__(self, nome, data_nascimento, cpf, endereco):
        super().__init__(endereco)
        self.nome = nome
        self.data_nascimento = data_nascimento
        self.cpf = cpf


class Historico:
    def __init__(self):
        self._transacoes = []

    @property
    def transacoes(self):
        return self._transacoes

    def adicionar_transacao(self, transacao):
        self._transacoes.append({
            "tipo": type(transacao).__name__,
            "valor": transacao.valor,
            "data": datetime.now().strftime('%d-%m-%Y %H:%M:%S'),
        })


class Conta:
    def __init__(self, numero, cliente):
        self._saldo = 0
        self._numero = numero
        self._agencia = AGENCIA
        self._cliente = cliente
        self._historico = Historico()

    @classmethod
    def nova_conta(cls, cliente, numero):
        return cls(numero, cliente)

    @property
    def saldo(self):
        return self._saldo

    @property
    def numero(self):
        return self._numero

    @property
    def agencia(self):
        return self._agencia

    @property
    def cliente(self):
        return self._cliente

    @property
    def historico(self):
        return self._historico

    def sacar(self, valor):
        if valor <= 0:
            print("\n⚠️ Valor inválido para saque.")
            return False

        if valor > self._saldo:
            print("\n⚠️ Saldo insuficiente.")
            return False

        self._saldo -= valor
        print("\n✅ Saque realizado com sucesso!")
        return True

    def depositar(self, valor):
        if valor <= 0:
            print("\n⚠️ Valor inválido para depósito.")
            return False

        self._saldo += valor
        print("\n✅ Depósito realizado com sucesso!")
        return True


class ContaCorrente(Conta):
    def __init__(self, numero, cliente, limite=500, limite_saques=3):
        super().__init__(numero, cliente)
        self.limite = limite
        self.limite_saques = limite_saques

    def sacar(self, valor):
        numero_saques = len([
            t for t in self.historico.transacoes if t["tipo"] == "Saque"
        ])

        if valor > self.limite:
            print("\n⚠️ Valor excede o limite de saque.")
        elif numero_saques >= self.limite_saques:
            print("\n⚠️ Número de saques excedido.")
        else:
            return super().sacar(valor)

        return False

    def __str__(self):
        return f"""\
Agência:\t{self.agencia}
C/C:\t\t{self.numero}
Titular:\t{self.cliente.nome}
"""


class Transacao(ABC):
    @property
    @abstractmethod
    def valor(self):
        pass

    @abstractmethod
    def registrar(self, conta):
        pass


class Saque(Transacao):
    def __init__(self, valor):
        self._valor = valor

    @property
    def valor(self):
        return self._valor

    def registrar(self, conta):
        if conta.sacar(self.valor):
            conta.historico.adicionar_transacao(self)


class Deposito(Transacao):
    def __init__(self, valor):
        self._valor = valor

    @property
    def valor(self):
        return self._valor

    def registrar(self, conta):
        if conta.depositar(self.valor):
            conta.historico.adicionar_transacao(self)


# ========== FUNÇÕES ==========
def filtrar_usuario_por_cpf(cpf):
    for usuario in usuarios:
        if usuario.cpf == cpf:
            return usuario
    return None


def criar_usuario():
    cpf = input("Informe o CPF (somente números): ").strip()

    if not cpf.isdigit() or len(cpf) != 11:
        print("⚠️ CPF inválido. Deve conter 11 dígitos.")
        return

    if filtrar_usuario_por_cpf(cpf):
        print("⚠️ Já existe um usuário com esse CPF.")
        return

    nome = input("Informe o nome completo: ")
    data_nascimento = input("Data de nascimento (dd/mm/aaaa): ")

    logradouro = input("Logradouro: ")
    bairro = input("Bairro: ")
    cidade_estado = input("Cidade/UF: ")

    endereco = f"{logradouro}, {bairro} - {cidade_estado}"
    usuario = PessoaFisica(nome, data_nascimento, cpf, endereco)
    usuarios.append(usuario)

    print("✅ Usuário criado com sucesso!")


def criar_conta():
    cpf = input("Informe o CPF do usuário: ").strip()
    cliente = filtrar_usuario_por_cpf(cpf)

    if not cliente:
        print("⚠️ Usuário não encontrado.")
        return

    numero_conta = len(contas) + 1
    conta = ContaCorrente(numero_conta, cliente)
    contas.append(conta)
    cliente.adicionar_conta(conta)

    print(f"✅ Conta criada com sucesso! Número: {numero_conta}")


def exibir_extrato():
    cpf = input("Informe o CPF do titular: ").strip()
    cliente = filtrar_usuario_por_cpf(cpf)

    if not cliente or not cliente.contas:
        print("⚠️ Conta não encontrada.")
        return

    conta = cliente.contas[0]  # Simplesmente pega a primeira conta

    print("\n========== EXTRATO ==========")
    for t in conta.historico.transacoes:
        print(f"[{t['data']}] {t['tipo']}: R$ {t['valor']:.2f}")
    print(f"Saldo atual: R$ {conta.saldo:.2f}")
    print("=============================")


def realizar_deposito():
    cpf = input("Informe o CPF do titular: ").strip()
    cliente = filtrar_usuario_por_cpf(cpf)

    if not cliente or not cliente.contas:
        print("⚠️ Conta não encontrada.")
        return

    conta = cliente.contas[0]
    valor = float(input("Valor do depósito: "))
    transacao = Deposito(valor)
    cliente.realizar_transacao(conta, transacao)


def realizar_saque():
    cpf = input("Informe o CPF do titular: ").strip()
    cliente = filtrar_usuario_por_cpf(cpf)

    if not cliente or not cliente.contas:
        print("⚠️ Conta não encontrada.")
        return

    conta = cliente.contas[0]
    valor = float(input("Valor do saque: "))
    transacao = Saque(valor)
    cliente.realizar_transacao(conta, transacao)


# ========== MENU PRINCIPAL ==========
def menu():
    while True:
        opcao = input("""
========= MENU =========
[1] Depositar
[2] Sacar
[3] Extrato
[4] Criar Usuário
[5] Criar Conta Corrente
[0] Sair
===========================
=> """)

        if opcao == "1":
            realizar_deposito()
        elif opcao == "2":
            realizar_saque()
        elif opcao == "3":
            exibir_extrato()
        elif opcao == "4":
            criar_usuario()
        elif opcao == "5":
            criar_conta()
        elif opcao == "0":
            print("🏦 Obrigado por usar nosso sistema bancário. Até logo!")
            break
        else:
            print("⚠️ Opção inválida! Tente novamente.")


# Executa o programa
menu()
