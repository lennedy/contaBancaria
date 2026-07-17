from ContaBancaria import ContaBancaria

class ContaSalario(ContaBancaria):
    def __init__(self, cliente, numero, saldo,empresa,saques_realizados,limite_saques):
        super().__init__(cliente, numero, saldo)
        self.__empresa = empresa
        self.__saques_realizados = saques_realizados
        self.__limite_saques = limite_saques

    def receber_salario(self, valor):
        super().depositar(valor)

    def sacar(self, valor):
        if self.__saques_realizados >= self.__limite_saques:
            return False
        saque = super().sacar(valor)
        if saque:
            self.__saques_realizados += 1
        return saque
    
    def depositar(self, valor):
        return False
    
    def transferir(self, valor, destino):
        return False
    
    def exibir_dados(self):
        return f"{super().exibir_dados()}\nEmpresa:{self.__empresa}\n Saques Realizados:{self.__saques_realizados}\nLimite de Saque:{self.__limite_saques}"
    
    def get_tipo_conta(self):
        return "Conta Salário"