import tkinter as tk
from tkinter import messagebox, simpledialog


class Cliente:
    def __init__(self, nome, cpf):
        self.__nome = nome
        self.__cpf = cpf

    def get_nome(self):
        return self.__nome

    def get_cpf(self):
        return self.__cpf

    def exibir_dados(self):
        return f"Nome: {self.__nome}\nCPF: {self.__cpf}"


class ContaBancaria:
    def __init__(self, cliente, numero, saldo):
        self.__cliente = cliente
        self.__numero = numero
        self.__saldo = saldo

    def get_titular(self):
        return self.__cliente

    def get_numero(self):
        return self.__numero

    def get_saldo(self):
        return self.__saldo

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
            f"Nome: {self.__cliente.get_nome()}\n"
            f"CPF: {self.__cliente.get_cpf()}\n"
            f"Número da Conta: {self.__numero}\n"
            f"Saldo: R$ {self.__saldo:.2f}"
        )



class ContaCorrente(ContaBancaria):
    def __init__(self, cliente, numero, saldo, limite, tarifa_mensal):
        super().__init__(cliente, numero, saldo)
        self.__limite = limite
        self.__tarifa_mensal = tarifa_mensal

    def sacar(self, valor):
        
        if valor > 0 and valor <= (self.get_saldo() + self.__limite):
            self._ContaBancaria__saldo -= valor
            return True
        return False

    def cobrar_tarifa(self):
        
        self._ContaBancaria__saldo -= self.__tarifa_mensal

    def exibir_dados(self):
        return super().exibir_dados() + f"\nLimite: R$ {self.__limite:.2f}"


class ContaPoupanca(ContaBancaria):
    def __init__(self, cliente, numero, saldo, taxa_rendimento):
        super().__init__(cliente, numero, saldo)
        self.__taxa_rendimento = taxa_rendimento

    def render_juros(self):
        
        rendimento = self.get_saldo() * self.__taxa_rendimento
        self._ContaBancaria__saldo += rendimento

    def exibir_dados(self):
        return super().exibir_dados() + f"\nTaxa: {self.__taxa_rendimento}"


class ContaSalario(ContaBancaria):
    def __init__(self, cliente, numero, saldo, empresa, limite_saques):
        super().__init__(cliente, numero, saldo)
        self.__empresa = empresa
        self.__saques_realizados = 0
        self.__limite_saques = limite_saques

    def receber_salario(self, valor):
        
        self._ContaBancaria__saldo += valor

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
        return super().exibir_dados() + f"\nEmpresa: {self.__empresa}"
