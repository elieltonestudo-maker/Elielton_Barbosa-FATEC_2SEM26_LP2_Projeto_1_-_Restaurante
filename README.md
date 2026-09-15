# Sistema de Gestão de Restaurante 🍽️

Este projeto consiste em um sistema de gestão de estoque, comandas e pagamentos desenvolvido como requisito avaliativo para as disciplinas de **Estrutura de Dados** e **Linguagem de Programação 2** da **Fatec Rio Claro**.

O objetivo principal é aplicar os conceitos de Orientação a Objetos e estruturas de dados dinâmicas personalizadas, sem a utilização de coleções nativas estruturais da linguagem (como listas ou dicionários embutidos) para a lógica principal do negócio.

---

## 🛠️ Funcionalidades do Sistema

- **Controle de Comandas:** Abertura por cliente, inserção e remoção dinâmica de itens antes do fechamento.
- **Controle de Estoque:** Armazenamento de lotes perecíveis contendo nome, preços de compra/venda, datas e quantidade.
- **Regra FIFO (PEPS):** Prioridade automática de saída para os produtos com data de compra mais antiga (lotes mais velhos).
- **Controle de Pagamento:** Fechamento de comandas aceitando PIX, Cartão, Dinheiro e modalidade de "Confiança".
- **Persistência de Dados:** Armazenamento não volátil e carregamento do estado do sistema através da biblioteca `pickle`.
- **Simulação com Dados Falsos:** Geração automática de registros aleatórios para testes rápidos utilizando a biblioteca `Faker`.
- **Relatórios:** Emissão de relatórios detalhados de vendas e consumo.

---

## 🧠 Diferenciais Técnicos e Usabilidade (Homologados)

- **Arquitetura Visual Isolada:** Separação estrita de responsabilidades (SoC) com a criação da classe `InterfaceUsuario` para gerenciar menus e painéis textuais, limpando o fluxo de controle do `main.py`.
- **Cálculo de Saldo Reservado Líquido:** O sistema não consulta apenas os lotes físicos; ele calcula em tempo real o saldo disponível subtraindo o consumo pendente nas comandas abertas do salão, evitando vendas duplicadas.
- **Suporte Completo a Case-Insensitive:** O sistema realiza a busca de nomes padronizados em minúsculas (`.lower().strip()`). O usuário pode digitar `HAMBURGUER`, `Hamburguer` ou `hamburguer` que o sistema reconhece e processa perfeitamente.
- **Travas de Segurança:** Validação em tempo real para impedir o lançamento de produtos que não existem no cardápio ou que ultrapassem o limite de estoque disponível.
- **Feedback Visual Avançado:** Exibição detalhada de itens em consumo durante alterações (Opção 11) e do nome do cliente em tempo real na tela ao selecionar a comanda para lançamento ou fechamento.
- **Robustez:** Tratamento de exceções com blocos `try/except` para impedir o fechamento repentino do terminal por digitação inválida (letras em campos de números).
- **Preparação para Extensão FEFO (PVPS):** Embora o escopo exija a ordenação cronológica de compras (FIFO), a estrutura de armazenamento foi projetada para suportar a transição para a política FEFO (First Expired, First Out). O código para conversão da estrutura em uma Fila de Prioridades Ordenada por Vencimento encontra-se mapeado e documentado nativamente no módulo de infraestrutura (estruturas/fila_estoque.py e servicos/gestor_estoque.py).

---

## 🏗️ Estruturas de Dados Customizadas

Para atender às restrições do projeto e exercitar o encapsulamento, foram desenvolvidas as seguintes estruturas manuais baseadas em nós (`No`):
1. **Fila Dinâmica (`FilaEstoque`):** Utilizada no controle de estoque para garantir a saída sequencial correta dos produtos perecíveis.
2. **Lista Encadeada (`ListaComandas`):** Utilizada para gerenciar dinamicamente as comandas abertas e os itens vinculados a cada uma delas.
3. **Lista Encadeada (`ListaHistorico`):** Utilizada para armazenar de forma sequencial o histórico permanente de comprovantes de pagamentos.

---

