# estruturas/no.py

class No:
    def __init__(self, conteudo):
        self.conteudo = conteudo  # usado p/ armazenar o ojeto ao no
        self.proximo = None       # aponta para o próximo nó
