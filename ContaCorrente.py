from ContaBancaria import ContaBancaria

class ContaCorrente(ContaBancaria):
    def __init__(self, cliente, numero, saldo,limite,tarifa_mensal):
        super().__init__(cliente, numero, saldo)
        self.__limite:float = limite
        self.__tarifa_mensal:float = tarifa_mensal
    def sacar(self,valor:float) -> float: 
        if valor <= (self.__limite + self._ContaBancaria__saldo) and self._ContaBancaria__saldo >= -(self.__limite):
            self._ContaBancaria__saldo -= valor
            return True
        else:
            return False
    def cobrar_tarifa(self) -> None:
        return self.sacar(self.__tarifa_mensal)
    def get_tipo_conta(self):
        return "Conta Corrente"
    def exibir_dados(self) -> str:
        return f'{super().exibir_dados()}\nLimite:{self.__limite:.2f}R$\nTarifa:{self.__tarifa_mensal:.2f}R$'