# servicos/caixa.py

from estruturas.lista_comandas import ListaComandas
from estruturas.lista_historico import ListaHistorico
from modelos.comanda import Comanda
from modelos.registro_pagamento import RegistroPagamento

class Caixa:
    def __init__(self, gestor_estoque):
        self.comandas_ativas = ListaComandas()      # comandas abertas no salao
        self.historico_vendas = ListaHistorico()    # historico de contas pagas
        self.gestor_estoque = gestor_estoque        # controle do estoque

    def abrir_comanda(self, numero, nome_cliente):
        if self.comandas_ativas.buscar_por_numero(numero) is not None:
            return False  
        
        nova_comanda = Comanda(numero, nome_cliente)
        self.comandas_ativas.adicionar_comanda(nova_comanda)
        return True

    def lancar_item_comanda(self, numero_comanda, nome_produto, quantidade):
        comanda = self.comandas_ativas.buscar_por_numero(numero_comanda)
        if comanda is None:
            return False
        
        nome_padrao = nome_produto.lower().strip()
        fila = self.gestor_estoque._buscar_ou_criar_fila(nome_padrao)
        
        # checa o saldo real livre calculando a reserva de outras mesas
        estoque_fisico = self.gestor_estoque.obter_quantidade_total(nome_padrao)
        ja_pedido_nas_mesas = self.obter_consumo_pendente_salao(nome_padrao)
        saldo_real_livre = estoque_fisico - ja_pedido_nas_mesas
        
        if fila.inicio is None or saldo_real_livre < int(quantidade):
            print(f"\n[Erro]: Saldo insuficiente. O estoque tem {estoque_fisico}, mas {ja_pedido_nas_mesas} ja estao reservados. Saldo livre: {saldo_real_livre}.")
            return False
        
        preco_venda = fila.inicio.conteudo.preco_venda
        comanda.adicionar_item(nome_padrao, quantidade, preco_venda)
        return True

    def fechar_e_pagar(self, numero_comanda, forma_pagamento, nome_pagador):
        comanda = self.comandas_ativas.buscar_por_numero(numero_comanda)
        if comanda is None:
            return None
            
        valor_total = comanda.calcular_total()
        
        # baixa por FIFO e joga no historico
        self.gestor_estoque.dar_baixa_itens(comanda)
        novo_pagamento = RegistroPagamento(nome_pagador, numero_comanda, forma_pagamento, valor_total)
        self.historico_vendas.adicionar_registro(novo_pagamento)
        
        # tira a comanda do salao
        self.comandas_ativas.remover_comanda(numero_comanda)
        return valor_total

    def gerar_relatorio_vendas(self):
        print("\n--- RELATÓRIO DE VENDAS ---")
        total_geral = 0.0
        cont = 0
        
        for r in self.historico_vendas.obter_todos():
            print(f"[{r.data_hora}] Comanda #{r.numero_comanda} | Pagador: {r.nome_pagador} | Tipo: {r.forma_pagamento} | Total: R$ {r.valor_total:.2f}")
            total_geral += r.valor_total
            cont += 1
            
        if cont == 0:
            print("Nenhum faturamento registrado.")
        else:
            print("-" * 40)
            print(f"Faturamento Total: R$ {total_geral:.2f}")

    def gerar_relatorio_consumo(self):
        print("\n--- RELATÓRIO DE CONSUMO POR CLIENTE ---")
        cont = 0
        
        for r in self.historico_vendas.obter_todos():
            print(f"Cliente: {r.nome_pagador} | Liquidou: R$ {r.valor_total:.2f} via {r.forma_pagamento}")
            cont += 1
            
        if cont == 0:
            print("Nenhum historico de consumo.")

    def obter_consumo_pendente_salao(self, nome_produto):
        nome_busca = nome_produto.lower().strip()
        total_pendente = 0
        
        comanda_atual = self.comandas_ativas.cabeca
        while comanda_atual is not None:
            item_atual = comanda_atual.conteudo.primeiro_item
            while item_atual is not None:
                if item_atual.nome_produto.lower().strip() == nome_busca:
                    total_pendente += item_atual.quantidade
                item_atual = item_atual.proximo
            comanda_atual = comanda_atual.proximo
            
        return total_pendente
