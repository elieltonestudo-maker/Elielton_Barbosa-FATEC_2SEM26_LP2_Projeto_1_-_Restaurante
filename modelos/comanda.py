# modelos/comanda.py
from modelos.item_pedido import ItemPedido
from datetime import datetime

class Comanda:
    def __init__(self, numero, nome_cliente):
        # Número identificador da comanda (ex: número da mesa ou ficha)
        self.numero = int(numero)
        
        # Nome do cliente associado à comanda
        self.nome_cliente = nome_cliente
        
        # Carimba automaticamente a data e hora em que a comanda foi aberta no restaurante
        self.data_hora_abertura = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        
        # Ponteiro que indica o PRIMEIRO item pedido pelo cliente (Início da lista encadeada).
        # Começa como None porque a comanda é aberta vazia, sem nenhum consumo.
        self.primeiro_item = None 

    def adicionar_item(self, nome_produto, quantidade, preco_unitario):
        """Adiciona um item ao consumo. Se o item já existir, soma a quantidade."""
        # Cria um ponteiro auxiliar começando no primeiro item para varrer a lista
        atual = self.primeiro_item
        
        # PASSO 1: Percorre a lista para verificar se o cliente já pediu esse produto antes
        while atual is not None:
            if atual.nome_produto == nome_produto:
                # Se achou o mesmo produto, apenas soma a nova quantidade no nó existente
                atual.quantidade += int(quantidade)
                return  # Interrompe o método, pois o item foi atualizado
            atual = atual.proximo  # Avança para o próximo item da lista
        
        # PASSO 2: Se chegou aqui, significa que é um produto novo na comanda.
        # Instancia um novo nó de ItemPedido.
        novo_item = ItemPedido(nome_produto, quantidade, preco_unitario)
        
        # Faz o novo item apontar para o atual primeiro item da lista (insere no início)
        novo_item.proximo = self.primeiro_item
        
        # Atualiza o início da comanda para apontar para o novo item que acabou de ser criado
        self.primeiro_item = novo_item

    def remover_item(self, nome_produto):
        """Remove completamente um item da comanda antes do fechamento conta."""
        # Ponteiro para rastrear o item atual da busca
        atual = self.primeiro_item
        # Ponteiro para rastrear o item anterior (necessário para refazer o elo da lista)
        anterior = None
        
        # Varre a lista encadeada procurando o produto pelo nome
        while atual is not None:
            if atual.nome_produto == nome_produto:
                # CASO 1: O item a ser removido é o primeiro da lista
                if anterior is None:
                    self.primeiro_item = atual.proximo  # O início passa a ser o segundo item
                # CASO 2: O item está no meio ou no final da lista
                else:
                    anterior.proximo = atual.proximo  # O anterior pula o atual e conecta direto no próximo
                return True  # Indica que a remoção foi feita com sucesso
            
            # Avança os ponteiros para continuar a busca no próximo nó
            anterior = atual
            atual = atual.proximo
        return False  # Retorna Falso caso o item não tenha sido encontrado na comanda

    def calcular_total(self):
        """Percorre toda a lista encadeada somando o valor total consumido."""
        total = 0.0
        # Começa a varredura a partir do primeiro item pedido
        atual = self.primeiro_item
        
        # Percorre a lista acumulando os valores até chegar ao fim (None)
        while atual is not None:
            # Multiplica a quantidade solicitada pelo preço unitário daquele item
            total += atual.quantidade * atual.preco_unitario
            # Avança o ponteiro auxiliar para o próximo item
            atual = atual.proximo
            
        return total  # Retorna a soma total calculada manualmente
