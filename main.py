# main.py

import os
import pickle
from datetime import datetime, timedelta
from faker import Faker

from servicos.gestor_estoque import GestorEstoque
from servicos.interface import InterfaceUsuario
from servicos.caixa import Caixa

fake = Faker('pt_BR')
ARQUIVO_DADOS = "dados.pkl"

def salvar_sistema(gestor_estoque, caixa):
    # salva as estruturas no arquivo local
    try:
        with open(ARQUIVO_DADOS, "wb") as f:
            pickle.dump((gestor_estoque, caixa), f)
    except Exception as e:
        print(f"\n[Erro]: Falha ao salvar os dados: {e}")

def carregar_sistema():
    # busca o arquivo salvo ou inicia o sistema limpo
    if os.path.exists(ARQUIVO_DADOS):
        try:
            with open(ARQUIVO_DADOS, "rb") as f:
                return pickle.load(f)
        except Exception:
            print("\n[Aviso]: Arquivo de dados corrompido. Criando novo sistema.")
    
    gestor = GestorEstoque()
    caixa = Caixa(gestor)
    return gestor, caixa

def popular_dados_falsos(gestor_estoque, caixa):
    # carrega os produtos e as comandas de teste usando o faker
    print("\n[Aviso]: Populando o sistema com dados automáticos de teste...")
    
    produtos_padrao = [
        {"nome": "hamburguer", "pc": 10.0, "pv": 25.0},
        {"nome": "lanche natural", "pc": 8.0, "pv": 22.0},
        {"nome": "hot dog", "pc": 9.0, "pv": 23.5},
        {"nome": "refrigerante", "pc": 2.5, "pv": 6.0},
        {"nome": "batata frita", "pc": 4.0, "pv": 15.0},
        {"nome": "suco natural", "pc": 3.5, "pv": 8.0},
        {"nome": "agua mineral", "pc": 1.5, "pv": 4.5},
        {"nome": "cerveja", "pc": 4.0, "pv": 9.0},
        {"nome": "pizza", "pc": 15.0, "pv": 40.0},
        {"nome": "pudim", "pc": 3.0, "pv": 12.0},
        {"nome": "porção calabresa", "pc": 12.0, "pv": 32.0}
    ]
    
    hoje = datetime.now()
    for prod in produtos_padrao:
        # cria dois lotes por produto para testar o critério da fila
        data_c1 = (hoje - timedelta(days=3)).strftime("%d/%m/%Y")
        data_v1 = (hoje + timedelta(days=15)).strftime("%d/%m/%Y")
        gestor_estoque.abastecer_produto(prod["nome"], prod["pc"], prod["pv"], data_c1, data_v1, 10)
        
        data_c2 = hoje.strftime("%d/%m/%Y")
        data_v2 = (hoje + timedelta(days=20)).strftime("%d/%m/%Y")
        gestor_estoque.abastecer_produto(prod["nome"], prod["pc"], prod["pv"], data_c2, data_v2, 15)
            
    for num_comanda in range(1, 4):
        nome_cliente = fake.first_name()
        caixa.abrir_comanda(num_comanda, nome_cliente)
        caixa.lancar_item_comanda(num_comanda, "hamburguer", 1)

    print("[Sucesso]: Estoque abastecido por lotes e comandas iniciais abertas!")


