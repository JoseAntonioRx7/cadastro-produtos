# Cadastro de Clientes e Pedidos

Um sistema desktop simples e direto para o gerenciamento de clientes, produtos e pedidos. Construído com interface gráfica nativa do Python e banco de dados relacional local, é ideal para pequenos controles de vendas, dispensando configurações complexas de infraestrutura.

![Interface do Sistema](image_552258.png)

## 🚀 Funcionalidades

*   **Gestão de Clientes:** Cadastro de novos clientes com validação de campos obrigatórios e prevenção contra e-mails duplicados.
*   **Gestão de Produtos:** Inserção de produtos no catálogo com seus respectivos preços (suporte à formatação monetária).
*   **Registro de Pedidos:** Associação em interface fluida entre clientes cadastrados e produtos disponíveis, controlando a quantidade desejada através de menus suspensos (Combobox).
*   **Visualização em Tempo Real:** Tabelas dinâmicas (Treeview) que exibem e atualizam instantaneamente os registros de clientes, produtos e pedidos.
*   **Relatórios Integrados:** Cálculo automático do total vendido agrupado por produto, acessível através da aba superior de navegação.
*   **Controle de Dados:** Botão de emergência para apagar todos os registros do banco de dados simultaneamente (protegido por pop-up de confirmação).

## 💻 Tecnologias Utilizadas

Este projeto foi desenvolvido utilizando exclusivamente a biblioteca padrão do Python, garantindo alta portabilidade.

*   **Linguagem:** Python 3.x
*   **Interface Gráfica (GUI):** Tkinter
*   **Banco de Dados:** SQLite3 (banco de dados embutido em arquivo local)

## 🗄️ Estrutura do Banco de Dados

Ao rodar o sistema pela primeira vez, um arquivo chamado `cadastro.db` é gerado automaticamente na raiz do projeto. Ele opera sob a seguinte modelagem relacional:

1.  **`clientes`**: `id` (Primary Key), `nome`, `email` (Unique), `telefone`.
2.  **`produtos`**: `id` (Primary Key), `nome`, `preco`.
3.  **`pedidos`**: `id` (Primary Key), `cliente_id` (Foreign Key), `produto_id` (Foreign Key), `quantidade`.

## ⚙️ Como Executar

1.  Certifique-se de ter o **Python** instalado no seu sistema operativo.
2.  Faça o clone deste repositório ou o download do arquivo de código.
3.  Nenhuma instalação de dependência externa via `pip` é necessária.
4.  Abra o terminal no diretório do projeto e execute:
    ```bash
    python nome_do_arquivo.py
    ```
    *(Substitua `nome_do_arquivo.py` pelo nome real do seu script, como `main.py` ou `app.py`).*

## 👨‍💻 Autor

Desenvolvido por **José Antônio**
📧 [ramosjoseantonio254@gmail.com](mailto:ramosjoseantonio254@gmail.com)

<img width="1040" height="1000" alt="image" src="https://github.com/user-attachments/assets/69e5ac2b-3fd5-4ce5-b670-cf13645976f2" />
