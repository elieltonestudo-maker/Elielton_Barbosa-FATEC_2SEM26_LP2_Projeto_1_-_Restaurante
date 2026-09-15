# modelos/produto.py

class Produto:
    def __init__(self, nome, preco_compra, preco_venda, data_compra, data_vencimento, quantidade):
        self.nome = nome
        self.preco_compra = float(preco_compra)
        self.preco_venda = float(preco_venda)
        self.data_compra = data_compra
        self.data_vencimento = data_vencimento
        self.quantidade = int(quantidade) # quantidade do lote
