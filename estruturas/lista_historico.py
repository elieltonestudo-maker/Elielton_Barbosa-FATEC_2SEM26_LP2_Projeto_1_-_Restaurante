# estruturas/lista_historico.py

from estruturas.no import No

class ListaHistorico:
    def __init__(self):
        self.cabeca = None  # busca histórico de pagamentos

    def adicionar_registro(self, registro_pagamento):
        # envia registro de pagamento no início da lista
        novo_no = No(registro_pagamento)
        novo_no.proximo = self.cabeca
        self.cabeca = novo_no

    def obter_todos(self):
        # faz uma busca do que foi pago
        atual = self.cabeca
        while atual is not None:
            yield atual.conteudo
            atual = atual.proximo
