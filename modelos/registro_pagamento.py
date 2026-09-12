# modelos/registro_pagamento.py

from datetime import datetime

class RegistroPayment:
    def __init__(self, nome_pagador, numero_comanda, forma_pagamento, valor_total):
        self.nome_pagador = nome_pagador
        self.numero_comanda = int(numero_comanda)
        self.forma_pagamento = forma_pagamento  # Exemplos: PIX, Cartão, Dinheiro ou Confiança
        self.valor_total = float(valor_total)
        self.data_hora = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