def main():
    gestor_estoque, caixa = carregar_sistema()
    
    if gestor_estoque.produtos_estoque is None:
        popular_dados_falsos(gestor_estoque, caixa)

    while True:
        InterfaceUsuario.exibir_menu()
        opcao = input("Escolha uma opção: ").strip()

        if opcao == "1":
            try:
                num = int(input("Número da Comanda: "))
                nome = input("Nome do Cliente: ").strip()
                if nome == "":
                    print("\n[Erro]: O nome do cliente não pode ser vazio.")
                    continue
                if caixa.abrir_comanda(num, nome):
                    print(f"\n[Sucesso]: Comanda # {num} aberta para {nome}.")
                else:
                    print("\n[Erro]: Esta comanda já está ativa no salão.")
            except ValueError:
                print("\n[Erro]: Digite um número válido para a comanda.")

        elif opcao == "2":
            try:
                num = int(input("Número da Comanda: "))
                comanda = caixa.comandas_ativas.buscar_por_numero(num)
                
                if comanda is None:
                    print(f"\n[Bloqueado]: A comanda # {num} nao esta aberta ou nao existe no salao!")
                    continue
                
                print(f" -> Comanda ativa localizada! Cliente dono: {comanda.nome_cliente.upper()}")
                print("-" * 40)
                
                InterfaceUsuario.exibir_painel_cardapio()
                
                produto = input("Nome do Produto do Cardápio: ").strip().lower()
                
                # calcula o saldo livre subtraindo o que ja foi pedido no salao
                estoque_bruto = gestor_estoque.obter_quantidade_total(produto)
                reservado = caixa.obter_consumo_pendente_salao(produto)
                total_disponivel = estoque_bruto - reservado
                
                qtd = int(input(f"Disponíveis: {total_disponivel}, Digite a Quantidade: "))
                
                if qtd <= 0:
                    print("\n[Erro]: A quantidade deve ser maior que zero.")
                    continue
                
                if caixa.lancar_item_comanda(num, produto, qtd):
                    print(f"\n[Sucesso]: {qtd}x '{produto}' adicionado(s) à comanda # {num} ( {comanda.nome_cliente} ).")
                else:
                    print("\n[Erro]: Nao foi possivel lancar. Verifique se o produto possui saldo suficiente.")
            except ValueError:
                print("\n[Erro]: Entrada numérica inválida.")

        elif opcao == "3":
            try:
                num = int(input("Número da Comanda: "))
                comanda = caixa.comandas_ativas.buscar_por_numero(num)
                if comanda:
                    print(f"\n--- Comanda # {comanda.numero} - Cliente: {comanda.nome_cliente} ---")
                    print(f"Abertura: {comanda.data_hora_abertura}")
                    print("-" * 40)
                    atual = comanda.primeiro_item
                    while atual:
                        print(f"{atual.quantidade}x {atual.nome_produto} | R$ {atual.preco_unitario:.2f} un")
                        atual = atual.proximo
                    print("-" * 40)
                    print(f"Total Atual: R$ {comanda.calcular_total():.2f}")
                else:
                    print("\n[Erro]: Comanda não encontrada.")
            except ValueError:
                print("\n[Erro]: Digite um número válido.")

        elif opcao == "4":
            try:
                num = int(input("Número da Comanda para Fechamento: "))
                comanda = caixa.comandas_ativas.buscar_por_numero(num)
                if comanda is None:
                    print("\n[Erro]: Comanda não encontrada.")
                    continue
                    
                print(f"\n -> Fechamento localizado! Cliente: {comanda.nome_cliente.upper()}")
                print("-" * 40)
                
                total = comanda.calcular_total()
                print(f"Valor Total da Conta: R$ {total:.2f}")
                print("Formas de Pagamento: PIX, Cartao, Dinheiro, Confianca")
                forma = input("Digite a forma de pagamento: ").strip()
                
                pagador = input("Nome de quem está pagando (Deixe vazio para o nome do cliente): ").strip()
                if pagador == "":
                    pagador = comanda.nome_cliente
                
                valor_pago = caixa.fechar_e_pagar(num, forma, pagador)
                if valor_pago is not None:
                    print(f"\n[Sucesso]: Comanda # {num} encerrada! Lotes de estoque atualizados por FIFO.")
                else:
                    print("\n[Erro]: Falha ao processar o fechamento.")
            except ValueError:
                print("\n[Erro]: Digite um número válido.")

        elif opcao == "5":
            try:
                nome = input("Nome do Produto: ").strip().lower()
                pc = float(input("Preço de Compra (R$): "))
                pv = float(input("Preço de Venda (R$): "))
                qtd = int(input("Quantidade do Lote: "))
                data_c = datetime.now().strftime("%d/%m/%Y")
                validade = input("Data de Vencimento (DD/MM/AAAA): ").strip()
                
                gestor_estoque.abastecer_produto(nome, pc, pv, data_c, validade, qtd)
                print(f"\n[Sucesso]: Novo lote de '{nome}' adicionado ao estoque.")
            except ValueError:
                print("\n[Erro]: Valores numéricos digitados incorretamente.")

        elif opcao == "6":
            InterfaceUsuario.exibir_painel_cardapio()
            nome = input("Nome do Produto para consulta: ").strip().lower()
            
            estoque_fisico = gestor_estoque.obter_quantidade_total(nome)
            em_consumo = caixa.obter_consumo_pendente_salao(nome)
            saldo_livre = estoque_fisico - em_consumo
            
            print(f"\n=======================================")
            print(f"       INSPEÇÃO DE ESTOQUE: {nome.upper()}   ")
            print(f"=======================================")
            print(f" • Total Físico (Lotes):     {estoque_fisico} un")
            print(f" • Reservado nas Mesas:     {em_consumo} un")
            print(f" -------------------------------------")
            print(f" -> Saldo Disponível Livre:  {saldo_livre} un")
            print(f"=======================================")

        elif opcao == "7":
            caixa.gerar_relatorio_vendas()

        elif opcao == "8":
            caixa.gerar_relatorio_consumo()

        elif opcao == "9":
            popular_dados_falsos(gestor_estoque, caixa)

        elif opcao == "10":
            gestor_estoque.exibir_cardapio()

        elif opcao == "11":
            try:
                num = int(input("Número da Comanda: "))
                comanda = caixa.comandas_ativas.buscar_por_numero(num)
                
                if comanda is None:
                    print(f"\n[Bloqueado]: A comanda #{num} não existe no salão.")
                    continue
                    
                print(f"\n -> Editando consumo de: {comanda.nome_cliente.upper()}")
                print("-" * 40)
                
                print("           CONSUMO ATUAL DA MESA       ")
                print("-" * 40)
                atual_item = comanda.primeiro_item
                contagem_itens = 0
                while atual_item:
                    print(f" * {atual_item.quantidade}x {atual_item.nome_produto} | R$ {atual_item.preco_unitario:.2f} un")
                    atual_item = atual_item.proximo
                    contagem_itens += 1
                if contagem_itens == 0:
                    print(" Nenhum item lançado nesta comanda até o momento.")
                print("-" * 40)
                
                produto = input("Nome do Produto que deseja alterar: ").strip().lower()
                
                item_encontrado = False
                atual = comanda.primeiro_item
                while atual:
                    if atual.nome_produto == produto:
                        item_encontrado = True
                        break
                    atual = atual.proximo
                    
                if not item_encontrado:
                    print(f"\n[Erro]: O produto '{produto}' não foi lançado nesta comanda.")
                    continue
                
                estoque_bruto = gestor_estoque.obter_quantidade_total(produto)
                reservado = caixa.obter_consumo_pendente_salao(produto)
                total_disponivel = estoque_bruto - reservado
                
                nova_qtd = int(input(f"Disponíveis no Estoque: {total_disponivel}. Digite a NOVA Quantidade Total desejada: "))
                
                if nova_qtd <= 0:
                    print("\n[Erro]: A quantidade deve ser maior que zero.")
                    continue
                
                # guarda o valor antigo para seguranca caso o novo lançamento falhe
                qtd_antiga = atual.quantidade
                comanda.remover_item(produto)
                
                if caixa.lancar_item_comanda(num, produto, nova_qtd):
                    print(f"\n[Sucesso]: Quantidade de '{produto}' atualizada para {nova_qtd}x com sucesso!")
                else:
                    caixa.lancar_item_comanda(num, produto, qtd_antiga)
                    print("\n[Erro]: Falha ao atualizar. O saldo livre do estoque não suporta a nova quantidade.")
            except ValueError:
                print("\n[Erro]: Entrada numérica inválida.")

        elif opcao == "0":
            print("\n[Aviso]: Salvando dados do restaurante...")
            salvar_sistema(gestor_estoque, caixa)
            print("Sistema fechado com segurança através do Pickle. Até logo!")
            break
        else:
            print("\n[Erro]: Opção inválida. Tente novamente.")

if __name__ == "__main__":
    main()
