import tkinter as tk
from tkinter import messagebox, simpledialog
from collections import Counter
import tkinter as tk
from tkinter import messagebox, simpledialog
from collections import Counter

class Endereco:

    def _init_(self, rua, numero, bairro, cidade):
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
        return f"{self._rua}, {self.numero} - {self.bairro} - {self._cidade}"


class Cliente:

    def _init_(self, nome, cpf, endereco):
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
        return (
            f"Nome: {self.__nome}\n"
            f"CPF: {self.__cpf}\n"
            f"Endereço: {self.__endereco.exibir_dados()}"
        )


class ContaBancaria:

    numero_contas = []

    def _init_(self, cliente, numero, saldo):
        self.__cliente = cliente
        self.__numero = numero
        self.__saldo = saldo

        cliente.adicionar_conta(self)

        ContaBancaria.numero_contas.append(numero)

    @classmethod
    def verificar_conta_duplicada(cls):
        return len(cls.numero_contas) != len(set(cls.numero_contas))

    @classmethod
    def contas_duplicadas(cls):
        contador = Counter(cls.numero_contas)
        return [conta for conta, qtd in contador.items() if qtd > 1]

    @property
    def cliente(self):
        return self.__cliente

    @property
    def numero(self):
        return self.__numero

    @property
    def saldo(self):
        return self.__saldo

    def get_titular(self):
        return self.cliente

    def get_numero(self):
        return self.numero

    def get_saldo(self):
        return self.saldo

    def exibir_dados(self):
        return (
            f"Nome: {self.cliente.get_nome()}\n"
            f"CPF: {self.cliente.get_cpf()}\n"
            f"Rua: {self.cliente.get_endereco().get_rua()}\n"
            f"Bairro: {self.cliente.get_endereco().get_bairro()}\n"
            f"Número da Conta: {self.numero}\n"
            f"Saldo: R$ {self.saldo:.2f}"
        )

    def depositar(self, valor):
        if valor > 0:
            self.__saldo += valor
            return True
        return False

    def sacar(self, valor):
        if valor > 0 and self.saldo >= valor:
            self.__saldo -= valor
            return True
        return False

    def transferir(self, valor, obj):
        if self.sacar(valor):
            obj.depositar(valor)
            return True
        return False