import tkinter as tk
from tkinter import messagebox, simpledialog

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
        return f'Rua: {self.__rua}, numero: {self.__numero} \nBairro: {self.__bairro} \nCidade {self.__cidade}'


class Cliente:
    def __init__(self, nome, cpf, endereço):
        self.__nome = nome
        self.__cpf = cpf
        self.__endereço = endereço
        self.__contas = []
    
    def get_nome(self):
        return self.__nome
    
    def get_cpf(self):
        return self.__cpf
    
    def get_endereco(self):
        return self.__endereço
    
    def adicionar_conta(self, cnt):
        self.__contas.append(cnt)
    
    def exibir_dados(self):
        return f'Nome: {self.__nome} \nCPF: {self.__cpf} \nEndereço: {self.__endereço}'


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
       
    def get_saldo(self):
        return self.__saldo
    
    @classmethod
    def verificar_conta_duplicada(cls):
        return len(cls.numeros_contas) != len(set(cls.numeros_contas))
    
    @classmethod
    def contas_duplicadas(cls):
        repetidos = set()
        n_repetidos = []
        for x in cls.numeros_contas:
            if ContaBancaria.numeros_contas.count(x) > 1:
                repetidos.add(x)
            else:
                n_repetidos.append(x)
        return f'{repetidos}'
        
    def depositar(self, valor):
        if valor > 0:
            self.__saldo += valor
            return True
        else:
            return False

    def sacar(self, valor):
        if valor > 0 and valor <= self.__saldo:
            self.__saldo -= valor
            return True
        else:
            return False

    def transferir(self, valor, conta_destino):
        if valor > 0 and valor <= self.__saldo:
            self.__saldo -= valor
            conta_destino.depositar(valor)
            return True
        else:
            return False
        
    def exibir_dados(self):
        return f'Conta:\nTitular: {self.__titular.get_nome()}\nNumero da conta: {self.__numero}\nSaldo: R$ {self.__saldo}\nCpf: {self.__titular.get_cpf()}\n\n---------------------------\n\nEndereço:\n{self.__titular.get_endereco().exibir_dados()}'


class ContaCorrente(ContaBancaria):
    def __init__(self, titular, numero, saldo, limite, tarifa_mensal):
        super().__init__(titular, numero, saldo)
        self.__limite = limite
        self.__tarifa_mensal = tarifa_mensal

    def sacar(self,valor): 
        if valor <= (self.__limite + self._ContaBancaria__saldo) and self._ContaBancaria__saldo >= -(self.__limite):
            self._ContaBancaria__saldo -= valor
            return True
        else:
            return False
        
    def cobrar_taxa(self):
        self.sacar(self.__tarifa_mensal)

    def get_tipo(self):
        return "Conta Corrente"

    def exibir_dados(self):
        return f'{super().exibir_dados()}\n\n---------------------------\n\nLimite: {self.__limite}\nTarifa mensal: {self.__tarifa_mensal}'

class ContaPoupanca(ContaBancaria):
    def __init__(self, titular, numero, saldo, taxa_rendimento):
        super().__init__(titular, numero, saldo)
        self.__taxa_rendimento = taxa_rendimento

    def sacar(self, valor):
        if valor < 0 and valor > self._ContaBancaria__saldo:
            return False
        else:
            self.__saldo -= valor
            return True
    
    def render_juros(self):
        rendimento = self.__taxa_rendimento * self._ContaBancaria__saldo
        self._ContaBancaria__saldo += rendimento
        return None
    
    def get_tipo(self):
        return "Conta Poupança"
    
    def exibir_dados(self):
         return f"{super().exibir_dados()}\nTaxa:{self.__taxa_rendimento}"


class ContaSalario(ContaBancaria):
    def __init__(self, titular, numero, saldo, empresa, saques_realizados, limites_saques):
        super().__init__(titular, numero, saldo)
        self.__empresa = empresa
        self.__saques_realizados = saques_realizados
        self.__limite_saques = limites_saques

    def receber_salario(self, valor):
        super().depositar(valor)

    def sacar(self, valor):
        if self.__saques_realizados >= self.__limites_saques:
            return False
        saque = super().sacar(valor)
        if saque:
            self.__saques_realizados += 1
        return saque
    
    def depositar(self, valor):
        return False
    
    def transferir(self, valor, destino):
        return False

    def get_tipo_conta(self):
        return "Conta Salário"
    
    def exibir_dados(self):
        return f"{super().exibir_dados()}\nEmpresa:{self.__empresa}\n Saques Realizados:{self.__saques_realizados}\nLimite de Saque:{self.__limite_saques}"