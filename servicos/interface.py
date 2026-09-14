# servicos/interface.py

class InterfaceUsuario:
    @staticmethod
    def exibir_menu():
        """Exibe o painel visual do menu interativo via terminal."""
        print("\n=======================================")
        print("      SISTEMA DE GESTÃO RESTAURANTE     ")
        print("=======================================")
        print("1 - Abrir Nova Comanda")
        print("2 - Lançar Item na Comanda")
        print("3 - Consultar Consumo da Comanda")
        print("4 - Fechar e Pagar Comanda (Baixa FIFO)")
        print("5 - Abastecer Estoque (Novo Lote)")
        print("6 - Consultar Quantidade em Estoque")
        print("7 - Relatório Financeiro de Vendas")
        print("8 - Relatório de Consumo por Cliente")
        print("9 - Forçar Carga de Dados Falsos (Faker)")
        print("10 - Visualizar Cardápio do Restaurante")
        print("11 - Alterar Quantidade de um Item")
        print("0 - Salvar e Sair")
        print("=======================================")

    @staticmethod
    def exibir_painel_cardapio():
        """Exibe as opções de texto fixas do cardápio para guiar o usuário."""
        print("\n---------------------------------------")
        print("           CARDÁPIO DISPONÍVEL         ")
        print("---------------------------------------")
        print(" * hamburguer       * lanche natural  ")
        print(" * hot dog          * refrigerante    ")
        print(" * batata frita     * suco natural    ")
        print(" * agua mineral     * cerveja         ")
        print("---------------------------------------")
