from collections import Counter

class Cliente:
    def __init__(self, nome: str, cpf: str, endereco: 'Endereco'):
        self.__nome = nome
        self.__cpf = cpf
        self.__endereco = endereco
        self.__contas = []

    def get_nome(self) -> str:
        return self.__nome
    
    def get_cpf(self) -> str:
        return self.__cpf
    
    def get_endereco(self) -> 'Endereco':
        return self.__endereco
    
    def get_contas(self) -> bool:
        if not self.__contas:
            return "Este cliente ainda não poossui contas"
        
    def listar_contas(self) -> str:
        linhas = []
        for conta in self.__contas:
            linhas.append(
                f"Conta {conta.get_numero()} - {conta.get_tipo_conta()} - Saldo: R${conta.get_saldo():.2f}"
            )
        return "\n".join(linhas)
    
    def exibir_dados_cliente(self) -> str:
        return (
            f"Nome: {self.get_nome()}\n"
            f"CPF: {self.get_cpf()}\n"
            f"Endereço: {self.get_endereco().exibir_dados()}"
        )

    def adicionar_conta(self, conta: 'ContaBancaria'):
        self.__contas.append(conta)

    def quantidade_contas(self):
        if len (self.__contas) >= 1:
            return len (self.__contas)
        else:
            return "O cliente não tem conta"
        
    def consultar_saldo_total(self):
        saldo_total = 0 
        for conta in self.__contas:
            saldo_total += conta.get_saldo()
        return saldo_total


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
        return (
            f"Rua: {self.get_rua()}\n"
            f"Número: {self.get_numero()}\n"
            f"Bairro: {self.get_bairro()}\n"
            f"Cidade: {self.get_cidade()}\n"
        )


class ContaBancaria:

    numero_contas = []

    def __init__(self, titular: Cliente, numero: str, saldo: float):
        self.__cliente = titular
        self.__numero = numero
        self._saldo = saldo
        ContaBancaria.numero_contas.append(numero)
        self.__cliente.adicionar_conta(self)

    @classmethod
    def verificar_conta_duplicada(cls):
        return len(cls.numero_contas) != len(set(cls.numero_contas))
    
    @classmethod
    def contas_duplicadas(cls):
        # o Counter() conta quantas vezes um elemento aparece em uma coleção
        contador = Counter(cls.numero_contas)
        return[conta for conta, qtd in contador.items() if qtd > 1]

    def get_titular(self) -> str:
        return self.__cliente.get_nome()

    def get_numero(self) -> str:
        return self.__numero

    def get_saldo(self) -> float:
        return self._saldo
    
    def get_cliente(self) -> Cliente:
        return self.__cliente

    def exibir_dados(self) -> str:
        return  (
            f"=======Conta Bancária=======\n"
            f"Número: {self.__numero}\n"
            f"Saldo: R$ {self._saldo:.2f}\n"
            f"Tipo de conta: {self.get_tipo_conta()}"
        )
    
    def depositar(self, valor: float) -> None:
        if valor > 0:
            self._saldo += valor
            return True
        else:
            return False
    
    def sacar(self, valor: float) -> bool:
        if 0 < valor <= self._saldo:
            self._saldo -= valor
            return True
        else:
            return False
    
    def transferir(self, valor: float, obj: 'ContaBancaria') -> bool:
        if self.sacar(valor):
            obj.depositar(valor)
            return True
        return False

    def get_tipo_conta(self):
        return "Conta Bancaria"
    
class ContaCorrente(ContaBancaria):
    def __init__(self, titular: Cliente, numero: str, saldo: float, limite: float, tarifa_mensal: float):
        super().__init__(titular, numero, saldo)
        self.__limite = limite
        self.__tarifa_mensal = tarifa_mensal

    def sacar(self, valor: float) -> None:
        saldo_atual = self._saldo
        if 0 < valor <= saldo_atual + self.__limite:
            self._saldo -= valor
            return True
        else:
            return False

    def cobrar_tarifa(self) -> None:
        if self.__tarifa_mensal <= 0:
            self.sacar(self.__tarifa_mensal)
        else:
            return None

    def exibir_dados(self) -> str:
        return (
            f"{super().exibir_dados()}\n"
            f"Limite: R$ {self.__limite:.2f}"
        )

    def get_tipo_conta(self) -> str:
        return "Conta Corrente"
    
    def pix (self, valor,conta_destino):
        return self.transferir(valor, conta_destino)
    
class ContaPoupanca(ContaBancaria):
    def __init__(self, titular: Cliente, numero: str, saldo: float, taxa_redimento: float):
        super().__init__(titular, numero, saldo)
        self.__taxa_rendimento = taxa_redimento

    def sacar(self, valor) -> None:
        if 0 < valor <= self._saldo:
            super().sacar(valor)
        else:
            return None

    def render_juros(self) -> None:
        if self.__taxa_rendimento > 0:
            self._saldo += self.__taxa_rendimento * self._saldo
        else:
            return None

    def exibir_dados(self) -> str:
        return (
            f"{super().exibir_dados()}\n"
            f"Taxa de Rendimento: {self.__taxa_rendimento}"
            )
    
    def get_tipo_conta(self) -> str:
        return "Conta Poupança"

class ContaInvestimento(ContaBancaria):
    def __init__(self, titular: Cliente, numero: int, saldo: float, taxa_rendimento: float, taxa_administracao: float):
        super().__init__(titular, numero, saldo)
        self.taxa_rendimento = taxa_rendimento
        self.taxa_administracao = taxa_administracao
    
    def get_tipo_conta(self) -> str:
        return "Conta Investimento"
    
    def render_investimento(self):
        self._saldo += (self.taxa_rendimento * 0.01) * self._saldo
        self._saldo -= (self.taxa_administracao * 0.01) * self._saldo 
        return self._saldo
    

    
        
