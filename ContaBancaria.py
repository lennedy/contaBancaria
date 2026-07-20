import tkinter as tk
from tkinter import messagebox, simpledialog
from collections import Counter
import tkinter as tk
from tkinter import messagebox, simpledialog
from collections import Counter

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
        return f"{self._rua}, {self.numero} - {self.bairro} - {self._cidade}"


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
        return (
            f"Nome: {self.__nome}\n"
            f"CPF: {self.__cpf}\n"
            f"Endereço: {self.__endereco.exibir_dados()}"
        )
    def quantidade_contas(self, conta):
        for conta in self.__contas:
          self.__contas.append(conta)
        return self.__contas
    
    def consultar_saldo_total(self, saldo, contas):
        self.saldo = saldo
        self.contas = contas
        return len(saldo)
    

class ContaBancaria:

    numero_contas = []

    def __init__(self, cliente, numero, saldo):
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
        


class ContaCorrente(ContaBancaria):
    def __init__(self, cliente, conta, saldo, limite, tarifa_mensal):
      super().__init__(cliente, conta, saldo)
      self.__limite = limite
      self.__tarifa_mensal = tarifa_mensal
    
    def pix(self, valor, conta_destino, conta):
        self.conta_destino = conta_destino
        self.conta = conta
        if valor > 0 and self.saldo >= valor:
              self.__valor -= conta
              self.__valor += conta_destino
              return True
        return False
    

class ContaPoupanca(ContaBancaria):
    def __init__(self, cliente, conta, saldo, taxa_rendimento):
      super().__init__(cliente, conta, saldo)
      self.__taxa_rendimento = taxa_rendimento
    
class ContaSalario(ContaBancaria):
    def __init__(self, cliente, conta, saldo, saques_realizados, empresas, limite_saques):
      super().__init__(cliente, conta, saldo)
      self.__saques_realizados = saques_realizados
      self.__empresas = empresas
      self.__limite_saques = limite_saques
      self.contador = 0

class ContaInvestimento(ContaBancaria):
    def __init__(self, taxa_rendimento = 0, taxa_administracao = 0):
      self.__taxa_rendimento = taxa_rendimento
      self.__taxa_administração = taxa_administracao
   
    def tipo_conta(self):
        return ContaInvestimento
    
    def render_investimento(self):
        rendimento = self.__saldo * self.__taxa_rendimento
        self._saldo = self._saldo = self.__taxa_administração
        return rendimento

      
