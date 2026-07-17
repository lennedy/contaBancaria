from collections import Counter

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
        return f"Rua: {self.get_rua()}, Nº {self.get_numero()} | Bairro: {self.get_bairro()} | Cidade: {self.get_cidade()}"
    

class Cliente:
    def __init__(self, nome: str, cpf: str, endereco:str):
        self.__nome = nome
        self.__cpf = cpf
        self.__endereco = endereco

    def get_nome(self) -> str:
        return self.__nome
    
    def get_cpf(self) -> str:
        return self.__cpf
    
    def get_endereco(self) -> Endereco:
        return self.__endereco
    
    def exibir_dados(self) -> str:
        return f"Nome: {self.get_nome()} | CPF: {self.get_cpf()} | Endereço: {self.get_endereco().exibir_dados()}"
    

class ContaBancaria:

    numero_contas = []
    def __init__(self, titular: Cliente, numero: str, saldo: float):
        self.__Cliente = titular
        self.__numero = numero
        self._saldo = saldo
    
        ContaBancaria.numero_contas.append(numero)

    @classmethod
    def verificar_conta_duplicada(cls):
        return len(cls.numero_contas) != len(set(cls.numero_contas))
    
    @classmethod
    def contas_duplicadas(cls):
        def contas_duplicacadas(cls):
            contador = Counter(cls.numero_contas)
            return[conta for conta, qtd in contador.items() if qtd > 1]

    @property
    def titular(self):
        return self.__titular

    @property
    def numero(self):
        return self.__numero

    @property
    def saldo(self):
        return self._saldo
     
    def get_tipo_conta(self) -> str:
        return "Conta Bancária"

    def get_titular(self) -> str:
        return self.__Cliente.get_nome()
    def get_numero(self) -> str:
        return self.__numero
    def get_saldo(self) -> str:
        return self._saldo
    
    def depositar(self, valor):
        if valor > 0:
            self._saldo += valor
            return True
        else:
            return False
    
    def sacar(self, valor):
        if self.saldo >= valor:
            self._saldo -= valor
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
        return f"{self.__Cliente.exibir_dados()} | numero: {self.__numero} | saldo: R$ {self._saldo}"
    
class ContaCorrente(ContaBancaria):
    def __init__(self, titular: Cliente, numero: str, saldo: float, limite:float, tarifa_mensal: float):
        super().__init__(titular, numero, saldo)
        self.__limite = limite
        self.__tarifa_mensal = tarifa_mensal
    
    def get_tipo_conta(self) -> str:
        return "Conta Corrente"
    
    def sacar(self, valor: float) -> bool:
        saldo_atual = self._saldo
        if 0 < valor <= saldo_atual + self.__limite:
            self._saldo -= valor
            return True
        else:
            return False
    
    def cobrar_taxa(self,) -> None:
        if self.__tarifa_mensal >= 0:
            self.sacar(self.__tarifa_mensal)
         


class ContaPoupanca(ContaBancaria):
    def __init__(self, titular, numero, saldo, taxa_rendimento):
        super().__init__(titular, numero, saldo)
        self.__taxa_rendimento = taxa_rendimento
    
    def get_tipo_conta(self):
        return "Conta Poupança"
    
    def render_juros(self, ):
        # if self.__taxa_rendimento:
        self._saldo += self._saldo * self.__taxa_rendimento
        # print(self._saldo)

class ContaSalario(ContaBancaria):
    def __init__(self, titular, numero, saldo, empresa, saques_realizados, limite_saques):
        super().__init__(titular, numero, saldo)
        self.__empresa = empresa
        self.__saques_realizados = saques_realizados
        self.__limite_saques = limite_saques

    def get_tipo_conta(self) -> str:
        return "Conta Salário"

    def get_empresa(self) -> str:
        return self.__empresa

    def get_saques_realizados(self) -> int:
        return self.__saques_realizados

    def get_limite_saques(self) -> int:
        return self.__limite_saques

    def receber_salario(self, valor: float) -> bool:
        if valor > 0:
            self._saldo += valor
            return True
        return False

    def depositar(self, valor: float) -> bool:
        return False

    def sacar(self, valor: float) -> bool:
        if valor <= 0:
            return False
        if valor > self._saldo:
            return False
        if self.__saques_realizados >= self.__limite_saques:
            return False

        self._saldo -= valor
        self.__saques_realizados += 1
        return True

    def transferir(self, valor: float, obj) -> bool:
        return False

    def exibir_dados(self) -> str:
        dados_base = super().exibir_dados()
        return (f"{dados_base} | Empresa: {self.__empresa} | "
                f"Saques: {self.__saques_realizados}/{self.__limite_saques}")
    
    