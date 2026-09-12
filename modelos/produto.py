# modelos/produto.py

class Produto:
    def __init__(self, nome, preco_compra, preco_venda, data_compra, data_vencimento, quantidade):
        # Nome do produto (ex: "Refrigerante Lata", "Hambúrguer")
        self.nome = nome
        
        # Preço pago pelo restaurante para adquirir o produto (convertido para número decimal)
        self.preco_compra = float(preco_compra)
        
        # Preço que o restaurante cobrará do cliente (convertido para número decimal)
        self.preco_venda = float(preco_venda)
        
        # Data em que o lote foi comprado/recebido
        self.data_compra = data_compra
        
        # Data de validade deste lote específico (fundamental para a regra do estoque)
        self.data_vencimento = data_vencimento
        
        # Quantidade de itens disponíveis neste lote específico
        self.quantidade = int(quantidade)
