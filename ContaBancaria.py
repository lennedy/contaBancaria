class Cliente:
    def __init__(self, nome, cpf, endereco):
        self.__nome = nome
        self.__cpf = cpf
        self.__endereco = endereco

    def get_nome(self):
        return self.__nome

    def get_cpf(self):
        return self.__cpf

    def get_endereco(self):
        return self.__endereco


class Endereco:
    def __init__(self, rua, bairro):
        self.__rua = rua
        self.__bairro = bairro

    def get_rua(self):
        return self.__rua

    def get_bairro(self):
        return self.__bairro


class ContaBancaria:

    numeros_conta = []

    def __init__(self, titular, numero, saldo):
        self._ContaBancaria__titular = titular
        self._ContaBancaria__numero = numero
        self._ContaBancaria__saldo = saldo

        ContaBancaria.numeros_conta.append(numero)

    def get_titular(self):
        return self._ContaBancaria__titular.get_nome()

    def get_numero(self):
        return self._ContaBancaria__numero

    def get_saldo(self):
        return self._ContaBancaria__saldo

    def depositar(self, valor):
        if valor > 0:
            self._ContaBancaria__saldo += valor
            return True
        return False

    def sacar(self, valor):
        if valor > 0 and self._ContaBancaria__saldo >= valor:
            self._ContaBancaria__saldo -= valor
            return True
        return False

    def transferir(self, valor, conta_destino):
        if self.sacar(valor):
            conta_destino.depositar(valor)
            return True
        return False

    def exibir_dados(self):
        endereco = self._ContaBancaria__titular.get_endereco()

        return (
            f"Nome: {self._ContaBancaria__titular.get_nome()}\n"
            f"CPF: {self._ContaBancaria__titular.get_cpf()}\n"
            f"Rua: {endereco.get_rua()}\n"
            f"Bairro: {endereco.get_bairro()}\n"
            f"Número da Conta: {self._ContaBancaria__numero}\n"
            f"Saldo: R$ {self._ContaBancaria__saldo:.2f}"
        )

    @classmethod
    def existe_conta_duplicadas(cls):
        return len(cls.numeros_conta) != len(set(cls.numeros_conta))

    @classmethod
    def conta_duplicadas(cls):
        vistas = []
        duplicadas = []

        for numero in cls.numeros_conta:
            if numero in vistas and numero not in duplicadas:
                duplicadas.append(numero)
            else:
                vistas.append(numero)

        return duplicadas


class ContaCorrente(ContaBancaria):
    def __init__(self, cliente, numero, saldo, limite, tarifa_mensal):
        super().__init__(cliente, numero, saldo)
        self.__limite = limite
        self.__tarifa_mensal = tarifa_mensal

    def get_limite(self):
        return self.__limite

    def get_tarifa_mensal(self):
        return self.__tarifa_mensal

    def sacar(self, valor):
        if valor > 0 and self.get_saldo() + self.__limite >= valor:
            self._ContaBancaria__saldo -= valor
            return True
        return False

    def cobrar_tarifa(self):
        if self.get_saldo() >= self.__tarifa_mensal:
            self._ContaBancaria__saldo -= self.__tarifa_mensal
            return True
        return False

    def get_tipo_conta(self):
        return "Conta Corrente"

    def exibir_dados(self):
        return (
            super().exibir_dados()
            + f"\nLimite: R$ {self.__limite:.2f}"
            + f"\nTarifa Mensal: R$ {self.__tarifa_mensal:.2f}"
        )