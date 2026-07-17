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
    def __init__(self, nome, cpf, endereco) -> None:
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
    
    def exibir_dados(self):
        return f'Nome: {self.__nome}\nCPF: {self.__cpf}\nEndereço: {self.__endereco}'
    
    def adicionar_conta(self, conta):
        self.__contas.append(conta)
    

class ContaBancaria:
    numero_contas = []
    contas_duplicadas = []
    def __init__(self, nome, conta, saldo):
        self.__cliente = nome
        self.__numero = conta
        self.__saldo = saldo
        ContaBancaria.numero_contas.append(self.__numero)
        self.__cliente.adicionar_conta(self)

    @property
    def titular(self):
        return self.__cliente
    
    @property
    def numero(self):
        return self.__numero
    
    @property
    def saldo(self):
        return self.__saldo
    
    def get_titular(self):
        return self.__cliente.get_nome()
    
    def get_numero(self):
        return self.numero
    
    def get_saldo(self):
        return self.saldo
    
    @classmethod
    def existe_conta_duplicada(cls):
        return len(cls.numero_contas) != len(set(cls.numero_contas))
    
    @classmethod
    def contas_duplicadas(cls):
        cls.contas_duplicadas = []
        vistos = set()

        for numero in cls.numero_contas:
            if numero in vistos and numero not in cls.contas_duplicadas:
                cls.contas_duplicadas.append(numero)
            else:
                vistos.add(numero)

        return cls.contas_duplicadas
    
    def depositar(self, valor):
        if valor < 0:
            return False
        else:
            self.__saldo += valor
            return True

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
        return f"Nome: {self.__cliente.get_nome()}\nConta: {self.__numero}\nSaldo: R$ {self.__saldo:.2f}\nCPF: {self.__cliente.get_cpf()}\n{self.__cliente.get_endereco().exibir_dados()}"
    
class ContaCorrente(ContaBancaria):
    def __init__(self, nome, conta, saldo, limite, tarifa_mensal):
        super().__init__(nome, conta, saldo)
        self.__limite = limite
        self.__tarifa_mensal = tarifa_mensal

    def sacar(self, valor):
        if valor <= (self.__limite + self._ContaBancaria__saldo) and self._ContaBancaria__saldo >= -(self.__limite):
            self._ContaBancaria__saldo -= valor
            return True
        else:
            return False
        
    def cobrar_tarifa(self):
        self.sacar(self.__tarifa_mensal)

    def exibir_dados(self):
        return f"Nome: {self._ContaBancaria__cliente.get_nome()}\nConta: {self._ContaBancaria__numero}\nSaldo: R$ {self._ContaBancaria__saldo:.2f}\nCPF: {self._ContaBancaria__cliente.get_cpf()}\n{self._ContaBancaria__cliente.get_endereco().exibir_dados()}\nLimite: {self.__limite}\nTarifa Mensal: {self.__tarifa_mensal}"

    def get_tipo_conta(self):
        return 'Conta Corrente'

class ContaPoupanca(ContaBancaria):
    def __init__(self, nome, conta, saldo, taxa_rendimento):
        super().__init__(nome, conta, saldo)
        self.__taxa_rendimento = taxa_rendimento

    def sacar(self, valor):
        if valor < 0:
            return False
        elif valor > self._ContaBancaria__saldo:
            return False
        else:
            self.__saldo -= valor
            return True

    def render_juros(self):
        rendimento = self.__taxa_rendimento * self._ContaBancaria__saldo
        self._ContaBancaria__saldo += rendimento
        return None

    def exibir_dados(self):
        return f"Nome: {self._ContaBancaria__cliente.get_nome()}\nConta: {self._ContaBancaria__numero}\nSaldo: R$ {self._ContaBancaria__saldo:.2f}\nCPF: {self._ContaBancaria__cliente.get_cpf()}\n{self._ContaBancaria__cliente.get_endereco().exibir_dados()}\nTaxa de rendimento: {self.__taxa_rendimento}"

    def get_tipo_conta(self):
        return 'Conta Poupança'

class ContaSalario(ContaBancaria):
    def __init__(self, nome, conta, saldo, empresa, saquases_realizados, limite_saques):
        super().__init__(nome, conta, saldo)
        self.__empresa = empresa
        self.__saques_realizados = saquases_realizados
        self.__limite_saques = limite_saques
        self.contador = 0

    def receber_salario(self, valor):
        super().depositar(valor)

    def sacar(self, valor):
        self.contador += 1
        if (self.contador >= self.__limite_saques) :
            return 'Limite de saques atingido!'

        else:
            return super().sacar(valor)
    
    def depositar(self, valor):
        return False
    
    def transferir(self, valor, destino):
        return False
    
    def exibir_dados(self):
        return f"Nome: {self._ContaBancaria__cliente.get_nome()}\nConta: {self._ContaBancaria__numero}\nSaldo: R$ {self._ContaBancaria__saldo:.2f}\nCPF: {self._ContaBancaria__cliente.get_cpf()}\n{self._ContaBancaria__cliente.get_endereco().exibir_dados()}\nEmpresa: {self.__empresa}\nSaques realizados: {self.__saques_realizados}\nLimite de saques: {self.__limite_saques}"

    def get_tipo_conta(self):
        return 'Conta Salário'