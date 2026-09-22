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
def consultar_produto():
    tipo_consulta = input("""
1 - Código interno
2 - Código de barras
    
    Escolha a opção: """)

    if tipo_consulta == "1":
        consultar_codigo_interno()

    elif tipo_consulta == "2":
       consultar_codigo_barras()

    else:
        print("Opção inválida.")

def alterar_produto():
    codigo = int(input("Digite o código do produto que deseja alterar: "))

    conexao = sqlite3.connect("padaria.db")
    cursor = conexao.cursor()

    cursor.execute("""
        SELECT codigo, codigo_barras, nome, preco, estoque
        FROM produtos
        WHERE codigo = ?
    """, (codigo,))

    resultado = cursor.fetchone()
    if resultado is None:
        print("Produto não encontrado.")
        conexao.close()
        return

    print("Produto encontrado:")
    print("Código: ", resultado[0])
    print("Código de barras: ", resultado[1])
    print("Nome: ", resultado[2])
    print("Preço: ", resultado[3])
    print("Estoque: ", resultado[4])

    novo_nome = input("Digite o novo nome do produto (deixe em branco para não alterar): ")
    novo_preco = input("Digite o novo preço do produto (deixe em branco para não alterar): ")
    novo_estoque = input("Digite a nova quantidade em estoque (deixe em branco para não alterar): ")

    if novo_nome:
        cursor.execute("""
            UPDATE produtos
            SET nome = ?
            WHERE codigo = ?
        """, (novo_nome, codigo))

    if novo_preco:
        cursor.execute("""
            UPDATE produtos
            SET preco = ?
            WHERE codigo = ?
        """, (float(novo_preco), codigo))

    if novo_estoque:
        cursor.execute("""
            UPDATE produtos
            SET estoque = ?
            WHERE codigo = ?
        """, (int(novo_estoque), codigo))

    conexao.commit()
    conexao.close()

    print("\nProduto alterado com sucesso!")

def excluir_produto():
    codigo = int(input("Digite o código do produto que deseja excluir: "))

    conexao = sqlite3.connect("padaria.db")
    cursor = conexao.cursor()

    cursor.execute("""
        SELECT codigo, codigo_barras, nome, preco, estoque
        FROM produtos
        WHERE codigo = ?
    """, (codigo,))

    resultado = cursor.fetchone()
    if resultado is None:
        print("Produto não encontrado.")
        conexao.close()
        return

    print("Produto encontrado:")
    print("Código: ", resultado[0])
    print("Código de barras: ", resultado[1])
    print("Nome: ", resultado[2])
    print("Preço: ", resultado[3])
    print("Estoque: ", resultado[4])

    confirmacao = input("Tem certeza que deseja excluir este produto? (s/n): ")
    if confirmacao.lower() == "s":
        cursor.execute("""
            DELETE FROM produtos
            WHERE codigo = ?
        """, (codigo,))
        conexao.commit()
        print("\nProduto excluído com sucesso!")
    else:
        print("\nExclusão cancelada.")

    conexao.close()

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
    print("2 - Consultar produto")
    print("3 - Alterar produto")
    print("4 - Excluir produto")
    print("5 - Sair")

    opcao = input("\nEscolha uma opção: ")

    if opcao == "1":
        cadastrar_produto()

    elif opcao == "2":
        consultar_produto()    

    elif opcao == "3":
        alterar_produto()

    elif opcao == "4":
        excluir_produto()

    elif opcao == "5":
        print("Sistema encerrado.")
        break

    else:
        print("Opção inválida!")