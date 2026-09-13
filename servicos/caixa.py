# servicos/caixa.py

from estruturas.lista_comandas import ListaComandas
from estruturas.lista_historico import ListaHistorico
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
        """Busca o preço do produto no estoque e o adiciona na comanda do cliente com trava de segurança."""
        comanda = self.comandas_ativas.buscar_por_numero(numero_comanda)
        if comanda is None:
            return False  # Comanda não encontrada
        
        # PADRONIZAÇÃO: Força o nome do produto a ficar em minúsculo antes de buscar a fila
        nome_padrao = nome_produto.lower().strip()
        fila = self.gestor_estoque._buscar_ou_criar_fila(nome_padrao)
        
        # --- TRAVA DE SEGURANÇA REAL ---
        # Se o produto não possui nenhum lote ou se a quantidade total no estoque for 0
        if fila.inicio is None or self.gestor_estoque.obter_quantidade_total(nome_padrao) <= 0:
            print(f"\n[Bloqueado]: O produto '{nome_produto}' nao existe no cardapio ou esta esgotado!")
            return False  # Rejeita o lançamento e impede que entre na comanda
        
        preco_venda = fila.inicio.conteudo.preco_venda
        
        # Adiciona o item na comanda de forma encadeada apenas se passou na trava
        comanda.adicionar_item(nome_padrao, quantidade, preco_venda)
        return True

    def fechar_e_pagar(self, numero_comanda, forma_pagamento, nome_pagador):
        """Calcula o total, executa a baixa FIFO no estoque e encerra a comanda."""
        comanda = self.comandas_ativas.buscar_por_numero(numero_comanda)
        if comanda is None:
            return None
            
        valor_total = comanda.calcular_total()
        
        # 1. Aciona o Gestor de Estoque para decrementar as quantidades dos lotes corretos
        self.gestor_estoque.dar_baixa_itens(comanda)
        
        # 2. Cria o registro definitivo da venda para persistência e relatórios
        novo_pagamento = RegistroPagamento(nome_pagador, numero_comanda, forma_pagamento, valor_total)
        
        if hasattr(self.historico_vendas, 'adicionar_registro'):
            self.historico_vendas.adicionar_registro(novo_pagamento)
        else:
            self.historico_vendas.add_registro(novo_pagamento)
        
        # 3. Exclui a comanda da lista de mesas/atendimentos ativos
        self.comandas_ativas.remover_comanda(numero_comanda)
        
        return valor_total

    def gerar_relatorio_vendas(self):
        """Varre os registros de pagamentos e calcula o faturamento total acumulado."""
        print("\n--- RELATÓRIO DE VENDAS (FINANCEIRO) ---")
        total_geral = 0.0
        contagem = 0
        
        for registro in self.historico_vendas.obter_todos():
            print(f"[{registro.data_hora}] Comanda # {registro.numero_comanda} | "
                  f"Pagador: {registro.nome_pagador} | "
                  f"Tipo: {registro.forma_pagamento} | Total: R$ {registro.valor_total:.2f}")
            total_geral += registro.valor_total
            contagem += 1
            
        if contagem == 0:
            print("Nenhum faturamento registrado até o momento.")
        else:
            print("-" * 40)
            print(f"Faturamento Total Acumulado: R$ {total_geral:.2f}")

    def gerar_relatorio_consumo(self):
        """Mostra o histórico simplificado de consumo e as modalidades de pagamento usadas."""
        print("\n--- RELATÓRIO DE CONSUMO POR CLIENTE ---")
        contagem = 0
        
        for registro in self.historico_vendas.obter_todos():
            print(f"Cliente: {registro.nome_pagador} | Liquidou: R$ {registro.valor_total:.2f} via {registro.forma_pagamento}")
            contagem += 1
            
        if contagem == 0:
            print("Nenhum histórico de consumo registrado.")
