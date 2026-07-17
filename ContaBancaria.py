class Endereço:
    def __init__(self, rua, numero, bairro, cidade):
        self.__rua = rua
        self.__numero = int(numero)
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
        return f'Rua: {self.__rua}, Numero: {self.__numero}\nBairro: {self.__bairro}\nCidade: {self.__cidade}'


class Cliente:
    def __init__(self, nome, cpf, endereco):
        self.__nome = nome
        self.__cpf = cpf
        self.__endereco = endereco
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
        return f'Nome: {self.__nome}\nCPF: {self.__cpf}\n{self.__endereco.exibir_dados()}'


class ContaBancaria:

    numeros_contas = []

    def __init__(self, titular, numero, saldo):
        self.__titular = titular
        self.__numero = numero
        self.__saldo = saldo
        ContaBancaria.numeros_contas.append(numero)

    def get_titular(self):
        return self.__titular.get_nome()

    def get_numero(self):
        return self.__numero

    def get_tipo_conta(self):
        return "Conta Bancária"

    def get_saldo(self):
        return self.__saldo

    @classmethod
    def verificar_conta_duplicada(cls):
        return len(cls.numeros_contas) != len(set(cls.numeros_contas))

    @classmethod
    def contas_duplicadas(cls):
        repetidos = set()
        for numero in cls.numeros_contas:
            if cls.numeros_contas.count(numero) > 1:
                repetidos.add(numero)
        return repetidos

    def depositar(self, valor):
        if valor > 0:
            self.__saldo += valor
            return True
        return False

    def sacar(self, valor):
        if valor > 0 and valor <= self.__saldo:
            self.__saldo -= valor
            return True
        return False

    def transferir(self, valor, conta_destino):
        if self.sacar(valor):
            conta_destino.depositar(valor)
            return True
        return False

    def exibir_dados(self):
        return (
            f'CONTA\n'
            f'Titular: {self.__titular.get_nome()}\n'
            f'Numero: {self.__numero}\n'
            f'Saldo: R$ {self.__saldo}\n'
            f'CPF: {self.__titular.get_cpf()}\n\n'
            f'ENDEREÇO\n'
            f'{self.__titular.get_endereco().exibir_dados()}'
        )


class ContaCorrente(ContaBancaria):

    def __init__(self, titular, numero, saldo, limite, tarifa_mensal):
        super().__init__(titular, numero, saldo)
        self.__limite = limite
        self.__tarifa_mensal = tarifa_mensal

    def sacar(self, valor):
      if valor > 0 and valor <= self._ContaBancaria__saldo + self.__limite:
        self._ContaBancaria__saldo -= valor
        return True
      return False

    def cobrar_tarifa(self):
        return self.sacar(self.__tarifa_mensal)

    def get_tipo_conta(self):
        return "Conta Corrente"

    def exibir_dados(self):
        return (
            f'{super().exibir_dados()}\n'
            f'Limite: R$ {self.__limite}\n'
            f'Tarifa mensal: R$ {self.__tarifa_mensal}'
        )


class ContaPoupanca(ContaBancaria):

    def __init__(self, titular, numero, saldo, taxa_rendimento):
        super().__init__(titular, numero, saldo)
        self.__taxa_rendimento = taxa_rendimento

    def get_tipo_conta(self):
        return "Conta Poupança"

    def render_juros(self):
        self._ContaBancaria__saldo += (
            self._ContaBancaria__saldo * self.__taxa_rendimento
        )

    def exibir_dados(self):
        return (
            f'{super().exibir_dados()}\n'
            f'Taxa de rendimento: {self.__taxa_rendimento * 100}%'
        )


class ContaSalario(ContaBancaria):

    def __init__(self, titular, numero, saldo, empresa, saques_realizados, limite_saques):
        super().__init__(titular, numero, saldo)
        self.__empresa = empresa
        self.__saques_realizados = saques_realizados
        self.__limite_saques = limite_saques

    def receber_salario(self, valor):
        if valor > 0:
            self._ContaBancaria__saldo += valor
            return True
        return False

    def depositar(self, valor):
        print("Depositos comuns nao sao permitidos.")
        return False

    def sacar(self, valor):
        if self.__saques_realizados >= self.__limite_saques:
            print("Limite de saques atingido.")
            return False

        if valor > 0 and valor <= self._ContaBancaria__saldo:
            self._ContaBancaria__saldo -= valor
            self.__saques_realizados += 1
            return True

        return False

    def get_tipo_conta(self):
        return "Conta Salário"

    def transferir(self, valor, conta_destino):
        print("Tente novamente,transferencias nao sao permitidas para Conta Salario.")
        return False

    def exibir_dados(self):
        return (
            f'{super().exibir_dados()}\n'
            f'Empresa: {self.__empresa}\n'
            f'Saques realizados: {self.__saques_realizados}\n'
            f'Limite de saques: {self.__limite_saques}'
        )
