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
    
    def exibir_cardapio(self):
        """Varre a lista encadeada de estoques e mostra os produtos cadastrados e seus preços."""
        print("\n" + "-"*40)
        print("         --- CARDÁPIO DO DIA ---        ")
        print("-"*40)
        
        atual = self.produtos_estoque
        contagem = 0
        
        while atual is not None:
            # Pega o primeiro lote da fila para espiar o preço de venda atual do produto
            fila_produto = atual.fila
            if fila_produto.inicio is not None:
                preco_venda = fila_produto.inicio.conteudo.preco_venda
                # Formata a primeira letra em maiúscula apenas na hora de exibir na tela (.capitalize())
                print(f" * {atual.nome_produto.capitalize():<20} | R$ {preco_venda:.2f}")
                contagem += 1
            atual = atual.proximo
            
        if contagem == 0:
            print("Nenhum produto cadastrado no cardápio até o momento.")
        print("-"*40)