## 📁 Estrutura do Projeto

```text
├── estruturas/         # Implementação manual de No, Fila e Listas (comandas e histórico)
├── modelos/            # Classes de domínio (Produto, Comanda, ItemPedido, RegistroPagamento)
├── servicos/           # Regras de negócio (GestorEstoque, Caixa, InterfaceUsuario)
├── .gitignore          # Proteção para ignorar arquivos locais (.venv, dados.pkl e caches)
├── main.py             # Menu interativo do sistema via terminal
├── README.md           # Documentação do projeto
└── requirements.txt    # Lista de dependências automatizadas para a faculdade
```

---

## 🚀 Como Executar o Projeto

Siga os passos abaixo para rodar o sistema utilizando um ambiente virtual isolado local:

### Pré-requisitos
- [Python 3.10+](https://www.python.org/downloads/) instalado
- [Git](https://git-scm.com/downloads) instalado

### Passo a passo

1. **Clone o repositório e entre na pasta:**
   ```bash
   git clone https://github.com/elieltonestudo-maker/Elielton_Barbosa-FATEC_2SEM26_LP2_Projeto_1_-_Restaurante.git
   cd Elielton_Barbosa-FATEC_2SEM26_LP2_Projeto_1_-_Restaurante
   ```

2. **Crie o ambiente virtual:**
   ```bash
   python -m venv .venv
   ```

3. **Ative o ambiente virtual conforme o seu sistema:**
   - **Windows (PowerShell):**
     ```powershell
     .\.venv\Scripts\Activate.ps1
     ```
   - **Windows (Git Bash):**
     ```bash
     source .venv/Scripts/activate
     ```
   - **Linux / Mac:**
     ```bash
     source .venv/bin/activate
     ```

   > ⚠️ **Se der erro de permissão no PowerShell**, execute uma vez:
   > ```powershell
   > Set-ExecutionPolicy -Scope CurrentUser -ExecutionPolicy RemoteSigned
   > ```

4. **Instale as dependências:**
   ```bash
   pip install -r requirements.txt
   ```

5. **Execute o programa:**
   ```bash
   python main.py
   ```

> 💡 **Dica:** sempre ative o ambiente virtual (`.venv`) antes de executar `python main.py`,
> caso contrário as dependências instaladas não serão encontradas.


---

## 🧑‍💻 Desenvolvedor
- **Nome:** Elielton Barbosa
- **Instituição:** Fatec Rio Claro
- **Data de Apresentação:** 17/09/2026 às 07h50

---

## 📊 Roteiro Sugerido para Teste e Validação 

Para comprovar o funcionamento de todas as regras de negócio e o controle das estruturas dinâmicas manuais, sugere-se seguir o seguinte roteiro no terminal:

1. **Verificar os Clientes Automáticos (`Opção 3`):** 
   - Escolha a opção `3` e digite o número `1`. Você verá o primeiro cliente aleatório gerado pelo *Faker*.
   - Repita a consulta para as comandas `2` e `3`. O sistema provará que gerou **nomes diferentes**, mas que todos iniciam com **1x hambúrguer** lançado na conta para testar o fluxo.

2. **Auditar as Reservas no Estoque (`Opção 6`):**
   - Escolha a opção `6` e consulte o produto `hamburguer`. 
   - O painel exibirá que existem **3 unidades reservadas nas mesas** (1 de cada cliente ativo), demonstrando o cálculo de saldo líquido em tempo real antes da baixa física.

3. **Demonstrar a Baixa FIFO (`Opção 4`):**
   - Escolha a opção `4` e faça o fechamento da comanda `1`.
   - Volte na opção `6` e consulte o `hamburguer` novamente. Você verá que o lote mais antigo decrementou fisicamente, provando o funcionamento da estrutura `FilaEstoque` (PEPS).

4. **Testar a Extensão FEFO (Carta na Manga):**
   - Os módulos `fila_estoque.py` e `gestor_estoque.py` contêm a lógica de ordenação por prioridade de vencimento (FEFO) comentada nativamente, pronta para ser ativada caso seja solicitado pelo professor Orlando.
