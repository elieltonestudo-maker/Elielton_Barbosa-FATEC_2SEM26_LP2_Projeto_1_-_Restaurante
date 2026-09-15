# estruturas/lista_comandas.py

from estruturas.no import No

class ListaComandas:
    def __init__(self):
        self.cabeca = None  # lista as comandas ativas

    def adicionar_comanda(self, comanda):
        # cria uma comanda nna lista de cmoandas        
        novo_no = No(comanda)
        novo_no.proximo = self.cabeca
        self.cabeca = novo_no

    def buscar_por_numero(self, numero_comanda):
        # buca a comanda pelo numero 
        atual = self.cabeca
        while atual is not None:
            if atual.conteudo.numero == int(numero_comanda):
                return atual.conteudo
            atual = atual.proximo
        return None

    def remover_comanda(self, numero_comanda):
        # exclui a comandoa fechamento do caixa
        atual = self.cabeca
        anterior = None
        
        while atual is not None:
            if atual.conteudo.numero == int(numero_comanda):
                if anterior is None:
                    self.cabeca = atual.proximo
                else:
                    anterior.proximo = atual.proximo
                return atual.conteudo
            anterior = atual
            atual = atual.proximo
        return None
