# estruturas/no.py

class No:
    def __init__(self, conteudo):
        self.conteudo = conteudo  # Guarda o objeto (Comanda, Lote de Produto, etc.)
        self.proximo = None       # Ponteiro para o próximo nó
