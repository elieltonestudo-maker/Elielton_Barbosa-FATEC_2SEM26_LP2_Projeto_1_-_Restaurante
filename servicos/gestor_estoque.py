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
        """Busca a fila de um produto convertendo o argumento para minusculo."""
        nome_busca = nome_produto.lower()  # Converte o nome do produto para minúsculas para busca
        atual = self.produtos_estoque
        anterior = None
        while atual is not None:
            # Compara o nome salvo com o nome da busca (ambos em minusculo)
            if atual.nome_produto.lower() == nome_busca:
                return atual.fila
            anterior = atual
            atual = atual.proximo
        # Se não encontrou, cria um novo nó para o produto e adiciona no início da lista
        novo_no_estoque = NoEstoque(nome_busca)
        if anterior is None:
            self.produtos_estoque = novo_no_estoque
        else:
            anterior.proximo = novo_no_estoque
        return novo_no_estoque.fila

    def abastecer_produto(self, nome, preco_compra, preco_venda, data_compra, data_vencimento, quantidade):
        # Garante que o nome do produto seja registrado sempre em minúsculo no lote
        novo_lote = Produto(nome.lower(), preco_compra, preco_venda, data_compra, data_vencimento, quantidade)
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
                    # CORREÇÃO: O else agora está perfeitamente indentado dentro do while interno
                    produto_lote.quantidade -= quantidade_necessaria
                    quantidade_necessaria = 0
            
            # CORREÇÃO: Esta linha avançava incorretamente fora do laço principal, travando o sistema
            item_atual = item_atual.proximo

    def obter_quantidade_total(self, nome_produto):
        """Soma a quantidade disponível de todos os lotes ativos de um produto."""
        fila = self._buscar_ou_criar_fila(nome_produto)
        total = 0  # CORREÇÃO: Inicializado com 0 para permitir operações matemáticas simples
        atual = fila.inicio
        while atual is not None:
            total += atual.conteudo.quantidade
            atual = atual.proximo
        return total
