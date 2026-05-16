import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3

DB_PATH = "cadastro.db"


def conectar_banco():
    conexao = sqlite3.connect(DB_PATH)
    cursor = conexao.cursor()
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS clientes(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL,
            email TEXT UNIQUE NOT NULL,
            telefone TEXT
        )
        """
    )
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS produtos(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL,
            preco REAL NOT NULL
        )
        """
    )
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS pedidos(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            cliente_id INTEGER NOT NULL,
            produto_id INTEGER NOT NULL,
            quantidade INTEGER NOT NULL,
            FOREIGN KEY(cliente_id) REFERENCES clientes(id),
            FOREIGN KEY(produto_id) REFERENCES produtos(id)
        )
        """
    )
    conexao.commit()
    return conexao, cursor


def formatar_preco(valor):
    return f"R$ {valor:,.2f}".replace(".", ",")


def validar_campo(texto, nome_campo):
    if not texto.strip():
        messagebox.showerror("Erro", f"O campo '{nome_campo}' é obrigatório.")
        return False
    return True


def carregar_clientes():
    for item in tree_clientes.get_children():
        tree_clientes.delete(item)
    cursor.execute("SELECT id, nome, email, telefone FROM clientes ORDER BY nome")
    for registro in cursor.fetchall():
        tree_clientes.insert("", tk.END, values=registro)


def carregar_produtos():
    for item in tree_produtos.get_children():
        tree_produtos.delete(item)
    cursor.execute(
        """
        SELECT pr.id, pr.nome, pr.preco,
            COALESCE(SUM(pr.preco * p.quantidade), 0) AS total_vendido
        FROM produtos pr
        LEFT JOIN pedidos p ON p.produto_id = pr.id
        GROUP BY pr.id, pr.nome, pr.preco
        ORDER BY pr.nome
        """
    )
    for registro in cursor.fetchall():
        tree_produtos.insert(
            "",
            tk.END,
            values=(
                registro[0],
                registro[1],
                formatar_preco(registro[2]),
                formatar_preco(registro[3]),
            ),
        )


def carregar_pedidos():
    for item in tree_pedidos.get_children():
        tree_pedidos.delete(item)
    cursor.execute(
        """
        SELECT p.id, c.nome, pr.nome, p.quantidade
        FROM pedidos p
        JOIN clientes c ON p.cliente_id = c.id
        JOIN produtos pr ON p.produto_id = pr.id
        ORDER BY p.id
        """
    )
    for registro in cursor.fetchall():
        tree_pedidos.insert("", tk.END, values=registro)


def atualizar_comboboxes():
    cursor.execute("SELECT id, nome FROM clientes ORDER BY nome")
    clientes = cursor.fetchall()
    clientes_display = [f"{registro[0]} - {registro[1]}" for registro in clientes]
    combo_cliente["values"] = clientes_display

    cursor.execute("SELECT id, nome FROM produtos ORDER BY nome")
    produtos = cursor.fetchall()
    produtos_display = [f"{registro[0]} - {registro[1]}" for registro in produtos]
    combo_produto["values"] = produtos_display


def limpar_inputs_cliente():
    entry_nome.delete(0, tk.END)
    entry_email.delete(0, tk.END)
    entry_telefone.delete(0, tk.END)


def limpar_inputs_produto():
    entry_nome_produto.delete(0, tk.END)
    entry_preco_produto.delete(0, tk.END)


def limpar_inputs_pedido():
    combo_cliente.set("")
    combo_produto.set("")
    entry_quantidade.delete(0, tk.END)


def salvar_cliente():
    nome = entry_nome.get().strip()
    email = entry_email.get().strip()
    telefone = entry_telefone.get().strip()
    if not validar_campo(nome, "Nome") or not validar_campo(email, "Email"):
        return
    try:
        cursor.execute(
            "INSERT INTO clientes (nome, email, telefone) VALUES (?, ?, ?)",
            (nome, email, telefone),
        )
        conexao.commit()
        messagebox.showinfo("Sucesso", "Cliente cadastrado com sucesso.")
        limpar_inputs_cliente()
        carregar_clientes()
        atualizar_comboboxes()
    except sqlite3.IntegrityError:
        messagebox.showerror("Erro", "Email já cadastrado. Use um email diferente.")


def salvar_produto():
    nome = entry_nome_produto.get().strip()
    preco_texto = entry_preco_produto.get().strip().replace(",", ".")
    if not validar_campo(nome, "Nome do produto") or not validar_campo(preco_texto, "Preço"):
        return
    try:
        preco = float(preco_texto)
    except ValueError:
        messagebox.showerror("Erro", "Preço inválido. Use números como 12.50 ou 12,50.")
        return
    cursor.execute(
        "INSERT INTO produtos (nome, preco) VALUES (?, ?)",
        (nome, preco),
    )
    conexao.commit()
    messagebox.showinfo("Sucesso", "Produto cadastrado com sucesso.")
    limpar_inputs_produto()
    carregar_produtos()
    atualizar_comboboxes()


def salvar_pedido():
    cliente_selecionado = combo_cliente.get().strip()
    produto_selecionado = combo_produto.get().strip()
    quantidade_texto = entry_quantidade.get().strip()
    if not validar_campo(cliente_selecionado, "Cliente") or not validar_campo(produto_selecionado, "Produto") or not validar_campo(quantidade_texto, "Quantidade"):
        return
    try:
        quantidade = int(quantidade_texto)
        if quantidade <= 0:
            raise ValueError
    except ValueError:
        messagebox.showerror("Erro", "Quantidade precisa ser um número inteiro maior que zero.")
        return
    cliente_id = int(cliente_selecionado.split(" - ")[0])
    produto_id = int(produto_selecionado.split(" - ")[0])
    cursor.execute(
        "INSERT INTO pedidos (cliente_id, produto_id, quantidade) VALUES (?, ?, ?)",
        (cliente_id, produto_id, quantidade),
    )
    conexao.commit()
    messagebox.showinfo("Sucesso", "Pedido registrado com sucesso.")
    limpar_inputs_pedido()
    carregar_pedidos()


def apagar_todos_registros():
    resposta = messagebox.askyesno(
        "Confirmar exclusão",
        "Isso irá apagar TODOS os clientes, produtos e pedidos. Deseja continuar?",
    )
    if not resposta:
        return
    cursor.execute("DELETE FROM pedidos")
    cursor.execute("DELETE FROM clientes")
    cursor.execute("DELETE FROM produtos")
    conexao.commit()
    carregar_clientes()
    carregar_produtos()
    carregar_pedidos()
    atualizar_comboboxes()
    messagebox.showinfo("Feito", "Todos os registros foram removidos.")


def mostrar_sobre():
    messagebox.showinfo(
        "Sobre",
        "Nome: Luiz Felipe Barbachan, Jose Antonio, Arthur Vinicius \n"
        "Titulo: Cadastro de Clientes e Pedidos\n"
        "Descrição: Aplicação para gerenciar clientes, produtos e pedidos usando Tkinter e SQLite."
    )


def fechar_aplicacao():
    conexao.close()
    raiz.destroy()


if __name__ == "__main__":
    conexao, cursor = conectar_banco()
    raiz = tk.Tk()
    raiz.title("Cadastro de Clientes e Pedidos")
    raiz.geometry("980x900")
    raiz.resizable(False, False)

    menubar = tk.Menu(raiz)
    ajuda_menu = tk.Menu(menubar, tearoff=0)
    ajuda_menu.add_command(label="Sobre", command=mostrar_sobre)
    ajuda_menu.add_separator()
    ajuda_menu.add_command(label="Sair", command=fechar_aplicacao)
    menubar.add_cascade(label="Ajuda", menu=ajuda_menu)
    raiz.config(menu=menubar)

    frame_cadastros = tk.Frame(raiz, padx=10, pady=10)
    frame_cadastros.pack(fill="x")

    frame_cliente = tk.LabelFrame(frame_cadastros, text="Cadastro de Clientes", padx=10, pady=10)
    frame_cliente.grid(row=0, column=0, padx=5, pady=5, sticky="nsew")

    tk.Label(frame_cliente, text="Nome:").grid(row=0, column=0, sticky="w")
    entry_nome = tk.Entry(frame_cliente, width=40)
    entry_nome.grid(row=0, column=1, pady=5, sticky="w")

    tk.Label(frame_cliente, text="Email:").grid(row=1, column=0, sticky="w")
    entry_email = tk.Entry(frame_cliente, width=40)
    entry_email.grid(row=1, column=1, pady=5, sticky="w")

    tk.Label(frame_cliente, text="Telefone:").grid(row=2, column=0, sticky="w")
    entry_telefone = tk.Entry(frame_cliente, width=40)
    entry_telefone.grid(row=2, column=1, pady=5, sticky="w")

    tk.Button(frame_cliente, text="Salvar Cliente", width=18, command=salvar_cliente).grid(row=3, column=0, columnspan=2, pady=10)

    frame_produto = tk.LabelFrame(frame_cadastros, text="Cadastro de Produtos", padx=10, pady=10)
    frame_produto.grid(row=0, column=1, padx=5, pady=5, sticky="nsew")

    tk.Label(frame_produto, text="Nome:").grid(row=0, column=0, sticky="w")
    entry_nome_produto = tk.Entry(frame_produto, width=35)
    entry_nome_produto.grid(row=0, column=1, pady=5, sticky="w")

    tk.Label(frame_produto, text="Preço (R$):").grid(row=1, column=0, sticky="w")
    entry_preco_produto = tk.Entry(frame_produto, width=35)
    entry_preco_produto.grid(row=1, column=1, pady=5, sticky="w")

    tk.Button(frame_produto, text="Salvar Produto", width=18, command=salvar_produto).grid(row=2, column=0, columnspan=2, pady=10)

    frame_pedido = tk.LabelFrame(raiz, text="Registrar Pedido", padx=10, pady=10)
    frame_pedido.pack(fill="x", padx=10, pady=5)

    tk.Label(frame_pedido, text="Cliente:").grid(row=0, column=0, sticky="w")
    combo_cliente = ttk.Combobox(frame_pedido, width=40, state="readonly")
    combo_cliente.grid(row=0, column=1, pady=5, sticky="w")

    tk.Label(frame_pedido, text="Produto:").grid(row=1, column=0, sticky="w")
    combo_produto = ttk.Combobox(frame_pedido, width=40, state="readonly")
    combo_produto.grid(row=1, column=1, pady=5, sticky="w")

    tk.Label(frame_pedido, text="Quantidade:").grid(row=2, column=0, sticky="w")
    entry_quantidade = tk.Entry(frame_pedido, width=10)
    entry_quantidade.grid(row=2, column=1, pady=5, sticky="w")

    tk.Button(frame_pedido, text="Salvar Pedido", width=18, command=salvar_pedido).grid(row=3, column=0, columnspan=2, pady=10)

    frame_botoes = tk.Frame(raiz, padx=10, pady=5)
    frame_botoes.pack(fill="x")
    tk.Button(frame_botoes, text="Apagar todos registros", command=apagar_todos_registros, fg="red").pack(side="right")

    frame_listas = tk.Frame(raiz, padx=10, pady=10)
    frame_listas.pack(fill="both", expand=True)

    frame_lista_clientes = tk.LabelFrame(frame_listas, text="Clientes Cadastrados", padx=5, pady=5)
    frame_lista_clientes.grid(row=0, column=0, padx=5, pady=5, sticky="nsew")

    frame_lista_produtos = tk.LabelFrame(frame_listas, text="Produtos Cadastrados", padx=5, pady=5)
    frame_lista_produtos.grid(row=0, column=1, padx=5, pady=5, sticky="nsew")

    frame_lista_pedidos = tk.LabelFrame(frame_listas, text="Pedidos Registrados", padx=5, pady=5)
    frame_lista_pedidos.grid(row=1, column=0, columnspan=2, padx=5, pady=5, sticky="nsew")

    frame_listas.grid_rowconfigure(0, weight=1)
    frame_listas.grid_rowconfigure(1, weight=1)
    frame_listas.grid_columnconfigure(0, weight=1)
    frame_listas.grid_columnconfigure(1, weight=1)

    col_clientes = ("ID", "Nome", "Email", "Telefone")
    tree_clientes = ttk.Treeview(frame_lista_clientes, columns=col_clientes, show="headings", height=8)
    for coluna in col_clientes:
        tree_clientes.heading(coluna, text=coluna)
    tree_clientes.column("ID", width=40, anchor="center")
    tree_clientes.column("Nome", width=180)
    tree_clientes.column("Email", width=180)
    tree_clientes.column("Telefone", width=120)
    tree_clientes.pack(fill="both", expand=True)

    col_produtos = ("ID", "Nome", "Preço")
    tree_produtos = ttk.Treeview(frame_lista_produtos, columns=col_produtos, show="headings", height=8)
    for coluna in col_produtos:
        tree_produtos.heading(coluna, text=coluna)
    tree_produtos.column("ID", width=40, anchor="center")
    tree_produtos.column("Nome", width=220)
    tree_produtos.column("Preço", width=100, anchor="e")
    tree_produtos.pack(fill="both", expand=True)

    col_pedidos = ("ID", "Cliente", "Produto", "Quantidade")
    tree_pedidos = ttk.Treeview(frame_lista_pedidos, columns=col_pedidos, show="headings", height=8)
    for coluna in col_pedidos:
        tree_pedidos.heading(coluna, text=coluna)
    tree_pedidos.column("ID", width=40, anchor="center")
    tree_pedidos.column("Cliente", width=250)
    tree_pedidos.column("Produto", width=250)
    tree_pedidos.column("Quantidade", width=100, anchor="center")
    tree_pedidos.pack(fill="both", expand=True)

    carregar_clientes()
    carregar_produtos()
    carregar_pedidos()
    atualizar_comboboxes()

    raiz.protocol("WM_DELETE_WINDOW", fechar_aplicacao)
    raiz.mainloop()

