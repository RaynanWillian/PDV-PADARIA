import sqlite3

# -----------------------
# BANCO DE DADOS
# -----------------------
conexao = sqlite3.connect("padaria.db")
cursor = conexao.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS produtos (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    codigo INTEGER NOT NULL UNIQUE,
    codigo_barras TEXT,
    nome TEXT NOT NULL,
    preco REAL NOT NULL,
    estoque INTEGER NOT NULL
)
""")

conexao.commit()
conexao.close()

print("Banco de dados criado com sucesso!")


# -----------------------
# FUNÇÕES
# -----------------------
def cadastrar_produto():
    codigo = int(input("Digite o código do produto: "))
    codigo_barras = input("Digite o código de barras do produto: ")
    nome = input("Digite o nome do produto: ")
    preco = float(input("Digite o preço do produto: "))
    estoque = int(input("Digite a quantidade em estoque: "))

    conexao = sqlite3.connect("padaria.db")
    cursor = conexao.cursor()

    cursor.execute("""
        INSERT INTO produtos (codigo, codigo_barras, nome, preco, estoque)
        VALUES (?, ?, ?, ?, ?)
    """, (codigo, codigo_barras, nome, preco, estoque))

    conexao.commit()
    conexao.close()

    print("\nProduto cadastrado com sucesso!")

def consultar_codigo_barras():
    codigo_barras = input("Digite o código de barras: ")

    conexao = sqlite3.connect("padaria.db")
    cursor = conexao.cursor()
    
    cursor.execute("""
        SELECT codigo, codigo_barras, nome, preco, estoque
        FROM produtos
        WHERE codigo_barras = ?
    """, (codigo_barras,))

    resultado = cursor.fetchone()
    if resultado is None:
        print("Não encontrado.")
    else:
        print("Produto: ", resultado[2])
        print("Código: ", resultado[0])
        print("Código de barras: ", resultado[1])
        print("Preço: ", resultado[3])
        print("Estoque: ", resultado[4])

    conexao.close()

def consultar_codigo_interno():
    codigo_interno = input("Digite o código interno: ")

    conexao = sqlite3.connect("padaria.db")
    cursor = conexao.cursor()

    cursor.execute("""
        SELECT codigo, codigo_barras, nome, preco, estoque
        FROM produtos
        WHERE codigo = ?
        """, (codigo_interno,))
    
    resultado = cursor.fetchone()
    if resultado is None:
        print("Não encontrado.")
    else:
        print("Produto: ", resultado[2])
        print("Código: ", resultado[0])
        print("Código de barras: ", resultado[1])
        print("Preço: ", resultado[3])
        print("Estoque: ", resultado[4])

    conexao.close()

# -----------------------
# MENU PRINCIPAL
# -----------------------
while True:
    print("\n==============================")
    print("      PDV DA PADARIA")
    print("==============================")
    print("1 - Cadastrar produto")
    print("2 - Consultar produto pelo código de barras")
    print("3 - Sair")

    opcao = input("\nEscolha uma opção: ")

    if opcao == "1":
        cadastrar_produto()

    elif opcao == "2":
        consultar_codigo_barras()    

    elif opcao == "3":
        print("Sistema encerrado.")
        break

    else:
        print("Opção inválida!")