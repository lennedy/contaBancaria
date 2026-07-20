from typing import List


class Endereco:
    def __init__(self, rua: str, numero: int, bairro: str, cidade: str):
        self.__rua = rua
        self.__numero = numero
        self.__bairro = bairro
        self.__cidade = cidade


    def get_rua(self) -> str:
        return self.__rua
   
    def get_numero(self) -> int:
        return self.__numero
   
    def get_bairro(self) -> str:
        return self.__bairro
   
    def get_cidade(self) -> str:
        return self.__cidade
   
    def exibir_dados(self) -> str:
        return f"{self.__rua}, {self.__numero} - {self.__bairro}, {self.__cidade}"


class Cliente:
    def __init__(self, nome: str, cpf: str, endereco: Endereco):
        self.__nome = nome
        self.__cpf = cpf
        self.__endereco = endereco
        self.__contas: List['ContaBancaria'] = []


    def get_nome(self) -> str:
        return self.__nome
   
    def get_cpf(self) -> str:
        return self.__cpf
   
    def get_endereco(self):
        return self.__endereco
   
    def adicionar_conta(self, conta: 'ContaBancaria') -> None:
        if conta not in self.__contas:
            self.__contas.append(conta)

    def exibir_dados(self) -> str:
        return f"Nome: {self.__nome}\nCPF: {self.__cpf}\nEndereço: {self.__endereco.exibir_dados()}"
    
    def quantidade_contas(self):
        return len(self.__contas)
    
    def consultar_saldo_total(self):
        return sum(conta.get_saldo() for conta in self.__contas)

class ContaBancaria:

    numeros_contas = []
    def __init__(self, cliente: Cliente, numero:int, saldo: float):
        self.__cliente = cliente
        self.__numero = numero
        if saldo < 0:
            self.__saldo = 0.0
        else:
            self.__saldo = float(saldo)
       
        ContaBancaria.numeros_contas.append(self.__numero)
        cliente.adicionar_conta(self)


    def get_titular(self) -> Cliente:
        return self.__cliente
   
    def get_numero(self) -> str:
        return self.__numero
   
    def get_saldo(self) -> float:
        return self.__saldo
   
    def set_saldo(self, novo_saldo: float) -> None:
        self.__saldo = novo_saldo
   
    def depositar(self, valor: float) -> None:
        if valor > 0:
            self.__saldo += valor


    def sacar(self, valor: float) -> bool:
        if valor > 0 and self.__saldo >= valor:
            self.__saldo -= valor
            return True
        return False
   
    def transferir(self, valor: float, conta_destino: 'ContaBancaria') -> bool:
        if valor > 0 and self.sacar(valor):
            conta_destino.depositar(valor)
            return True
        return False
   
    def get_tipo_conta(self) -> str:
        return "Conta Bancária"
   
    def exibir_dados(self) -> str:
        return (
            f"Tipo de conta: {self.get_tipo_conta()}\n"
            f"Titular: {self.__cliente.get_nome()}\n"
            f"Conta: {self.__numero}\n"
            f"Saldo: R$ {self.__saldo:.2f}"
        )

    @classmethod
    def existe_conta_duplicada(cls):
        return len(cls.numeros_contas) != len(set(cls.numeros_contas))


    @classmethod
    def contas_duplicadas(cls):
        duplicadas = []
        for numero in cls.numeros_contas:
            if cls.numeros_contas.count(numero) > 1 and numero not in duplicadas:
                duplicadas.append(numero)
        return duplicadas


class ContaCorrente (ContaBancaria):
    def __init__ (self, cliente, numero, saldo, limite=400.0, tarifa_mensal=15.0):
        super().__init__(cliente, numero, saldo)
        self.__limite = float(limite)
        self.__tarifa_mensal = float(tarifa_mensal)


    def sacar(self, valor: float) -> bool:
        if valor <= 0:
            return False
        if super().sacar(valor):
            return True
        saldo_atual = self.get_saldo()
        if (saldo_atual + self.__limite) >= valor:
            falta = valor - saldo_atual
            self.__limite -= falta
            novo_saldo = saldo_atual- valor
            self.set_saldo(novo_saldo)
            return True
        return False
   
    def cobrar_tarifa (self) -> None:
        return self.sacar (self.__tarifa_mensal)
    
    def pix(self, valor, conta_destino):
        return self.transferir(valor, conta_destino)
   
    def exibir_dados(self) -> str:
        return (super().exibir_dados() + f"\nLimite disponível: R$ {self.__limite:.2f}")
   
    def get_tipo_conta (self):
        return "Conta Corrente"
   

class ContaPoupanca (ContaBancaria):
    def __init__(self, cliente: Cliente, numero: str, saldo: float, taxa_rendimento: float):
        super().__init__(cliente, numero, saldo)
        self.__taxa_rendimento = taxa_rendimento
   
    def sacar(self, valor: float) -> bool:
        if valor <= 0:
            return False
        if valor > self.get_saldo():
            return False
       
    def render_juros(self) -> None:
        juros = self.get_saldo() * self.__taxa_rendimento
        self.depositar(juros)


    def get_tipo_conta(self) -> str:
        return "Conta Poupança"
   

class ContaSalario (ContaBancaria):
    def __init__(self, cliente: Cliente, numero: str, saldo: float, empresa: str, limite_saques: int):
        super().__init__(cliente, numero, saldo)
        self.__empresa = str (empresa)
        self.__limite_saques = limite_saques
        self.__saques_realizados = 0
     
    def receber_salario(self, valor: float) -> None:
        if valor > 0:
            self.depositar(valor)
   
    def sacar(self, valor: float) -> bool:
        if valor <= 0:
            return False
        if self.__saques_realizados >= self.__limite_saques:
            return False
        if valor > self.get_saldo():
            return False
        if super().sacar(valor):
            self.__saques_realizados += 1
            return True
        return False
   
    def depositar(self, valor: float) -> bool:
        return super().depositar(valor)
   
    def transferir(self, valor: float, conta_destino: ContaBancaria) -> bool:
        if self.sacar(valor):
            conta_destino.depositar(valor)
            return True
        return False
   
    def exibir_dados(self) -> str:
        dados_mae = super().exibir_dados()
        return (f"{dados_mae}\n"
                f"Empresa: {self.__empresa}\n"
                f"Saques realizados: {self.__saques_realizados}/{self.__limite_saques}")
   
    def get_tipo_conta (self) -> str:
        return "Conta salário"


class ContaInvestimento (ContaBancaria):
    def __init__(self, cliente: Cliente, numero: int, saldo: float, taxa_rendimento: float, taxa_administracao: float):
        super().__init__(cliente, numero, saldo)
        self.__rendimento = taxa_rendimento
        self.__adm = taxa_administracao

    def render_investimento(self):
        rendimento = self.get_saldo() * self.__adm
        descontado = rendimento - self.__adm
        self.depositar(descontado)

    def get_tipo_conta(self) -> str:
        return "Conta Investimento"