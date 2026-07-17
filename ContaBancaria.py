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
        return f"{self.__rua}, {self.__numero} - {self.__bairro} - {self.__cidade}"


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
        contador =(cls.numero_contas)
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
    def __init__(self, titular: Cliente, numero: str, saldo: float, limite: float, tarifa_mensal: float):
        super().__init__(titular, numero, saldo)
        self.__limite = limite
        self.__tarifa_mensal = tarifa_mensal

    def sacar(self, valor: float):
        saldo_atual = getattr(self, "_ContaBancaria__saldo")
        if 0 < valor <= saldo_atual + self.__limite:
            setattr(self, "_ContaBancaria__saldo", saldo_atual - valor)
            return True
        return False
    
    def cobrar_tarifa(self):
        self.sacar(self.__tarifa_mensal)
    
    def exibir_dados(self):
        return super().exibir_dados()
    
    def get_tipo_conta(self):
        return "Conta Corrente"   

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

