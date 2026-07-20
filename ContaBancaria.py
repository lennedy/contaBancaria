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
    
    def quantidade_contas(self):
        return len(self.__contas)
    
    def consultar_saldo_total(self):
        total = 0
        for conta in self.__contas:
            total += conta.get_saldo()
        return total
    
    


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
class ContaCorrente(ContaBancaria):
    def __init__(self, cliente, numero, saldo, cobrar_taxa):
        super().__init__(cliente, numero, saldo)
        self.cobrar_taxa = cobrar_taxa
    def cobrar_taxa(self, taxa):
        saldo_taxado = self.set_saldo(self.get_saldo - taxa)
        return saldo_taxado
    def pix(self, valor, conta_destino):
        return self.transferir(valor,conta_destino) 


        
    def get_tipo_conta(self):
        return "Conta Corrente"



class ContaPoupanca(ContaBancaria):
    def __init__(self, cliente, numero, saldo,taxa_rendimento = 0.06):
     super().__init__(cliente, numero, saldo)
     self.taxa_rendimento = taxa_rendimento
    def render_juros(self):
        juros = self.get_saldo * self.taxa_rendimento
        return juros
    
    def get_tipo_conta(self):
     return " Conta Poupanca"
    
class ContaInvestimento(ContaBancaria):
    def __init__(self,cliente,numero, saldo, taxa_rendimento = float, taxa_administracao = float):
        super().__init__(cliente, numero, saldo)
        self.taxa_rendimento = taxa_rendimento
        self.taxa_administracao = taxa_administracao
    def render_investimento(self):
        investimento = (self.get_saldo() * self.taxa_rendimento) - self.taxa_administracao
        return investimento
        
    def get_tipo_conta(self):
        return " conta investimento"

    
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