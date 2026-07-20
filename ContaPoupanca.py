from ContaBancaria import ContaBancaria

class ContaPoupanca(ContaBancaria):
    def __init__(self, cliente, numero, saldo,taxa_rendimento):
        super().__init__(cliente, numero, saldo)
        self.__taxa_rendimento = taxa_rendimento
    def sacar(self, valor):
        return False
    def get_tipo_conta(self):
        return 'Conta Poupança'
    def render_juros(self):
        self._ContaBancaria__saldo += self.__taxa_rendimento * self._ContaBancaria__saldo * 0.01
        return None
    def exibir_dados(self):
         return f"{super().exibir_dados()}\nTaxa:{self.__taxa_rendimento}"