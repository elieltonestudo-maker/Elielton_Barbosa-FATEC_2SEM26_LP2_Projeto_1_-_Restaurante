# modelos/comanda.py
from modelos.item_pedido import ItemPedido
from datetime import datetime

class Comanda:
    def __init__(self, numero, nome_cliente):
        self.numero = int(numero)
        self.nome_cliente = nome_cliente
        self.data_hora_abertura = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        self.primeiro_item = None 

    def adicionar_item(self, nome_produto, quantidade, preco_unitario):
        """Adiciona um item ao consumo. Se o item já existir, soma a quantidade."""
        # Força o nome do produto recebido a ficar em minúsculas para a comparação
        nome_padronizado = nome_produto.lower().strip()
        atual = self.primeiro_item
        
        # PASSO 1: Percorre a lista comparando tudo em minúsculas
        while atual is not None:
            if atual.nome_produto.lower().strip() == nome_padronizado:
                atual.quantidade += int(quantidade)
                return  
            atual = atual.proximo  
        
        # PASSO 2: Se é um produto novo, insere no início da lista salvando em minúsculo
        novo_item = ItemPedido(nome_padronizado, int(quantidade), float(preco_unitario))
        novo_item.proximo = self.primeiro_item
        self.primeiro_item = novo_item

    def remover_item(self, nome_produto):
        """Remove completamente um item da comanda antes do fechamento."""
        nome_padronizado = nome_produto.lower().strip()
        atual = self.primeiro_item
        anterior = None
        
        while atual is not None:
            if atual.nome_produto.lower().strip() == nome_padronizado:
                if anterior is None:
                    self.primeiro_item = atual.proximo  
                else:
                    anterior.proximo = atual.proximo  
                return True  
            anterior = atual
            atual = atual.proximo
        return False  

    def calcular_total(self):
        """Percorre toda a lista encadeada somando o valor total consumido."""
        total = 0.0
        atual = self.primeiro_item
        while atual is not None:
            total += atual.quantidade * atual.preco_unitario
            atual = atual.proximo
        return total  
