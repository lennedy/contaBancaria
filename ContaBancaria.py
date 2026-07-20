from typing import List

class Endereco:
    def __init__(self, rua: str, numero: int, bairro: str, cidade: str):
        self.__rua = rua
        self.__numero = numero
        self.__bairro = bairro
        self.__cidade = cidade

    def get_rua(self):
        return self.__rua

    def get_numero(self):
        return self.__numero

    def get_bairro(self):
        return self.__bairro

    def get_cidade(self):
        return self.__cidade

    def exibir_dados(self):
        return f"{self.__rua}, {self.__numero} - {self.__bairro}, {self.__cidade}"


class Cliente:
    def __init__(self, nome: str, cpf: str, endereco: Endereco):
        self.__nome = nome
        self.__cpf = cpf
        self.__endereco = endereco
        self.__contas: List['ContaBancaria'] = []

    def get_nome(self):
        return self.__nome

    def get_cpf(self):
        return self.__cpf

    def get_endereco(self):
        return self.__endereco

    def adicionar_conta(self, conta):
        if conta not in self.__contas:
            self.__contas.append(conta)

    def exibir_dados(self):
        return (
            f"Nome: {self.__nome}\n"
            f"CPF: {self.__cpf}\n"
            f"Endereço: {self.__endereco.exibir_dados()}"
        )

class ContaBancaria:
    numeros_contas = []

    def __init__(self, cliente: Cliente, numero: str, saldo: float):
        self._cliente = cliente
        self._numero = str(numero)
        self._saldo = max(0.0, saldo)

        ContaBancaria.numeros_contas.append(self._numero)
        cliente.adicionar_conta(self)

    def get_titular(self):
        return self._cliente

    def get_numero(self):
        return self._numero

    def get_saldo(self):
        return self._saldo

    def depositar(self, valor):
        if valor > 0:
            self._saldo += valor
            return True
        return False

    def sacar(self, valor):
        if valor > 0 and self._saldo >= valor:
            self._saldo -= valor
            return True
        return False

    def transferir(self, valor, conta_destino):
        if self.sacar(valor):
            if conta_destino.depositar(valor):
                return True
            self._saldo += valor
            return False
        return False

    def exibir_dados(self):
        return (
            f"Tipo: Conta Bancária\n"
            f"Titular: {self._cliente.get_nome()}\n"
            f"Número: {self._numero}\n"
            f"Saldo: R$ {self._saldo:.2f}"
        )

    @classmethod
    def existe_conta_duplicada(cls):
        return len(cls.numeros_contas) != len(set(cls.numeros_contas))

    @classmethod
    def contas_duplicadas(cls):
        duplicadas = []
        for numero in cls.numeros_contas:
            if cls.numeros_contas.count(numero) > 1 and numero not in duplicadas:
                duplicadas.append(numero)
        return duplicadas


class ContaCorrente(ContaBancaria):
    def __init__(self, cliente, numero, saldo,
                 limite=500.0,
                 tarifa_mensal=20.0):

        super().__init__(cliente, numero, saldo)

        self.__limite = limite
        self.__tarifa_mensal = tarifa_mensal

    def get_limite_disponivel(self):
        limite_usado = max(0.0, -self._saldo)
        return self.__limite - limite_usado

    def sacar(self, valor):
        if valor <= 0:
            return False

        if valor <= self._saldo + self.__limite:
            self._saldo -= valor
            return True

        return False

    def cobrar_tarifa(self):
        return self.sacar(self.__tarifa_mensal)

    def exibir_dados(self):
        return (
            super().exibir_dados() +
            f"\nLimite disponível: R$ {self.get_limite_disponivel():.2f}"
        )

    def get_tipo_conta(self):
        return "Conta Corrente"
    

class ContaPoupanca(ContaBancaria):

    def __init__(self, cliente, numero, saldo,
                 taxa_rendimento=0.01):

        super().__init__(cliente, numero, saldo)

        self.__taxa_rendimento = taxa_rendimento

    def render_juros(self):
        rendimento = self.get_saldo() * self.__taxa_rendimento
        self.depositar(rendimento)

    def exibir_dados(self):
        return (
            super().exibir_dados() +
            f"\nTaxa de rendimento: {self.__taxa_rendimento*100:.2f}%"
        )

    def get_tipo_conta(self):
        return "Conta Poupança"


class ContaSalario(ContaBancaria):

    def __init__(self,
                 cliente,
                 numero,
                 saldo,
                 empresa="Empresa",
                 limite_saques=3):

        super().__init__(cliente, numero, saldo)

        self.__empresa = empresa
        self.__saques_realizados = 0
        self.__limite_saques = limite_saques

    def receber_salario(self, valor):
        if valor > 0:
            self._saldo += valor

    def depositar(self, valor):
        print("Conta salário não permite depósitos comuns.")
        return False

    def sacar(self, valor):

        if self.__saques_realizados >= self.__limite_saques:
            return False

        if super().sacar(valor):
            self.__saques_realizados += 1
            return True

        return False

    def transferir(self, valor, conta_destino):
        print("Conta salário não permite transferência para outra conta.")
        return False

    def exibir_dados(self):
        return (
            super().exibir_dados() +
            f"\nEmpresa: {self.__empresa}"
            f"\nSaques: {self.__saques_realizados}/{self.__limite_saques}"
        )

    def get_tipo_conta(self):
        return "Conta Salário"
    
