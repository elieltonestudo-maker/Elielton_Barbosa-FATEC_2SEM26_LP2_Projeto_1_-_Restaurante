# servicos/gestor_estoque.py

from estruturas.no import No
from estruturas.fila_estoque import FilaEstoque
from modelos.produto import Produto

class NoEstoque:
    def __init__(self, nome_produto):
        self.nome_produto = nome_produto
        self.fila = FilaEstoque()
        self.proximo = None

class GestorEstoque:
    def __init__(self):
        self.produtos_estoque = None

    def _buscar_ou_criar_fila(self, nome_produto):
        atual = self.produtos_estoque
        anterior = None
        while atual is not None:
            if atual.nome_produto.lower() == nome_produto.lower():
                return atual.fila
            anterior = atual
            atual = atual.proximo
        novo_no_estoque = NoEstoque(nome_produto)
        if anterior is None:
            self.produtos_estoque = novo_no_estoque
        else:
            anterior.proximo = novo_no_estoque
        return novo_no_estoque.fila

    def abastecer_produto(self, nome, preco_compra, preco_venda, data_compra, data_vencimento, quantidade):
        novo_lote = Produto(nome, preco_compra, preco_venda, data_compra, data_vencimento, quantidade)
        fila = self._buscar_ou_criar_fila(nome)
        fila.enfileirar(novo_lote)

    def dar_baixa_itens(self, comanda):
        item_atual = comanda.primeiro_item
        while item_atual is not None:
            quantidade_necessaria = item_atual.quantidade
            fila = self._buscar_ou_criar_fila(item_atual.nome_produto)
            
            while quantidade_necessaria > 0:
                lote_atual = fila.inicio
                if lote_atual is None:
                    break
                    
                produto_lote = lote_atual.conteudo
                if produto_lote.quantidade <= quantidade_necessaria:
                    quantidade_necessaria -= produto_lote.quantidade
                    fila.desenfileirar()
            else:
                # O lote atual tem mais do que o necessário; apenas subtrai a quantidade
                produto_lote.quantidade -= quantidade_necessaria
                quantidade_necessaria = 0
                
        item_atual = item_atual.proximo

    def obter_quantidade_total(self, nome_produto):
        """Soma a quantidade disponível de todos os lotes ativos de um produto."""
        fila = self._buscar_ou_criar_fila(nome_produto)
        total = None
        atual = fila.inicio
        while atual is not None:
            total += atual.conteudo.quantidade
            atual = atual.proximo
        return total
