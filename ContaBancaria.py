import tkinter as tk
from tkinter import messagebox, simpledialog
from BancoApp import Endereco, ContaBancaria, Cliente, ContaCorrente, ContaPoupanca, ContaSalario

class BancoApp:
    def __init__(self, janela):
        self.janela = janela
        self.janela.title("Sistema Bancário - POO em Python")
        self.janela.geometry("850x400")


        end1 = Endereco("Rua 1", 1000, "Centro", "Ceará-Mirim")
        end2 = Endereco("Rua 2", 2000, "Mini-Centro", "São-Gonçalo")
        end3 = Endereco("Rua 3", 3000, "Assentamento 3", "Ceará-Mirim")
        end4 = Endereco("Rua 4", 4000, "Planalto", "Parnamirim")


        cliente1 = Cliente("Helo", "00.000.000.-00", end1)
        cliente2 = Cliente("Joshua", "111.111.111-11", end2)
        cliente3 = Cliente("Clara", "222.222.222-22", end3)
        cliente4 = Cliente("Laura", "333.333.333-33", end4)

        self.contas = [
            ContaCorrente(cliente1, "1002", 200.0),
            ContaCorrente(cliente2, "1003", 300.0),
            ContaPoupanca(cliente3, "1004", 400.0),
            ContaSalario(cliente4, "1005", 500.0)
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