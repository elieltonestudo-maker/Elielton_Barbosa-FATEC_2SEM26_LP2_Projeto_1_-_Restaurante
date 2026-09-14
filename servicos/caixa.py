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
        """Busca o preço do produto no estoque com trava de saldo reservado real."""
        comanda = self.comandas_ativas.buscar_por_numero(numero_comanda)
        if comanda is None:
            return False
        
        nome_padrao = nome_produto.lower().strip()
        fila = self.gestor_estoque._buscar_ou_criar_fila(nome_padrao)
        
        # CALCULO DE SEGURANÇA BANCÁRIA:
        estoque_fisico = self.gestor_estoque.obter_quantidade_total(nome_padrao)
        ja_pedido_nas_mesas = self.obter_consumo_pendente_salao(nome_padrao)
        saldo_real_livre = estoque_fisico - ja_pedido_nas_mesas
        
        # Se o que o cliente quer agora for maior do que o saldo real livre, bloqueia!
        if fila.inicio is None or saldo_real_livre < int(quantidade):
            print(f"\n[Bloqueado]: Saldo insuficiente! Estoque possui {estoque_fisico}, mas {ja_pedido_nas_mesas} ja estao reservados em comandas abertas. Saldo livre: {saldo_real_livre}.")
            return False
        
        preco_venda = fila.inicio.conteudo.preco_venda
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

    def obter_consumo_pendente_salao(self, nome_produto):
        """Varre todas as comandas abertas somando a quantidade ja pedida de um produto."""
        nome_busca = nome_produto.lower().strip()
        total_pendente = 0
        
        # Percorre a lista encadeada de comandas ativas
        comanda_atual = self.comandas_ativas.cabeca
        while comanda_atual is not None:
            # Percorre a lista encadeada de itens daquela comanda
            item_atual = comanda_atual.conteudo.primeiro_item
            while item_atual is not None:
                if item_atual.nome_produto.lower().strip() == nome_busca:
                    total_pendente += item_atual.quantidade
                item_atual = item_atual.proximo
            comanda_atual = comanda_atual.proximo
            
        return total_pendente
