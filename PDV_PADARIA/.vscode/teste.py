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

#------------------------
# TABELA DE COMANDAS
#------------------------
cursor.execute("""
CREATE TABLE IF NOT EXISTS comandas (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    data_hora TEXT NOT NULL DEFAULT (datetime('now', 'localtime')),
    status TEXT NOT NULL DEFAULT 'ABERTA'
        CHECK (status IN ('ABERTA', 'PAGA', 'CANCELADA')),
    forma_pagamento TEXT
)
""")


#------------------------------
# TABELA DE ITENS DA COMANDA
#------------------------------
cursor.execute("""
CREATE TABLE IF NOT EXISTS itens_comanda (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    comanda_id INTEGER NOT NULL,
    produto_codigo INTEGER NOT NULL,
    nome_produto TEXT NOT NULL,
    quantidade INTEGER NOT NULL CHECK (quantidade > 0),
    preco_unitario REAL NOT NULL CHECK (preco_unitario >= 0),
    subtotal REAL NOT NULL,
    FOREIGN KEY (comanda_id) REFERENCES comandas(id)
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

    #1. Alterar o nome (opcional)
    novo_nome = input("Digite o novo nome do produto (deixe em branco para não alterar): ")

    #2. Validação do preço (opcional)
    while True:
        novo_preco = input("Digite o novo preço do produto (deixe em branco para não alterar): ").strip()
        
        if novo_preco == "":
            preco = None
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

    #3. Validação do estoque (obrigatório)
    while True:
        novo_estoque = input("Estoque é obrigatório. Por favor, digite um valor.").strip()
        
        try:
            estoque = int(novo_estoque)
        except ValueError:
            print("Estoque inválido. Por favor, digite apenas números inteiros.")
            continue

        if estoque < 0:
            print("Estoque inválido. Por favor, digite um valor maior ou igual a zero.")
            continue

        break

    #4. Salvar as alterações no banco de dados
    if novo_nome != "":
        cursor.execute("""
            UPDATE produtos
            SET nome = ?
            WHERE codigo = ?
        """, (novo_nome, codigo))

    if preco is not None:
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
        conexao.commit()
        conexao.close()

        print("\nProduto alterado com sucesso!")

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

def abrir_comanda():
    conexao = sqlite3.connect("padaria.db")
    cursor = conexao.cursor()

    # Criar uma nova comanda
    cursor.execute("""
        INSERT INTO comandas (status)
        VALUES ('ABERTA')
    """)

    comanda_id = cursor.lastrowid
    conexao.commit()

    print(f"\nComanda aberta com número: {comanda_id} aberta!")
    print("Digite o código para encerrar a inclusão de itens.")

    total = 0

    while True:
        codigo_digitado = input("\nDigite o código do produto (ou '0' para encerrar): ").strip()

        if codigo_digitado == "0":
            break

        try:
            codigo = int(codigo_digitado)

            if codigo <= 0:
                print("Digite um código válido ou 0 para encerrar.")
                continue

        except ValueError:
            print("Digite apenas números inteiros.")
            continue

        #Buscar o produto cadastrado
        cursor.execute("""
            SELECT codigo, nome, preco
            FROM produtos
            WHERE codigo = ?
            """, (codigo,))
        
        produto = cursor.fetchone()

        if produto is None:
            print("Produto não encontrado.")
            continue

        # Informar a quantidade
        while True:
            try:
                quantidade = int(input("Quantidade: "))

                if quantidade <= 0:
                    print("Digite uma quantidade maior que zero.")
                    continue
                break

            except ValueError:
                print("Digite apenas quantidae inteira válida.")

        codigo_produto, nome, preco = produto
        subtotal = round(preco * quantidade, 2)

        # Inserir o item na tabela itens_comanda
        cursor.execute("""
            INSERT INTO itens_comanda (
            comanda_id,
            produto_codigo,
            nome_produto,
            quantidade,
            preco_unitario,
            subtotal
            )
            VALUES (?, ?, ?, ?, ?, ?)
        """, (
            comanda_id,
            codigo_produto,
            nome, quantidade,
            preco,
            subtotal
        ))

        conexao.commit()
        total += subtotal

        print(f"Produto: {nome}")
        print(f"Subtotal: R$ {subtotal:.2f}")
        print(f"Total da comanda: R$ {total:.2f}")

    # Verificar se algum item foi adicionado à comanda
    cursor.execute("""
        SELECT COUNT(*)
        FROM itens_comanda
        WHERE comanda_id = ?
    """, (comanda_id,))

    quantidade_itens = cursor.fetchone()[0]
    if quantidade_itens == 0:
        cursor.execute("""
            UPDATE comandas
            SET status = 'CANCELADA'
            WHERE id = ?
        """, (comanda_id,))

        conexao.commit()
        print("\nComanda cancelada: Nenhum item foi adicionado à comanda.")

    else:
        print(f"\nComanda número {comanda_id} registrado!")
        print(f"Total da comanda: R$ {total:.2f}")
        print("Status: AGUARDANDO PAGAMENTO")

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
    print("5 - Abrir comanda")
    print("6 - Sair")

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
        abrir_comanda()

    elif opcao == "6":
        print("Saindo do programa...")
        break

    else:
        print("Opção inválida!")