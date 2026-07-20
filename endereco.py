class Endereco:
    def __init__(self,rua,numero,bairro,cidade):
        self.__rua:str = rua
        self.__numero:int = numero
        self.__bairro:str = bairro
        self.__cidade:str = cidade

    def get_rua(self):
        return self.__rua
    def get_numero(self):
        return self.__numero
    def get_bairro(self):
        return self.__bairro
    def get_cidade(self):
        return self.__cidade
    def exibir_dados(self):
        return (f"Rua: {self.__rua}\n"
                f"Número: {self.__numero}\n"
                f"Bairro: {self.__bairro}\n"
                f"Cidade: {self.__cidade}"             
    )
