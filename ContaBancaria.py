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
    def __init__(self,nome,cpf,endereco):
        self.__nome=nome
        self.__cpf=cpf
        self.__contas=[]
        self.__endereco = endereco
    def get_contas(self):
        return self.__contas    
    
    def get_nome(self):
        return self.__nome
    
    def get_cpf(self):
        return self.__cpf
    
    def get_endereco(self):
        return self.__endereco
    
    def exibir_dados(self):
        return f"nome:{self.get_nome()} cpf:{self.get_cpf()} endereço:{self.__endereco.exibir_dados()}"
    
    def adicionar_conta(self,conta):
        self.__contas.append(conta)
    
class ContaBancaria:


    numero_contas=[]
    contas_duplicadas1=[]

    numero_contas = []
    contas_duplicadas = []
    def __init__(self, nome, conta, saldo):
        self.__cliente = nome
        self.__numero = conta
        self._saldo = saldo
        
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
        return self.__numero
    def get_saldo(self):
        return self._saldo
    

    def depositar(self,valor):
        if valor > 0:
            self._saldo += valor
            return True
        else:
            return False
        
    def sacar(self, valor):
        
        if self._saldo >= valor:
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
        return f"""
    titular:{self.__cliente.get_nome()}
    conta:{self.get_numero()}
    saldo:{self.get_saldo()}
    cpf:{self.__cliente.get_cpf()}
    endereço: rua:{self.__cliente.get_endereco().exibir_dados()}
            #  numero:{self.__cliente.get_numero()}
              #cidade:{self.__cliente.get_cidade()}
        """
   
    

    #ta certo
    @classmethod
    def contas_duplicadas(cls):
        duplicados=[]
        vistos = set()

        for numero in cls.numero_contas:
            if numero in vistos and numero not in duplicados:
                duplicados.append(numero)
            else:
                vistos.add(numero)
        return duplicados

    @classmethod
    def existe_conta_duplicada(cls):
        return len(cls.numero_contas) != len(set(cls.numero_contas))
    
class ContaCorrente(ContaBancaria):
    def __init__(self, nome, conta, saldo,tarifa_mensal,limite):
        super().__init__(nome, conta, saldo)
        self.__tarifa_mensal=tarifa_mensal
        self.__limite=limite
    def get_tipo_conta(self):
        return "conta corrente"
    def exibir_dados(self):
        return (
            super().exibir_dados()+
            f"tipo:{self.get_tipo_conta()}\n"
            f"tarifa:{self.__tarifa_mensal}\n "+
            f"limite:{self.__limite}"
        )
           
    
    def sacar(self, valor):
        pass

    def cobrar_tarifa(self):
        super().sacar(self.__tarifa_mensal)
    
class ContaPoupanca(ContaBancaria):
    def __init__(self, nome, conta, saldo,taxa_rendimento):
        super().__init__(nome, conta, saldo)
        self.taxa_rendimento=taxa_rendimento
    def reder_juros(self):
        pass
    def exibir_dados(self):
        return (
            super().exibir_dados()
            )
    def sacar(self):
        pass
    def get_tipo_conta(self):
        return "Conta Poupança"

class ContaSalario(ContaBancaria):
    def __init__(self, nome, conta, saldo,empresa,saques_realizados,limite_saques):
        super().__init__(nome, conta, saldo)
        self.__empresa=empresa
        self.__saques_realizados=saques_realizados
        self.__limite_saques=limite_saques