class Endereco:
    def __init__(self, rua, numero, bairro, cidade):
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
        return f"Rua: {self.__rua}, Nº {self.__numero} - {self.__bairro}, {self.__cidade}"


class Cliente:
    def __init__(self, nome, cpf, rua, numero, bairro, cidade):
        self.__nome = nome
        self.__cpf = cpf
        self.__endereco = Endereco(rua, numero, bairro, cidade)
        self.__contas = []

    def get_nome(self):
        return self.__nome

    def get_cpf(self):
        return self.__cpf

    def get_endereco(self):
        return self.__endereco

    def adicionar_conta(self, conta):
        self.__contas.append(conta)

    def exibir_dados(self):
        return f"Nome: {self.__nome}\nCPF: {self.__cpf}\n{self.__endereco.exibir_dados()}"

    def __str__(self):
        return self.__nome


class ContaBancaria:
    def __init__(self, cliente, numero, saldo_inicial=0.0):
        self.__titular = cliente
        self.__numero = numero
        self.__saldo = saldo_inicial

    def get_titular(self):
        return self.__titular

    def get_numero(self):
        return self.__numero

    def get_saldo(self):
        return self.__saldo

    def depositar(self, valor):
        if valor > 0:
            self.__saldo = self.__saldo + valor
            return True
        else:
            return False

    def sacar(self, valor):
        if valor > 0:
            if self.__saldo >= valor:
                self.__saldo = self.__saldo - valor
                return True
            else:
                return False
        else:
            return False

    def transferir(self, valor, conta_destino):
        if valor > 0:
            if self.__saldo >= valor:
                self.__saldo = self.__saldo - valor
                conta_destino.depositar(valor)
                return True
            else:
                return False
        else:
            return False

    def get_tipo_conta(self):
        return "Conta Bancária"

    def exibir_dados(self):
        return f"Tipo: {self.get_tipo_conta()}\nNúmero da Conta: {self.__numero}\nSaldo: R$ {self.__saldo:.2f}"


class ContaCorrente(ContaBancaria):

    def __init__(self, cliente, numero, saldo_inicial=0, limite=500, tarifa_mensal=15):
        super().__init__(cliente, numero, saldo_inicial)
        self.__limite = limite
        self.__tarifa_mensal = tarifa_mensal

    def sacar(self, valor):
        if valor > 0:
            if self.get_saldo() + self.__limite >= valor:
                self._ContaBancaria__saldo = self.get_saldo() - valor
                return True
        return False

    def cobrar_tarifa(self):
        return self.sacar(self.__tarifa_mensal)

    def exibir_dados(self):
        return super().exibir_dados() + f"\nLimite: R$ {self.__limite:.2f}"

    def get_tipo_conta(self):
        return "Conta Corrente"


class ContaPoupanca(ContaBancaria):

    def __init__(self, cliente, numero, saldo_inicial=0, taxa_rendimento=0.01):
        super().__init__(cliente, numero, saldo_inicial)
        self.__taxa_rendimento = taxa_rendimento

    def render_juros(self):
        juros = self.get_saldo() * self.__taxa_rendimento
        self._ContaBancaria__saldo += juros

    def exibir_dados(self):
        return super().exibir_dados() + f"\nTaxa de rendimento: {self.__taxa_rendimento * 100}%"

    def get_tipo_conta(self):
        return "Conta Poupança"


class ContaSalario(ContaBancaria):

    def __init__(self, cliente, numero, saldo_inicial=0,
                 empresa="", limite_saques=3):

        super().__init__(cliente, numero, saldo_inicial)

        self.__empresa = empresa
        self.__saques_realizados = 0
        self.__limite_saques = limite_saques

    def receber_salario(self, valor):
        return super().depositar(valor)

    def depositar(self, valor):
        return False

    def sacar(self, valor):
        if self.__saques_realizados < self.__limite_saques:
            if super().sacar(valor):
                self.__saques_realizados += 1
                return True
        return False

    def transferir(self, valor, conta_destino):
        return False

    def exibir_dados(self):
        return super().exibir_dados() + \
               f"\nEmpresa: {self.__empresa}" + \
               f"\nSaques: {self.__saques_realizados}/{self.__limite_saques}"

    def get_tipo_conta(self):
        return "Conta Salário"