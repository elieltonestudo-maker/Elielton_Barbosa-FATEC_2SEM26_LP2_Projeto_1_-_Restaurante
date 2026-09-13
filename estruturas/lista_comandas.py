# estruturas/lista_comandas.py

from estruturas.no import No

class ListaComandas:
    def __init__(self):
        self.cabeca = None  # Início da lista de comandas ativas

    def adicionar_comanda(self, comanda):
        """Insere uma nova comanda no início da lista."""
        novo_no = No(comanda)
        novo_no.proximo = self.cabeca
        self.cabeca = novo_no

    def buscar_por_numero(self, numero_comanda):
        """Busca uma comanda específica pelo número informado."""
        atual = self.cabeca
        while atual is not None:
            if atual.conteudo.numero == int(numero_comanda):
                return atual.conteudo
            atual = atual.proximo
        return None

    def remover_comanda(self, numero_comanda):
        """Remove a comanda da lista após o fechamento do caixa."""
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
