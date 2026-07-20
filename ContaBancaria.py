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
        

    def quantidade_contas(self):
        return len(self.__contas)
    
    def consultar_saldo_total(self):
        return sum(conta.get_saldo() for conta in self.__contas)

        
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
        self.__titular = titular
        self.__numero = numero
        self.__saldo = saldo

        ContaBancaria.numeros_conta.append(self.__numero)
        titular.adicionar_conta(self)

    def get_titular(self):
        return self.__titular.get_nome()
    
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
        if valor > 0 and self.__saldo >= valor:
            self.__saldo -= valor
            return True
        return False

    def transferir(self, valor, conta_destino):
        if self.sacar(valor):
            conta_destino.depositar(valor)
            return True
        return False
    
    def exibir_dados(self):
        endereco = self.__titular.get_endereco()

        return (
            f"Nome: {self.__titular.get_nome()}\n"
            f"CPF: {self.__titular.get_cpf()}\n"
            f"Rua: {endereco.get_rua()}\n"
            f"Bairro: {endereco.get_bairro()}\n"
            f"Numero da Conta: {self.__numero}\n"
            f"Saldo: R$ {self.__saldo:.2f}"
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
    def __init__(self, cliente, numero, saldo, limite = 500, tarifa_mensal = 100):
        super().__init__(cliente, numero, saldo)
        self.__limite = limite
        self.__tarifa_mensal = tarifa_mensal
    
    def get_tipo_conta(self):
        return "Conta Corrente"

    def limite(self):
        if self.__limite >= 500:  
            return "Limite excedido"  
        else:
            return self.__saldo
        
    def sacar(self, valor):
        if valor > 0 and self.get_saldo() + self.__limite >= valor:
            self._ContaBancaria__saldo -= valor
            return True
        return False    
    
    def cobrar_taxa(self):
        return self.sacar(self.__tarifa_mensal)
    
    def pix(self, valor, conta_destino):
        if valor <= 0 or self.get_saldo() < valor:
            return False
        if self.sacar(valor):
            if conta_destino.depositar(valor):
                return True
            self.depositar(valor)
        return False

            
    
    def exibir_dados(self):
        return( 
            super().exibir_dados()
            + f"\nTipo: {self.get_tipo_conta()}"
             f"\nLimite: R$ {self.__limite:.2f}"
             f"\nTarifa Mensal: R$ {self.__tarifa_mensal:.2f}"
        )

class ContaPoupanca(ContaBancaria):
    def __init__(self, titular, numero, saldo, taxa_rendimento=0.05):
        super().__init__(titular, numero, saldo)
        self.__taxa_rendimento = taxa_rendimento    

    def get_tipo_conta(self):
        return "Conta Poupança"
    
    def render_juros(self):
        juros = self.get_saldo() * self.__taxa_rendimento
        self.depositar(juros)

    def exibir_dados(self):
        return (
            super().exibir_dados()
            + f"\nTipo: {self.get_tipo_conta()}"
             f"\nTaxa de rendimento: {self.__taxa_rendimento * 100:.0f}%"
            )    
    


class ContaSalario(ContaBancaria):
    def __init__(self, titular, numero, saldo, empresa, limite_saques=1):
        super().__init__(titular, numero, saldo)
        self.__empresa = empresa
        self.__saques_realizados = 0
        self.__limite_saques = limite_saques 

    def get_tipo_conta(self):
        return "Conta Salário"

    def receber_salario(self, valor):
        return super().depositar(valor)

    def depositar(self, valor):
        return False

    def sacar(self, valor):
        if self.__saques_realizados >= self.__limite_saques:
            return False

        if super().sacar(valor):
            self.__saques_realizados += 1
            return True

        return False              
    
    def transferir(self):
        return False

    def exibir_dados(self):
        return (
            super().exibir_dados()
            + f"\nTipo: {self.get_tipo_conta()}"
             f"\nEmpresa: {self.__empresa}"
             f"\nSaques realizados: {self.__saques_realizados}"
             f"\nLimite de saques: {self.__limite_saques}"
        )
        
    
class ContaInvestimento(ContaBancaria):
    def __init__(self, titular, numero , saldo, taxa_rendimento = 0.05, taxa_administracao = 0.01):
        super().__init__(titular, numero, saldo)
        self.__taxa_rendimento = taxa_rendimento
        self.__taxa_administracao = taxa_administracao

    def get_tipo_conta(self):
        return "Conta Investimento"
    
    def render_investimento(self):
        rendimento = self.get_saldo() * self.__taxa_rendimento
        taxa_administracao = rendimento * self.__taxa_administracao
        rendimento_total = rendimento - taxa_administracao

        self.depositar(rendimento_total)
