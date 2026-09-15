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
        nome_limpo = nome_produto.lower().strip()
        atual = self.primeiro_item
        
        # ve se ja tem na lista para somar
        while atual is not None:
            if atual.nome_produto.lower().strip() == nome_limpo:
                atual.quantidade += int(quantidade)
                return  
            atual = atual.proximo  
        
        # insere na comeco se for produto novo
        novo_item = ItemPedido(nome_limpo, int(quantidade), float(preco_unitario))
        novo_item.proximo = self.primeiro_item
        self.primeiro_item = novo_item

    def remover_item(self, nome_produto):
        nome_limpo = nome_produto.lower().strip()
        atual = self.primeiro_item
        anterior = None
        
        # remove mudando os ponteiros
        while atual is not None:
            if atual.nome_produto.lower().strip() == nome_limpo:
                if anterior is None:
                    self.primeiro_item = atual.proximo  
                else:
                    anterior.proximo = atual.proximo  
                return True  
            anterior = atual
            atual = atual.proximo
        return False  

    def calcular_total(self):
        # soma o total dos itens
        total = 0.0
        atual = self.primeiro_item
        while atual is not None:
            total += atual.quantidade * atual.preco_unitario
            atual = atual.proximo
        return total  
