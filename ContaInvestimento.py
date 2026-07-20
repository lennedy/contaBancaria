from ContaBancaria import ContaBancaria


class ContaInvestimento(ContaBancaria):
    def __init__(self, cliente, numero, saldo,taxa_rendimento,taxa_administracao):
        super().__init__(cliente, numero, saldo)
        self.__taxa_rendimento:float = taxa_rendimento
        self.__taxa_administracao:float = taxa_administracao
    def get_tipo_conta(self) -> str:
        return "Conta Investimento"
    def render_investimento(self):
        self._ContaBancaria__saldo += (self.__taxa_rendimento * 0.01 )* self._ContaBancaria__saldo 
        self._ContaBancaria__saldo -= self.__taxa_administracao
        return None