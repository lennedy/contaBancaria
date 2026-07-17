import tkinter as tk
from tkinter import messagebox, simpledialog
from ContaBancaria import Cliente, ContaBancaria, Endereco, ContaCorrente, ContaPoupanca, ContaSalario


class BancoApp:
    def __init__(self, janela):
        self.janela = janela
        self.janela.title("Sistema Bancário - POO em Python")
        self.janela.geometry("850x400")


        end1 = Endereco("Rua Luiz Gonzaga", 300, "Centro", "Natal")
        end2 = Endereco("Rua Boriocrática", 193, "Centro", "Natal")
        end3 = Endereco("Rua Parnamirim", 345, "Petrópolis", "Natal")
        end4 = Endereco("Rua Ceará-Mirim", 456, "Centro", "Natal")
   
        cliente1  = Cliente("João", "004.045", end1)
        cliente2 = Cliente("Maria", "023.450", end2)
        cliente3 = Cliente("Pedro", "005.009-56", end3)
        cliente4 = Cliente("Esther", "004.123-78", end4)


        self.contas = [
            ContaCorrente(cliente1, 1001, 500),
            ContaPoupanca(cliente2, 1002, 1000, 0.01),          
            ContaSalario(cliente3, 1003, 300, "Empresa X", 5),
            ContaBancaria(cliente4, 1004, 20)
        ]
   


        # messagebox.showinfo("Sucesso", "Depósito realizado.")


        self.criar_interface()


    def criar_interface(self):
        titulo = tk.Label(
            self.janela,
            text="Banco Python - Contas Bancárias",
            font=("Arial", 18, "bold")
        )
        titulo.pack(pady=15)


        self.frame_contas = tk.Frame(self.janela)
        self.frame_contas.pack()


        self.atualizar_tela()


    def atualizar_tela(self):
        for widget in self.frame_contas.winfo_children():
            widget.destroy()


        for conta in self.contas:
            frame = tk.Frame(
                self.frame_contas,
                borderwidth=2,
                relief="groove",
                padx=10,
                pady=10
            )
            frame.pack(side="left", padx=10, pady=10)


            lbl_titular = tk.Label(
                frame,
                text=conta.get_titular().get_nome(),
                font=("Arial", 14, "bold")
            )
            lbl_titular.pack()


            lbl_numero = tk.Label(
                frame,
                text=f"Conta: {conta.get_numero()}"
            )
            lbl_numero.pack()


            lbl_saldo = tk.Label(
                frame,
                text=f"Saldo: R$ {conta.get_saldo():.2f}",
                font=("Arial", 12)
            )
            lbl_saldo.pack(pady=5)


            btn_depositar = tk.Button(
                frame,
                text="Depositar",
                width=15,
                command=lambda c=conta: self.depositar(c)
            )
            # btn_depositar.config(state="disabled")
            btn_depositar.pack(pady=2)


            btn_sacar = tk.Button(
                frame,
                text="Sacar",
                width=15,
                command=lambda c=conta: self.sacar(c)
            )
            # btn_sacar.config(state="disabled")
            btn_sacar.pack(pady=2)


            btn_transferir = tk.Button(
                frame,
                text="Transferir",
                width=15,
                command=lambda c=conta: self.transferir(c)
            )
            # btn_transferir.config(state="disabled")
            btn_transferir.pack(pady=2)


            btn_dados = tk.Button(
                frame,
                text="Exibir Dados",
                width=15,
                command=lambda c=conta: self.exibir_dados(c)
            )
            # btn_dados.config(state="disabled")
            btn_dados.pack(pady=2)


            btn_rendimento = tk.Button(
                frame,
                text="Render Juros",
                width=15,
                command=lambda c=conta: self.render_juros(c)
            )
            btn_rendimento.config(state="disabled")
            btn_rendimento.pack(pady=2)


            btn_taxa = tk.Button(
                frame,
                text="Cobrar Taxa",
                width=15,
                command=lambda c=conta: self.cobrar_taxa(c)
            )
            btn_taxa.config(state="disabled")
            btn_taxa.pack(pady=2)


    def depositar(self, conta):
        valor = simpledialog.askfloat("Depósito", "Digite o valor do depósito:")


        if valor is not None:
            if conta.depositar(valor):
                messagebox.showinfo("Sucesso", "Depósito realizado.")
            else:
                messagebox.showerror("Erro", "Valor inválido.")


        self.atualizar_tela()


    def sacar(self, conta):
        valor = simpledialog.askfloat("Saque", "Digite o valor do saque:")


        if valor is not None:
            if conta.sacar(valor):
                messagebox.showinfo("Sucesso", "Saque realizado.")
            else:
                messagebox.showerror("Erro", "Saldo insuficiente ou valor inválido.")


        self.atualizar_tela()


    def transferir(self, conta_origem):
        valor = simpledialog.askfloat("Transferência", "Digite o valor:")


        if valor is None:
            return


        numero_destino = simpledialog.askinteger(
            "Transferência",
            "Digite o número da conta destino:"
        )


        conta_destino = None


        for conta in self.contas:
            if conta.get_numero() == numero_destino:
                conta_destino = conta
                break


        if conta_destino is None:
            messagebox.showerror("Erro", "Conta destino não encontrada.")
            return


        if conta_origem == conta_destino:
            messagebox.showerror("Erro", "Não é possível transferir para a mesma conta.")
            return


        if conta_origem.transferir(valor, conta_destino):
            messagebox.showinfo("Sucesso", "Transferência realizada.")
        else:
            messagebox.showerror("Erro", "Saldo insuficiente ou valor inválido.")


        self.atualizar_tela()


    def exibir_dados(self, conta):
        messagebox.showinfo("Dados da Conta", conta.exibir_dados())


    def render_juros(self, conta):
        if(conta.get_tipo_conta() == "Conta Poupança"):
            conta.render_juros()
            messagebox.showerror("Sucesso", "Rendimento efetuado.")
        else:
            messagebox.showerror("Erro", "Conta não disponibiliza rendimento")
   
    def cobrar_taxa(self, conta):
        if(conta.get_tipo_conta() == "Conta Corrente"):
            conta.cobrar_tarifa()
            messagebox.showerror("Sucesso", "Rendimento efetuado.")
        else:
            messagebox.showerror("Erro", "Cobrança invalida para essa conta")






janela = tk.Tk()
app = BancoApp(janela)
janela.mainloop()


ContaBancaria.py
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


class ContaBancaria:


    numeros_contas = []
    def __init__(self, cliente: Cliente, numero: str, saldo: float):
        self.__cliente = cliente
        self.__numero = str(numero)
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
