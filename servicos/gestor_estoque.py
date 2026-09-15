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
        nome_busca = nome_produto.lower().strip()
        atual = self.produtos_estoque
        anterior = None
        
        while atual is not None:
            if atual.nome_produto.lower().strip() == nome_busca:
                return atual.fila
            anterior = atual
            atual = atual.proximo
            
        novo_no_estoque = NoEstoque(nome_busca)
        if anterior is None:
            self.produtos_estoque = novo_no_estoque
        else:
            anterior.proximo = novo_no_estoque
        return novo_no_estoque.fila

    def abastecer_produto(self, nome, preco_compra, preco_venda, data_compra, data_vencimento, quantidade):
        novo_lote = Produto(nome.lower().strip(), preco_compra, preco_venda, data_compra, data_vencimento, quantidade)
        fila = self._buscar_ou_criar_fila(nome)
        fila.enfileirar(novo_lote)
        #fila.enfileirar_por_vencimento(novo_lote)  # <------- Para usar o método FEFO, descomente esta linha e comente a linha acima

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
                    produto_lote.quantidade -= quantidade_necessaria
                    quantidade_necessaria = 0
            
            item_atual = item_atual.proximo

    def obter_quantidade_total(self, nome_produto):
        fila = self._buscar_ou_criar_fila(nome_produto)
        total = 0  
        atual = fila.inicio
        while atual is not None:
            total += atual.conteudo.quantidade
            atual = atual.proximo
        return total
    
    def exibir_cardapio(self):
        print("\n" + "-"*40)
        print("         --- CARDÁPIO DO DIA ---        ")
        print("-"*40)
        
        atual = self.produtos_estoque
        contagem = 0
        
        while atual is not None:
            fila_produto = atual.fila
            if fila_produto.inicio is not None:
                preco_venda = fila_produto.inicio.conteudo.preco_venda
                print(f" * {atual.nome_produto.capitalize():<20} | R$ {preco_venda:.2f}")
                contagem += 1
            atual = atual.proximo
            
        if contagem == 0:
            print("Nenhum produto cadastrado no cardápio até o momento.")
        print("-"*40)
