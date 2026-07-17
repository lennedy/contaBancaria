import tkinter as tk
from tkinter import messagebox, simpledialog
from Classes import Cliente, ContaBancaria, Endereço, ContaCorrente

class BancoApp:
def __init__(self, janela):
self.janela = janela
self.janela.title("Caixa economico - POO em Python")
self.janela.geometry("850x400")
self.janela.configure(background="#a4d16d")
endereço1 = Endereço("Rua das Flores", 25, "Centro", "Natal")
endereço2 = Endereço("Avenida Brasil", 100, "Jardim América", "Recife")
cliente1 = Cliente("Carlos", "123.456.789-00", endereço1)
cliente2 = Cliente("Mariana", "987.654.321-00", endereço2)
self.contas = [
ContaCorrente(cliente1, 1001, 500, 100, 10),
ContaBancaria(cliente2, 1002, 1000)
]
self.criar_interface()
def criar_interface(self):
titulo = tk.Label(
self.janela,
text="Caixa economico - Contas Bancárias",
font=("Arial", 18, "bold"),
background="#cbf09e"
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
pady=10,
background="#7bb337"
)
frame.pack(side="left", padx=10, pady=10)
lbl_titular = tk.Label(
frame,
text=conta.get_titular(),
font=("Arial", 14, "bold"),
background="#cbf09e"
)
lbl_titular.pack()
lbl_numero = tk.Label(
frame,
text=f"Conta: {conta.get_numero()}",
background="#cbf09e"
)
lbl_numero.pack()
lbl_saldo = tk.Label(
frame,
text=f"Saldo: R$ {conta.get_saldo():.2f}",
font=("Arial", 12),
background="#cbf09e"
)
lbl_saldo.pack(pady=5)
btn_depositar = tk.Button(
frame,
text="Depositar",
width=15,
background="#a4d16d",
command=lambda c=conta: self.depositar(c)
)
btn_depositar.pack(pady=2)
btn_sacar = tk.Button(
frame,
text="Sacar",
width=15,
background="#a4d16d",
command=lambda c=conta: self.sacar(c)
)
btn_sacar.pack(pady=2)

btn_transferir = tk.Button(
frame,
text="Transferir",
width=15,
background="#a4d16d",
command=lambda c=conta: self.transferir(c)
)
btn_transferir.pack(pady=2)
btn_dados = tk.Button(
frame,
text="Exibir Dados",
width=15,
background="#a4d16d",
command=lambda c=conta: self.exibir_dados(c)
)
btn_dados.pack(pady=2)
btn_rendimento = tk.Button(
frame,
text="Render Juros",
width=15,
background="#a4d16d",
command=lambda c=conta: self.render_juros(c)
)
btn_rendimento.pack(pady=2)
btn_taxa = tk.Button(
frame,
text="Cobrar Taxa",
width=15,
background="#a4d16d",
command=lambda c=conta: self.cobrar_taxa(c)
)
btn_taxa.pack(pady=2)