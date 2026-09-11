# Sistema de Gestão de Restaurante 🍽️

Este projeto consiste em um sistema de gestão de estoque, comandas e pagamentos desenvolvido como requisito avaliativo para as disciplinas de **Estrutura de Dados** e **Linguagem de Programação 2** da **Fatec Rio Claro**.

O objetivo principal é aplicar os conceitos de Orientação a Objetos e estruturas de dados dinâmicas personalizadas, sem a utilização de coleções nativas estruturais da linguagem (como listas ou dicionários embutidos) para a lógica principal do negócio.

---

## 🛠️ Funcionalidades do Sistema

- **Controle de Comandas:** Abertura por cliente, inserção e remoção dinâmica de itens (refeições e bebidas) antes do fechamento.
- **Controle de Estoque:** Armazenamento de lotes perecíveis contendo nome, preços de compra/venda, datas e quantidade.
- **Regra FIFO (PEPS):** Prioridade automática de saída para os produtos com data de compra mais antiga (lotes mais velhos).
- **Controle de Pagamento:** Fechamento de comandas aceitando PIX, Cartão, Dinheiro e modalidade de "Confiança".
- **Persistência de Dados:** Armazenamento não volátil e carregamento do estado do sistema através da biblioteca `pickle`.
- **Simulação com Dados Falsos:** Geração automática de registros aleatórios para testes rápidos utilizando a biblioteca `Faker`.
- **Relatórios:** Emissão de relatórios detalhados de vendas e consumo.

---

## 🏗️ Estruturas de Dados Customizadas

Para atender às restrições do projeto e exercitar o encapsulamento, foram desenvolvidas as seguintes estruturas manuais baseadas em nós (`No`):
1. **Fila Dinâmica (`FilaEstoque`):** Utilizada no controle de estoque para garantir a saída sequencial correta dos produtos perecíveis.
2. **Lista Encadeada (`ListaComandas`):** Utilizada para gerenciar dinamicamente as comandas abertas e os itens vinculados a cada uma delas.

---

## 📁 Estrutura do Projeto

```text
├── estruturas/         # Implementação manual de No, Fila e Lista
├── modelos/            # Classes de domínio (Produto, Comanda, Pagamento)
├── servicos/           # Regras de negócio (GerenciadorEstoque, Caixa)
├── main.py             # Menu interativo do sistema
└── README.md           # Documentação do projeto
```

---

## 🚀 Como Executar o Projeto

1. Certifique-se de ter o Python 3 instalado.
2. Instale as dependências necessárias:
   ```bash
   pip install faker
   ```
3. Execute o arquivo principal:
   ```bash
   python main.py
   ```

---

## 🧑‍💻 Desenvolvedor
- **Nome:** Elielton Barbosa
- **Instituição:** Fatec Rio Claro
- **Data de Apresentação:** 17/09/2026 às 07h50
