# estruturas/fila_estoque.py

from estruturas.no import No

class FilaEstoque:
    def __init__(self):
        self.inicio = None      # vaip/ lote mais antigo
        self.fim = None         # vai p/ lote mais recente
        self.total_itens = 0

    def enfileirar(self, produto):
        # bota o lote novo no fim da fila
        novo_no = No(produto)
        if self.fim is None:
            self.inicio = novo_no
            self.fim = novo_no
        else:
            self.fim.proximo = novo_no
            self.fim = novo_no
        self.total_itens += 1

    def desenfileirar(self):
        # tira o mais antigo do comeco
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

    def esta_vazia(self):
        return self.total_itens == 0

    
    '''Rascunho do método FEFO (por vencimento).    
    --->> Para fazer a mudança para o FeFo:

     1-Passo: começe retirando o comentario do metodo enfileirar_por_vencimento (self, produto) nesse arquivo logo abaixo dessa explicação.,

     2-Passo: vá até o arquivo servicos/gestor_estoque.py e substitua a chamada 'fila.enfileirar(novo_lote)' 
     por esta 'fila.enfileirar_por_vencimento(novo_lote)'

       abaixo no método 'abastecer_produto' do GestorEstoque.

     3-Rode o programa e faça testes de abastecimento.  
    
    '''
    

    '''def enfileirar_por_vencimento(self, produto):
        """Insere o novo lote na posição correta da fila ordenada por vencimento."""
        novo_no = No(produto)
        from datetime import datetime
        venc_novo = datetime.strptime(produto.data_vencimento, "%d/%m/%Y")
        
        if self.inicio is None or venc_novo < datetime.strptime(self.inicio.conteudo.data_vencimento, "%d/%m/%Y"):
            novo_no.proximo = self.inicio
            self.inicio = novo_no
            if self.fim is None:
                self.fim = novo_no
            self.total_itens += 1
            return

        atual = self.inicio
        while atual.proximo is not None and datetime.strptime(atual.proximo.conteudo.data_vencimento, "%d/%m/%Y") <= venc_novo:
            atual = atual.proximo
            
        novo_no.proximo = atual.proximo
        atual.proximo = novo_no
        if novo_no.proximo is None:
            self.fim = novo_no
            
        self.total_itens += 1

#'''
