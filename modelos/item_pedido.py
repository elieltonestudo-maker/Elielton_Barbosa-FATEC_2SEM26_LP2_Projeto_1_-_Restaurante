# modelos/item_pedido.py

class ItemPedido:
    def __init__(self, nome_produto, quantidade, preco_unitario):
        # produto consumido pelo cliente
        self.nome_produto = nome_produto
        
        # Quantidade pdida pelo cliente
        self.quantidade = int(quantidade)
        
        # Preço de venda 
        self.preco_unitario = float(preco_unitario)                
        self.proximo = None # aponta para o próximo item
        
