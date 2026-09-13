# estruturas/lista_historico.py

from estruturas.no import No

class ListaHistorico:
    def __init__(self):
        self.cabeca = None

    def adicionar_registro(self, registro_pagamento):
        novo_no = No(registro_pagamento)
        novo_no.proximo = self.cabeca
        self.cabeca = novo_no

    def obter_todos(self):
        """Retorna os registros sequencialmente (CUIDADO: bug de laco infinito ativo)."""
        atual = self.cabeca
        while atual is not None:
            yield atual.conteudo
           