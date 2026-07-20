import tkinter as tk
from tkinter import messagebox, simpledialog

class Cliente:
    def __init__(self, nome, cpf, endereco):
        self.__nome = nome
        self.__cpf = cpf
        self.__contas = []
        self.__endereco = endereco

    def adicionar_contas(self, conta):
        self.__contas.append(conta)
    
    def get_nome(self):
        return self.__nome
    
    def get_cpf(self):
        return self.__cpf
    
    def get_endereco(self):
        return self.__endereco

    
    def exibir_dados(self):
        return (
        f"\nNome: {self.get_nome()}"
        f"\nCPF: {self.get_cpf()}"
        f"\n{self.get_endereco().exibir_dados()}"
        )
    
    def quantidade_contas(self):
        return len(self.__contas)

    def adicionar_conta(self, conta):
        self.__contas.append(conta)

    def consultar_saldo_total(self):
        total = 0
        for conta in self.__contas:
            total += conta.get_saldo()

        return total

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
        return f"Cidade: {self.get_cidade()},\nBairro: {self.get_bairro()},\nRua: {self.get_rua()},\nNúmero: {self.get_numero()}"


    
class ContaBancaria:
    numeros_contas = []

    def __init__(self, cliente, numero, saldo):
        self.__cliente = cliente
        self.__numero = numero
        self.__saldo = saldo
        ContaBancaria.numeros_contas.append(numero)
        cliente.adicionar_contas(self)

    def get_titular(self):
        return self.__cliente  

    def get_saldo(self):
        return self.__saldo

    def set_saldo(self, saldo):
        self.__saldo = saldo

    def get_numero(self):
        return self.__numero

    def depositar(self, valor):
        if valor < 0:
            return False
        else:
            self.__saldo += valor
            return True
    def get_tipo_conta(self):
        return "Conta Bancaria"
    
    def sacar(self, valor):
        if valor < 0:
            return False
        elif valor > self.__saldo:
            return False
        else:
            self.__saldo -= valor
            return True

    def transferir(self, valor, destino):
        if self.sacar(valor):
            destino.depositar(valor)
            return True
        else:
            return False
        
   

    def exibir_dados(self):
        c = self.__cliente
        end = c.get_endereco()
        return (
        f"Nome: {c.get_nome()}\n"
        f"CPF: {c.get_cpf()}\n"
        f"{end.exibir_dados()}\n"
        f"Número da conta: {self.__numero}\n"
        f"Saldo: R$ {self.__saldo:.2f}"
    )
    @classmethod
    def existe_conta_duplicada(cls):
        return len(cls.numeros_contas) != len(set(cls.numeros_contas))

    @classmethod  
    def contas_duplicadas(cls):
        vistas = []
        duplicadas = []
        for numero in cls.numeros_contas:
            if numero in vistas:
                duplicadas.append(numero)
            else:
                vistas.append(numero)
        return duplicadas  
    



class ContaCorrente(ContaBancaria):
    def __init__(self, cliente, numero, saldo, limite, tarifa_mensal):
        super().__init__(cliente, numero, saldo)
        self.__limite = limite
        self.__tarifa_mensal = tarifa_mensal

    def cobrar_tarifa(self):
        self.sacar(self.__tarifa_mensal)

    def sacar(self, valor):

        if valor < 0:
            return False

        saldo_total = self.get_saldo() + self.__limite
        if valor <= saldo_total:
            self.set_saldo(self.get_saldo() - valor)
            return True

        return False
    
    def exibir_dados(self):
        return (
            super().exibir_dados() +
            f"\nTipo: {self.get_tipo_conta()}"
            f"\nlimite: {self.__limite}" 
            f"\ntarifa: {self.__tarifa_mensal}"
        )
    def get_tipo_conta(self):
        return "Conta Corrente"
    
    def pix(self, valor, conta_destino):
        return self.transferir(valor, conta_destino)

class ContaPoupanca(ContaBancaria):
    def __init__(self, cliente, numero, saldo, taxa_rendimento: float):
        super().__init__(cliente, numero, saldo)
        self.__taxa_rendimento = taxa_rendimento

    def sacar(self, valor):
        return super().sacar(valor)


    def render_juros(self):
        juros = self.get_saldo() * self.__taxa_rendimento
        self.depositar(juros)
    
    def exibir_dados(self):
        return (
            super().exibir_dados() +
            f"\nTipo: {self.get_tipo_conta()}" 
            f"\nTaxa de rendimento: {self.__taxa_rendimento}"
        )

    def get_tipo_conta(self):
        return "Conta Poupança"
    

class ContaSalario(ContaBancaria):
    def __init__(self, cliente, numero, saldo, empresa, limite_de_saque):
            super().__init__(cliente, numero, saldo)
            self.__empresa = empresa
            self.__limite_de_saques = limite_de_saque
            self.__saques_realizados = 0


    def depositar(self, valor):
        return False

    def get_tipo_conta(self):
        return "Conta Salário"
    def sacar(self, valor):
            if self.__saques_realizados >= self.__limite_de_saques:
                return False
            
            if super().sacar(valor):
                self.__saques_realizados += 1
                return True
            
            return False
        
    def transferir(self, valor, conta_destino):
            return False
        
    def exibir_dados(self):
            return(
                super().exibir_dados() +
                f"\nTipo: {self.get_tipo_conta()}" 
                f"\nEmpresa: {self.__empresa}"
                f"\nLimite de saques: {self.__limite_de_saques}"
                f"\nsaques realizados: {self.__saques_realizados}"

            )
    
    def receber_salario(self, valor):
        if valor <= 0:
           return False

        self.set_saldo(self.get_saldo() + valor)
        return True
    
    def pix(valor, conta_destino):
        return False
    

class ContaInvestimento(ContaBancaria):
    def __init__(self, cliente, numero, saldo, taxa_rendimento = float, taxa_administracao= float):
            super().__init__(cliente, numero, saldo)
            self.__taxa_rendimento = taxa_rendimento
            self.__taxa_administracao = taxa_administracao

    def render_investimento(self):
        investimento = (self.get_saldo() * self.__taxa_rendimento)- self.__taxa_administracao
        return self.depositar(investimento)


    def get_tipo_conta(self):
        return "Conta Investimento"
    
    def exibir_dados(self):
        return (
            
            super().exibir_dados()+
            f"\nTaxa de investimento:{self.__taxa_rendimento}"
            f"\n Tipo: {self.get_tipo_conta()}"
            
            )
    


    



