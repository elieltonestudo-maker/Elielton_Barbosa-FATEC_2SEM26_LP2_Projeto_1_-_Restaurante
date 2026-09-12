# modelos/item_pedido.py

class ItemPedido:
    def __init__(self, nome_produto, quantidade, preco_unitario):
        # Nome do produto consumido pelo cliente
        self.nome_produto = nome_produto
        
        # Quantidade que o cliente pediu deste item específico
        self.quantidade = int(quantidade)
        
        # Preço de venda praticado no momento do pedido
        self.preco_unitario = float(preco_unitario)
        
        # Ponteiro/Referência que aponta para o PRÓXIMO item que o cliente pediu.
        # Começa como None pois é inserido um item por vez.
        self.proximo = None 
