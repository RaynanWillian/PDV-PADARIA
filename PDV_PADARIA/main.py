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
    estoque INTEGER NOT NULL,
    tipo_controle TEXT NOT NULL DEFAULT 'UNIDADE',
    CHECK (tipo_controle IN ('UNIDADE', 'SEM_CONTROLE'))
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

def consultar_codigo_barras():
    # validar o código de barras
        codigo_barras = input("Digite o código de barras: ").strip()

        if codigo_barras =="":
            print("Consulta cancelada.")
            return
        
        conexao = sqlite3.connect("padaria.db")
        cursor = conexao.cursor()
    
        cursor.execute("""
            SELECT codigo, codigo_barras, nome, preco, estoque
            FROM produtos
            WHERE codigo_barras = ?
        """, (codigo_barras,))

        resultado = cursor.fetchone()
        if resultado is None:
            print("Esse código de barras não encontrado.")
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

def alterar_produto():
    while True:
        try:
            codigo = int(input("Digite o código do produto que deseja alterar: "))
            break
        except ValueError:
            print("Código inválido. Por favor, digite apenas números.")

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

    while True:
        novo_preco = input("Digite o novo preço do produto (deixe em branco para não alterar): ").strip()
        #Validação do preço
        if novo_preco == "":
            break

        try:
            preco = float(novo_preco.replace(",", "."))
        except ValueError:
            print("Preço inválido. Por favor, digite apenas números.")
            continue

        if preco <= 0:
            print("Preço inválido. Por favor, digite um valor maior que zero.")
            continue
        break

    novo_estoque = input("Digite a nova quantidade em estoque (deixe em branco para não alterar): ").strip()

    estoque = None
    
    if novo_preco != "":
        try:
            estoque = int(novo_estoque)
        except ValueError:
            print("Estoque inválido. Por favor, digite apenas números inteiros.")
            conexao.close()
            return

        if estoque < 0:
            print("Estoque inválido. Por favor, digite um valor maior ou igual a zero.")
            conexao.close()
            return
    
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
        """, (preco, codigo))

    if estoque is not None:
        cursor.execute("""
        UPDATE produtos
        SET estoque = ?
        WHERE codigo = ?
        """, (estoque, codigo))

def excluir_produto():
    while True:
        try:
            codigo = int(input("Digite o código do produto que deseja excluir: "))
            break
        except ValueError:
            print("Código inválido. Por favor, digite apenas números.")

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
    # 1. Validar o código interno
    while True:
        try:
            codigo = int(input("Digite o código do produto: "))
        except ValueError:
            print("Digite apenas números inteiros.")
            continue

        if codigo <= 0:
            print("Digite um número positivo.")
            continue

        conexao = sqlite3.connect("padaria.db")
        cursor = conexao.cursor()

        cursor.execute(
            "SELECT codigo FROM produtos WHERE codigo = ?",
            (codigo,)
        )
        resultado = cursor.fetchone()
        conexao.close()

        if resultado is not None:
            print("Esse código já está cadastrado. Use outro.")
            continue

        break

    # 2. Validar o código de barras
    while True:
        codigo_barras = input(
            "Digite o código de barras (ou Enter para deixar vazio): "
        ).strip()

        if codigo_barras == "":
            codigo_barras = None
            break

        conexao = sqlite3.connect("padaria.db")
        cursor = conexao.cursor()

        cursor.execute(
            "SELECT codigo FROM produtos WHERE codigo_barras = ?",
            (codigo_barras,)
        )
        resultado = cursor.fetchone()
        conexao.close()

        if resultado is not None:
            print("Esse código de barras já está cadastrado.")
            continue

        break

    # 3. Validar o nome
    while True:
        nome = input("Digite o nome do produto: ").strip()

        if not nome:
            print("O nome não pode ficar vazio.")
            continue

        break

    # 4. Validar o preço
    while True:
        try:
            preco = float(
                input("Digite o preço do produto: ").replace(",", ".")
            )
        except ValueError:
            print("Digite um preço válido, como 10,50.")
            continue

        if preco <= 0:
            print("O preço deve ser maior que zero.")
            continue

        break

    # 5. Validar o estoque
    while True:
        try:
            estoque = int(input("Digite a quantidade em estoque: "))
        except ValueError:
            print("Digite uma quantidade inteira.")
            continue

        if estoque < 0:
            print("O estoque não pode ser negativo.")
            continue

        break

    # 6. Salvar no banco de dados
    conexao = sqlite3.connect("padaria.db")
    cursor = conexao.cursor()

    try:
        cursor.execute("""
            INSERT INTO produtos
                (codigo, codigo_barras, nome, preco, estoque)
            VALUES (?, ?, ?, ?, ?)
        """, (codigo, codigo_barras, nome, preco, estoque))

        conexao.commit()
        print("\nProduto cadastrado com sucesso!")

    except sqlite3.IntegrityError:
        print("Erro: esse código interno já está cadastrado.")

    finally:
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