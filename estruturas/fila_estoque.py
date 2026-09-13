# estruturas/fila_estoque.py

from estruturas.no import No

class FilaEstoque:
    def __init__(self):
        self.inicio = None      # Aponta para o lote mais antigo
        self.fim = None         # Aponta para o lote mais recente
        self.total_itens = 0

    def enfileirar(self, produto):
        """Adiciona um novo lote no fim da fila (reabastecimento)."""
        novo_no = No(produto)
        if self.fim is None:
            self.inicio = novo_no
            self.fim = novo_no
        else:
            self.fim.proximo = novo_no
            self.fim = novo_no
        self.total_itens += 1

    def desenfileirar(self):
        """Remove e retorna o lote mais antigo do início da fila (baixa por venda)."""
        if self.inicio is None:
            return None
        
        produto_removido = self.inicio.conteudo
        self.inicio = self.inicio.proximo
        
        if self.inicio is None:
            self.fim = None
            
        self.total_itens -= 1
        return produto_removido

    def esta_vazia(self):
        return self.total_itens == 0
