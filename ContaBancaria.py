import tkinter as tk
from tkinter import messagebox, simpledialog

class Endereco:
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
        return f'Rua: {self.__rua}\nNumero: {self.__numero}\nBairro: {self.__bairro}\nCidade: {self.__cidade}'

class Cliente:
    def __init__(self,nome,cpf,endereco):
        self.__nome=nome
        self.__cpf=cpf
        self.__contas=[]
        self.__endereco = endereco
    def get_contas(self):
        return self.__contas    
    
    def get_nome(self):
        return self.__nome
    
    def get_cpf(self):
        return self.__cpf
    
    def get_endereco(self):
        return self.__endereco
    
    def exibir_dados(self):
        return f":{self.get_nome()} :{self.get_cpf()}"
    
    def adicionar_conta(self,conta):
        self.__contas.append(conta)
    


class ContaBancaria:

    numero_contas=[]
    contas_duplicadas1=[]

    numero_contas = []
    contas_duplicadas = []
    def __init__(self, nome, conta, saldo):
        self.__cliente = nome
        self.__numero = conta
        self.__saldo = saldo
        ContaBancaria.numero_contas.append(self.__numero)
        self.__cliente.adicionar_conta(self)


    def get_titular(self):
        return self.__cliente.get_nome()
    def get_numero(self):
        return self.__numero
    def get_saldo(self):
        return self.__saldo
    

    def depositar(self,valor):
        if valor > 0:
            self.__saldo += valor
            return True
        else:
            return False
        
    def sacar(self, valor):
        
        if self.__saldo >= valor:
            self.__saldo -= valor
            return True
        else:                
            return False
        
            
    
    def transferir(self, valor, obj):
        if self.sacar(valor):
            obj.depositar(valor)
            return True
        else:
            return False
                
                    

    def exibir_dados(self):
        return f"""
        titular:{self.__cliente}
        conta:{self.__numero}
        saldo:{self.__saldo}
        """
   
    

    
    @classmethod
    def contas_duplicadas(cls):
        duplicados=[]
        vistos = set()

        for numero in cls.numero_contas:
            if numero in vistos and numero not in duplicados:
                duplicados.append(numero)
            else:
                vistos.add(numero)
        return duplicados

    @classmethod
    def existe_conta_duplicada(cls):
        return len(cls.numero_contas) != len(set(cls.numero_contas))
    

    class ContaCorrente(ContaBancaria):
    def __init__(self, cliente, numero, saldo, limite,tarifa_mensal):
        super().__init__( cliente, numero, saldo)
        self.__limite = limite
        self.__tarifa_mensal = tarifa_mensal
    def sacar(self, valor):
        if valor <= self.get_saldo() + self.__limite:
            self.set_saldo(self.get_saldo() - valor)
            return True
        else:
            return False
    def cobrar_taxa(self):
        super().sacar(self.__tarifa_mensal)
  

    def exibir_dados(self):
        return  (
            super().exibir_dados() +
            f"\ntipo: {self.get_tipo_conta()}"
            f"\nlimite: {self.__limite}" +
            f"\ntarifa: {self.__tarifa_mensal}"
        )
    def get_tipo_conta(self):
        return "Conta Corrente"

class ContaPoupanca(ContaBancaria):
    def __init__(self, cliente, numero, saldo, taxa_rendimento: float):
        super().__init__( cliente, numero, saldo)
        self.__taxa_rendimento = taxa_rendimento

    def sacar(self, valor):
        return super().sacar(valor)


    def render_juros(self):
        juros = self.get_saldo() * self.__taxa_rendimento
        self.depositar(juros)

      
    def exibir_dados(self):
        return(
        super().exibir_dados() +
        f"\ntipo:{self.get_tipo_conta()}" +
        f"\ntaxa de rendimento:{self.__taxa_rendimento}"
        )
    def get_tipo_conta(self):
        return "Conta Poupança"
class ContaSalario(ContaBancaria):
    def __init__(self, cliente, numero, saldo, empresa, limite_de_saques):
        super().__init__(cliente, numero, saldo)
        self.__empresa = empresa
        self.__limite_de_saques = limite_de_saques
        self.__saques_realizados = 0
    def get_tipo_conta(self):
        return "Conta Salario"
    def depositar(self, valor):
        return False
    def sacar(self, valor):
        if self.__saques_realizados < self.__limite_de_saques:
            if super().sacar(valor):
                self.__saques_realizados += 1
            return True
        return False
    
    def exibir_dados(self):
        return (
        super().exibir_dados() +
        f"\nTipo: {self.get_tipo_conta()}" +
        f"\nEmpresa: {self.__empresa}" +
        f"\nSaques realizados: {self.__saques_realizados}/{self.__limite_de_saques}"
    )
    def receber_salario(self, valor):
        self.set_saldo(self.get_saldo() + valor)
        return True
