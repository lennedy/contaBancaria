from typing import List




class Endereco:
    def __init__(self, rua: str, numero: int, bairro: str, cidade: str):
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
        return f"{self.__rua}, {self.__numero} - {self.__bairro}, {self.__cidade}"




class Cliente:
    def __init__(self, nome: str, cpf: str, endereco: Endereco):
        self.__nome = nome
        self.__cpf = cpf
        self.__endereco = endereco
        self.__contas: List['ContaBancaria'] = []


    def get_nome(self):
        return self.__nome


    def get_cpf(self):
        return self.__cpf


    def get_endereco(self):
        return self.__endereco


    def adicionar_conta(self, conta):
        if conta not in self.__contas:
            self.__contas.append(conta)


    def exibir_dados(self):
        return (
            f"Nome: {self.__nome}\n"
            f"CPF: {self.__cpf}\n"
            f"Endereço: {self.__endereco.exibir_dados()}"
        )




class ContaBancaria:
    numeros_contas = []


    def __init__(self, cliente: Cliente, numero: str, saldo: float):
        self._cliente = cliente
        self._numero = str(numero)
        self._saldo = max(0.0, saldo)


        ContaBancaria.numeros_contas.append(self._numero)
        cliente.adicionar_conta(self)


    def get_titular(self):
        return self._cliente


    def get_numero(self):
        return self._numero


    def get_saldo(self):
        return self._saldo


    def depositar(self, valor):
        if valor > 0:
            self._saldo += valor
            return True
        return False


    def sacar(self, valor):
        if valor > 0 and self._saldo >= valor:
            self._saldo -= valor
            return True
        return False


    def transferir(self, valor, conta_destino):
        if self.sacar(valor):
            if conta_destino.depositar(valor):
                return True
            # conta destino recusou o depósito (ex.: ContaSalario) -> desfaz o saque
            self._saldo += valor
            return False
        return False


    def exibir_dados(self):
        return (
            f"Tipo: Conta Bancária\n"
            f"Titular: {self._cliente.get_nome()}\n"
            f"Número: {self._numero}\n"
            f"Saldo: R$ {self._saldo:.2f}"
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




# CONTA CORRENTE




class ContaCorrente(ContaBancaria):
    def __init__(self, cliente, numero, saldo,
                 limite=500.0,
                 tarifa_mensal=20.0):


        super().__init__(cliente, numero, saldo)


        self.__limite = limite
        self.__tarifa_mensal = tarifa_mensal


    def get_limite_disponivel(self):
        limite_usado = max(0.0, -self._saldo)
        return self.__limite - limite_usado


    def sacar(self, valor):
        if valor <= 0:
            return False


        if valor <= self._saldo + self.__limite:
            self._saldo -= valor
            return True


        return False


    def cobrar_tarifa(self):
        return self.sacar(self.__tarifa_mensal)


    def exibir_dados(self):
        return (
            super().exibir_dados() +
            f"\nLimite disponível: R$ {self.get_limite_disponivel():.2f}"
        )


    def get_tipo_conta(self):
        return "Conta Corrente"




# CONTA POUPANÇA




class ContaPoupanca(ContaBancaria):


    def __init__(self, cliente, numero, saldo,
                 taxa_rendimento=0.01):


        super().__init__(cliente, numero, saldo)


        self.__taxa_rendimento = taxa_rendimento


    def render_juros(self):
        rendimento = self.get_saldo() * self.__taxa_rendimento
        self.depositar(rendimento)


    def exibir_dados(self):
        return (
            super().exibir_dados() +
            f"\nTaxa de rendimento: {self.__taxa_rendimento*100:.2f}%"
        )


    def get_tipo_conta(self):
        return "Conta Poupança"




# CONTA SALÁRIO




class ContaSalario(ContaBancaria):


    def __init__(self,
                 cliente,
                 numero,
                 saldo,
                 empresa="Empresa",
                 limite_saques=3):


        super().__init__(cliente, numero, saldo)


        self.__empresa = empresa
        self.__saques_realizados = 0
        self.__limite_saques = limite_saques


    def receber_salario(self, valor):
        if valor > 0:
            self._saldo += valor


    # depósito comum não permitido
    def depositar(self, valor):
        print("Conta salário não permite depósitos comuns.")
        return False


    def sacar(self, valor):


        if self.__saques_realizados >= self.__limite_saques:
            return False


        if super().sacar(valor):
            self.__saques_realizados += 1
            return True


        return False


    # transferência não permitida
    def transferir(self, valor, conta_destino):
        print("Conta salário não permite transferência para outra conta.")
        return False


    def exibir_dados(self):
        return (
            super().exibir_dados() +
            f"\nEmpresa: {self.__empresa}"
            f"\nSaques: {self.__saques_realizados}/{self.__limite_saques}"
        )


    def get_tipo_conta(self):
        return "Conta Salário"


AppBanco: 

import tkinter as tk
from tkinter import messagebox, simpledialog
from ContaBancaria import Endereco, ContaBancaria, Cliente, ContaCorrente, ContaPoupanca, ContaSalario






class BancoApp:
    def __init__(self, janela):
        self.janela = janela
        self.janela.title("Sistema Bancário - POO em Python")
        self.janela.geometry("850x400")




        end1 = Endereco("Rua Aviador", 1000, "Cohab", "Ceará-Mirim")
        end2 = Endereco("Rua Bonita", 123, "Centro", "Natal")
        end3 = Endereco("Rua Curricular", 456, "São Geraldo", "Ceará-Mirim")
        end4 = Endereco("Rua Centenárea", 426, "São Geraldo", "Ceará-Mirim")




        cliente1 = Cliente("Mateus", "100.200.300-04", end1)
        cliente2 = Cliente("Pedro", "111.222.333-44", end2)
        cliente3 = Cliente("Vitoria", "777.777.777-77", end3)
        cliente4 = Cliente("João", "222.222.222-22", end4)


        self.contas = [
            ContaCorrente(cliente1, "1002", 200.0),
            ContaCorrente(cliente2, "1003", 100.0),
            ContaPoupanca(cliente3, "1004", 150.0),
            ContaSalario(cliente4, "1006", 1718.0, "IFRN")
        ]


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
            btn_depositar.pack(pady=2)


            btn_sacar = tk.Button(
                frame,
                text="Sacar",
                width=15,
                command=lambda c=conta: self.sacar(c)
            )
            btn_sacar.pack(pady=2)


            btn_transferir = tk.Button(
                frame,
                text="Transferir",
                width=15,
                command=lambda c=conta: self.transferir(c)
            )
            btn_transferir.pack(pady=2)


            btn_dados = tk.Button(
                frame,
                text="Exibir Dados",
                width=15,
                command=lambda c=conta: self.exibir_dados(c)
            )
            btn_dados.pack(pady=2)


            btn_rendimento = tk.Button(
                frame,
                text="Render Juros",
                width=15,
                command=lambda c=conta: self.render_juros(c)
            )
            btn_rendimento.pack(pady=2)


            btn_taxa = tk.Button(
                frame,
                text="Cobrar Tarifa",
                width=15,
                command=lambda c=conta: self.cobrar_taxa(c)
            )
            btn_taxa.pack(pady=2)


    def depositar(self, conta):
        valor = simpledialog.askfloat("Depósito", "Digite o valor do depósito:")


        if valor is not None:
            saldo_antes = conta.get_saldo()
            conta.depositar(valor)


            if conta.get_saldo() > saldo_antes:
                messagebox.showinfo("Sucesso", "Depósito realizado.")
            else:
                messagebox.showerror(
                    "Erro",
                    "Valor inválido ou esta conta não permite depósitos comuns."
                )


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


        numero_destino = simpledialog.askstring(
            "Transferência",
            "Digite o número da conta destino:"
        )


        if numero_destino is None:
            return


        conta_destino = None


        for conta in self.contas:
            if conta.get_numero() == numero_destino.strip():
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
            messagebox.showerror("Erro", "Transferência não permitida, saldo insuficiente ou valor inválido.")


        self.atualizar_tela()


    def exibir_dados(self, conta):
        messagebox.showinfo("Dados da Conta", conta.exibir_dados())


    def render_juros(self, conta):
        if conta.get_tipo_conta() == "Conta Poupança":
            conta.render_juros()
            messagebox.showinfo("Sucesso", "Rendimento efetuado.")
            self.atualizar_tela()
        else:
            messagebox.showerror("Erro", "Conta não disponibiliza rendimento.")


    def cobrar_taxa(self, conta):
        if conta.get_tipo_conta() == "Conta Corrente":
            if conta.cobrar_tarifa():
                messagebox.showinfo("Sucesso", "Tarifa cobrada.")
            else:
                messagebox.showerror("Erro", "Saldo/limite insuficiente para cobrar a tarifa.")
            self.atualizar_tela()
        else:
            messagebox.showerror("Erro", "Cobrança inválida para essa conta.")






janela = tk.Tk()
app = BancoApp(janela)
janela.mainloop()
