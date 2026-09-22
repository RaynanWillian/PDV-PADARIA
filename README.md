# PDV PADARIA

# 🥖 Sistema de PDV para Padaria

Sistema de **Ponto de Venda (PDV)** desenvolvido em **Python** e **SQLite**, criado para auxiliar no controle de produtos e no registro de vendas de uma padaria.

O projeto tem como objetivo aplicar, na prática, conceitos de programação, banco de dados e desenvolvimento de sistemas, além de atender a uma necessidade real de um pequeno negócio.

### 🚧 Status: Em desenvolvimento

## 📌 Sobre o projeto

Este projeto consiste no desenvolvimento de um sistema de PDV para uma padaria, permitindo o cadastro e a consulta de produtos e servindo como base para o registro e gerenciamento das vendas realizadas no estabelecimento.

O sistema utiliza SQLite para armazenamento dos dados, permitindo que as informações permaneçam salvas localmente sem a necessidade de configurar um servidor de banco de dados.

O projeto também está sendo desenvolvido de forma incremental, com novas funcionalidades sendo adicionadas conforme a necessidade do negócio.

## ⚙️ Funcionalidades
### Atualmente implementado

- [x] Criação automática do banco de dados SQLite

- [x] Criação da tabela de produtos

- [x] Cadastro de produtos

- [x] Consulta de produtos

- [x] Busca por código interno do produto

- [x] Busca por código de barras

- [x] Armazenamento de preço e estoque

- [x] Identificação única dos produtos

## 🚧 Em desenvolvimento / planejado

- Registro de vendas

- Cálculo automático do total da venda

- Seleção de produtos por código ou código de barras

- Controle de estoque após a venda

- Diferentes formas de pagamento

- Pagamento via Pix

- Pagamento em débito

- Pagamento em crédito parcelado

- Registro de data e horário das vendas

- Consulta do histórico de vendas

- Cancelamento e alteração de vendas

- Controle administrativo de estoque

- Abertura e fechamento de caixa

- Integração com leitor de código de barras

- Geração de comprovante de venda

## 🛠️ Tecnologias
- Python — linguagem principal do projeto
- SQLite — banco de dados local
- sqlite3 — biblioteca padrão do Python para comunicação com o SQLite
- Visual Studio Code — ambiente utilizado durante o desenvolvimento
- Git e GitHub — versionamento e armazenamento do código
- 📂 Estrutura do projeto

A estrutura pode evoluir conforme novas funcionalidades forem adicionadas.

PDV_PADARIA/
│
├── padaria.db
├── main.py
└── README.md

A estrutura acima representa a organização inicial do projeto e poderá ser modificada durante o desenvolvimento.

## 🚀 Instalação
### 1. Pré-requisitos

É necessário ter o Python 3 instalado no computador.

Verifique a instalação executando:

python --version

ou:

py --version
### 2. Clone o repositório

git clone https://github.com/SEU-USUARIO/SEU-REPOSITORIO.git

Entre na pasta do projeto:

cd PDV_PADARIA
### 3. Execute o sistema
python main.py

Caso o computador utilize o comando py:

py main.py

O banco de dados SQLite será utilizado localmente pelo sistema.


### 💻 Como usar

Após iniciar o programa, o usuário poderá utilizar as funcionalidades disponíveis no sistema.

Entre as operações atualmente disponíveis estão:

### 🔎 Consulta de produtos

O sistema permite localizar produtos utilizando:

Código interno;
Código de barras.

Os dados dos produtos são armazenados no banco de dados SQLite.

### 📦 Cadastro de produtos

Os produtos podem possuir informações como:

Campo	Descrição
id	Identificador interno
codigo	Código interno do produto
codigo_barras	Código de barras
nome	Nome do produto
preco	Preço de venda
estoque	Quantidade disponível
## 🗄️ Banco de dados

O projeto utiliza SQLite, um banco de dados relacional leve que permite armazenar as informações diretamente em um arquivo local.

A tabela principal utilizada atualmente é:

| campo | descrição |
|---|---|
| `id` | identificador único |
| `codigo` | código interno do produto |
| `codigo_barras` | código de barras |
| `nome` | nome do produto |
| `preco` | preço do produto |
| `estoque` | quatidade disponível |



O uso do SQLite foi escolhido por ser adequado para uma aplicação local de pequeno porte e por permitir trabalhar com banco de dados sem a necessidade de configurar um servidor externo.

## 🎯 Objetivos do projeto

Além de atender a uma necessidade real de uma padaria, este projeto tem como objetivos:

- Praticar desenvolvimento em Python;
- Aprender e aplicar conceitos de banco de dados;
- Trabalhar com operações CRUD;
- Desenvolver um sistema baseado em uma necessidade real;
- Praticar organização e manutenção de código;
- Utilizar Git e GitHub para versionamento;
- Evoluir gradualmente o projeto para um sistema de PDV mais completo.
- 🔮 Próximos passos

O projeto continuará sendo desenvolvido de acordo com as necessidades do estabelecimento.

Entre os próximos objetivos estão a implementação do registro completo de vendas, gerenciamento de estoque, formas de pagamento, histórico de vendas e gerenciamento do caixa.

## 👨‍💻 Desenvolvedor

Desenvolvido por **Raynan Willian** como projeto prático de desenvolvimento de software e aplicação de conhecimentos adquiridos durante a graduação em Análise e Desenvolvimento de Sistemas.

## 📄 Licença

Este projeto está em desenvolvimento e, no momento, não possui uma licença definida.