# estruturas/lista_historico.py

from estruturas.no import No

class ListaHistorico:
    def __init__(self):
        self.cabeca = None  # Início do histórico de pagamentos

    def adicionar_registro(self, registro_pagamento):
        """Insere um novo registro de pagamento no início da lista de histórico."""
        novo_no = No(registro_pagamento)
        novo_no.proximo = self.cabeca
        self.cabeca = novo_no

    def obter_todos(self):
        """Retorna um gerador para percorrer os registros sequencialmente na hora do relatório."""
        atual = self.cabeca
        while atual is not None:
            yield atual.conteudo
            atual = atual.proximo
