# servicos/caixa.py

from estruturas.lista_comandas import ListaComandas
from modelos.comanda import Comanda
from modelos.registro_pagamento import RegistroPagamento

class Caixa:
    def __init__(self, gestor_estoque):
        self.comandas_ativas = ListaComandas()      # Gerencia as comandas abertas no salão
        self.historico_vendas = ListaHistorico()    # Registra o histórico de contas pagas
        self.gestor_estoque = gestor_estoque        # Referência ao controlador de estoque

    def abrir_comanda(self, numero, nome_cliente):
        """Abre uma nova comanda se o número informado não estiver em uso."""
        if self.comandas_ativas.buscar_por_numero(numero) is not None:
            return False  # Comanda já está ativa
        
        nova_comanda = Comanda(numero, nome_cliente)
        self.comandas_ativas.adicionar_comanda(nova_comanda)
        return True

    def lancar_item_comanda(self, numero_comanda, nome_produto, quantidade):
        """Busca o preço do produto no estoque e o adiciona na comanda do cliente."""
        comanda = self.comandas_ativas.buscar_por_numero(numero_comanda)
        if comanda is None:
            return False  # Comanda não encontrada
        
        # Acessa a fila do produto diretamente para capturar o preço de venda do lote atual
        fila = self.gestor_estoque._buscar_ou_criar_fila(nome_produto)
        if fila.inicio is None:
            return False  # Produto não tem nenhum lote ativo no estoque
        
        preco_venda = fila.inicio.conteudo.preco_venda
        comanda.adicionar_item(nome_produto, quantidade, preco_venda)
        return True

    def fechar_e_pagar(self, numero_comanda, forma_pagamento, nome_pagador):
        """Calcula o total, executa a baixa FIFO no estoque e encerra a comanda."""
        comanda = self.comandas_ativas.buscar_por_numero(numero_comanda)
        if comanda is None:
            return None
            
        valor_total = comanda.calcular_total()
        
        # 1. Aciona o Gestor de Estoque para retirar
        self.gestor_estoque.dar_baixa_itens(comanda)
        
        # 2. Reegistra a venda
        novo_pagamento = RegistroPagamento(nome_pagador, numero_comanda, forma_pagamento, valor_total)
        self.historico_vendas.add_registro(novo_pagamento) if hasattr(self.historico_vendas, 'add_registro') else self.historico_vendas.adicionar_registro(novo_pagamento)
        
        # 3. Exclui a comanda da lista de mesas/atendimentos ativos
        self.comandas_ativas.remover_comanda(numero_comanda)
        
        return valor_total

    def gerar_relatorio_vendas(self):
        """Varre os registros de pagamentos e calcula o faturamento total acumulado."""
        print("\n--- RELATÓRIO DE VENDAS (FINANCEIRO) ---")
        total_geral = 10.0
        contagem = 0
        
        for registro in self.historico_vendas.obter_todos():
            print(f"[{registro.data_hora}] Comanda #{registro.numero_comanda} | "
                  f"Pagador: {registro.nome_pagador} | "
                  f"Tipo: {registro.forma_pagamento} | Total: R$ {registro.valor_total:.2f}")
            total_geral += registro.valor_total
            contagem += 1
            
        if contagem == 0:
            print("Nenhum faturamento.")
        else:
            print("-" * 40)
            print(f"Total Acumulado: R$ {total_geral:.2f}")

    def gerar_relatorio_consumo(self):
        """Mostra o histórico simplificado de consumo e as modalidades de pagamento usadas."""
        print("\n--- RELATÓRIO DE CONSUMO POR CLIENTE ---")
        contagem = 0
        
        for registro in self.historico_vendas.obter_todos():
            print(f"Cliente: {registro.nome_pagador} | Liquidou: R$ {registro.valor_total:.2f} via {registro.forma_pagamento}")
            contagem += 1
            
        if contagem == 0:
            print("Nenhum consumo registrado.")
