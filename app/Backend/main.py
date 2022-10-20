# Importa tudo que é necessário para o funcionamento do programa
from app.Backend.filme import Filme
from app.Backend.helpers import most_empty, lugares_disponiveis, lista_strings_para_string, verificador_input, store_objects, load_objects
from app.Backend.sessao import Sessao
from app.Backend.sala import Sala
from app.Backend.pagamento import Pagamento
import pickle
# Importa tudo que é necessário para o funcionamento do programa
# from filme import Filme
# from helpers import most_empty, lugares_disponiveis, lista_strings_para_string, verificador_input
# from sessao import Sessao
# from sala import salas
# from pagamento import Pagamento

# Cria duas salas
salas= store_objects([Sala(), Sala()], "salas.pkl")

# Lista de pagamentos (usar para mostrar o total faturado para o administrador)
pagamentos = store_objects([], "pagamentos.pkl")

# Listas de sessoes e filmes
sessoes = store_objects([Sessao('O Senhor dos Aneis', ['aventura'], 5.5, 'Muitas emoções', 'https://', False, False, ['15:00', '20:00']), Sessao('O Senhor dos Aneis', ['aventura'], 5.5, 'Muitas emoções', 'https://', False, True, ['11:00', '20:00']), Sessao('MIB', ['Romance'], 5.5, 'Muitas emoções', 'https://', False, False, ['15:00', '23:00'])], "sessoes.pkl")

salas[0].adicionar_sessao(sessoes[0])
salas[0].adicionar_sessao(sessoes[1])
salas[1].adicionar_sessao(sessoes[2])
print(list(load_objects("salas.pkl")))
salas = store_objects(salas, "salas.pkl")
print(list(load_objects("salas.pkl")))
filmes = store_objects([Filme("O Senhor dos Aneis", ["aventura"], 5.5, 'Muitas emoções', 'https://'), Filme("MIB", ["Romance"], 5.5, 'Muitas emoções', 'https://')], "filmes.pkl")

# Função que preenche as poltronas de uma sala
def preencher_poltronas(sala_mais_vazia, quantidade_ingressos, id, horario):
    # Deixar o usuário escolher as poltronas
    poltronas_a_preencher = input(
        "Digite as coordenadas das poltronas que você deseja sentar separadas por um espaço: ").split()[:quantidade_ingressos]

    # Preencher a sala com as poltronas escolhidas pelo usuário
    erradas = sala_mais_vazia.preencher_poltronas(
        poltronas_a_preencher, id, horario)

    # Se o usuário não escolher as poltronas corretamente
    while erradas != []:
        letras_erradas = list(set(erradas[0]))
        numeros_errados = list(set(erradas[1]))
        # Se o usuario escolher uma poltrona já ocupada, é printado um aviso
        if erradas[2] != []:
            print(
                f"Poltrona(s) {lista_strings_para_string(list(set(erradas[2])))} já estão ocupadas!")
        # Se o usuario escrever uma letra que não existe na matriz de poltronas, é printado um aviso
        if erradas[0] != [] and erradas[1] == []:
            print(
                f"Poltronas com letra(s) {lista_strings_para_string(letras_erradas)} não existem!")
        elif erradas[1] != [] and erradas[0] == []:
            print(
                f"Poltronas com número(s) {lista_strings_para_string([str(num) for num in numeros_errados])} não existem!")
        elif erradas[0] != []:
            print(
                f"Poltronas com letra(s) {lista_strings_para_string(letras_erradas)} não existem!")

            print(
                f"Poltronas com número(s) {lista_strings_para_string([str(num) for num in numeros_errados])} não existem!")

        # Repetir o processo de escolha de poltronas até o usuário escolher as poltronas corretamente
        poltronas_a_preencher = input(
            "Digite as coordenadas das poltronas que você deseja sentar separadas por um espaço: ").split()[:quantidade_ingressos]
        erradas = sala_mais_vazia.preencher_poltronas(
            poltronas_a_preencher, id, horario)

    # Retornar a lista de poltronas que o usuário escolheu
    return poltronas_a_preencher

# Função que mostra os filmes disponíveis


def printar_filmes():
    # Printa a lista de filmes
    print()
    print("Lista de filmes disponíveis:")
    print()
    if len(filmes) == 0:
        print("Não há filmes disponíveis!")
    for filme in range(len(filmes)):
        print(f"{filme + 1}: ", end="")
        filmes[filme].print_info()
        print()
    print('-----------------------------------------------------')
    return [(filmes.index(filme) + 1, filme) for filme in filmes]
# Função que printa as sessões de um filme


def printar_sessoes(filme):
    print()
    print(f"Sessões de {filme.upper()}: ")
    print()
    # Pra cada sessão da lista de sessões cujo nome do .get_nome() é o mesmo que o usuário deseja assistir
    for sessao in range(len([sessao for sessao in sessoes if sessao.nome == filme])):
        print(f"{sessao + 1}: ", end="")
        # Mostra a sessão
        sessao = sessoes.index(
            [sessao for sessao in sessoes if sessao.nome == filme][sessao])
        sessoes[sessao].print_info()
        print()
    print('-----------------------------------------------------')
    return [(sessoes.index(sessao), sessao) for sessao in [sessao for sessao in sessoes if sessao.nome == filme]]

# Função que mostra a sessão escolhida e opcionalmente seus horárioss


def mostrar_sessao(numero_da_sessao, mostrar_horarios=False):
    print()
    # Mostra a sessão
    # Mostra o nome
    print(sessoes[numero_da_sessao - 1].nome.upper(), end=' ')
    # Mostra se é legando ou não
    if sessoes[numero_da_sessao - 1].legenda == True:
        print("LEGENDADO", end=' ')
    else:
        print("DUBLADO", end=' ')
    # Mostra se é 3D ou não
    if sessoes[numero_da_sessao - 1].DDD == True:
        print("3D", end=' ')
    else:
        print("2D", end=' ')

    # Se for pra mostrar os horários
    if mostrar_horarios:
        print()
        # Mostra os horários da sessão
        print("Horários: ")
        print()
        for horario in range(len(sessoes[numero_da_sessao - 1].horarios)):
            print(f"{horario + 1}: ", end="")
            print(sessoes[numero_da_sessao - 1].horarios[horario])
            print()
        print('-----------------------------------------------------')

# Função que retorna a sala mais vazia dado a quantidade de lugares disponíveis na sala mais vazia e a sessão escolhida


def sala_mais_vazia(quantidade_lugares_disponiveis_sala_mais_vazia, sessao):
    # Printar as poltronas da sala mais vazia que passa a sessão escolhida para o usuário escolher as poltronas
    print("Poltronas: ")
    print(sessao)
    for sala in salas:
        for horario in sessao.horarios:
            if sessao in sala.sessoes and lugares_disponiveis(sala.cronograma[f"{sessao.id} {horario}"]) == quantidade_lugares_disponiveis_sala_mais_vazia:
                sala.printar_poltronas(sessao.id, horario)
                return sala
            

# Função que printa o comprovante de compra


def comprovante(numero_da_sessao, horario, poltronas, pagamento):
    print()
    print("Comprovante de compra: ")
    # Mostra a sessão
    mostrar_sessao(numero_da_sessao)
    # Mostra o horário
    print(horario)
    # Mostra as poltronas
    print(f"Poltronas escolhidas: {lista_strings_para_string(poltronas)}")
    # Mostra o pagamento
    pagamento.print_info()
    print("-----------------------------------------------------")


# Função que mostra as sessões de cada sala

def mostra_sessoes_de_cada_sala(printar_indice=False):
    # Pra cada sala
    for sala in range(len(salas)):
        print()
        print(f"Sala {sala + 1}:")
        print()
        # Se a sala está vazia (sem sessões) é printado um aviso
        if salas[sala].sessoes == []:
            print("Nenhuma sessão cadastrada")
            print()
        # Se a sala tem sessões
        for sessao in salas[sala].sessoes:
            for s in range(len(sessoes)):
                # Então verifica qual sessão é pelo id e printa
                if sessoes[s].id == sessao.id:
                    if printar_indice:
                        print(f"Opção {s + 1} : ")
                    # Printa a sessão com as informações
                    mostrar_sessao(s + 1, mostrar_horarios=True)

# Função que altera uma sessão


def alterar_sessao(numero_da_sessao=None):
    # Se não existir nenhuma sessão, é printado um aviso
    if len(sessoes) == 0:
        print("Não existem sessões cadastradas")
        print()
        return
    # Se o numero escolhido não existir na lista de sessao, é printado um aviso
    if numero_da_sessao is None:
        mostra_sessoes_de_cada_sala(printar_indice=True)
        numero_da_sessao = verificador_input(
            "da sessão", sessoes, 'in', "Opção inválida!")

        # Se existir mostra a sessão escolhida e seus horários
        mostrar_sessao(numero_da_sessao, mostrar_horarios=True)

    # Pergunta pelo nome do filme da sessão
    novo_nome = input(
        "Digite o nome do filme da sessão: ")
    # Pergunta pelo novo gênero da sessão
    novo_genero = input(
        "Digite o gênero da sessão: ").split()
    # Pergunta pelos novos horários da sessão
    novos_horarios = input(
        "Digite os horários da sessão: ").split()
    # Pergunta se a sessão é 3D ou não
    novo_DDD = input("É 3D? (S/N) ").upper() != 'N'
    # Pergunta se a sessão é legendada ou não

    novo_legenda = input("É legendada? (S/N) ").upper() != 'N'
    # Modifica as informações da sessão
    sessoes[numero_da_sessao - 1].modifica_info(
        novo_nome, novo_genero, novos_horarios, novo_DDD, novo_legenda)
    # Mostra a sessão escolhida e seus horários
    mostrar_sessao(numero_da_sessao, mostrar_horarios=True)

# Função que exclui uma sessão


def excluir_sessao():
    # Se o numero escolhido não existir na lista de sessao, é printado um aviso
    mostra_sessoes_de_cada_sala(printar_indice=True)
    numero_da_sessao = verificador_input(
        "da sessão (para excluir)", sessoes, 'in', "Opção inválida!")

    # Mostra a sessão escolhida e seus horários
    mostrar_sessao(numero_da_sessao, mostrar_horarios=True)
    if input("Deseja excluir a sessão? (S/N) ").upper() != 'S':
        return
    for sala in salas:
        sala.remover_sessao(sessoes[numero_da_sessao - 1])

    filmes.pop(filmes.index([filme for filme in filmes if filme.nome == sessoes[numero_da_sessao - 1].nome][0]))
    sessoes.pop(numero_da_sessao - 1)

# Função que adiciona uma nova sessão


def adicionar_sessao():
    sessoes.append(Sessao())
    alterar_sessao(len(sessoes))
    # Se o numero da sala para colocar a nova sessão não existir na lista de salas, é printado um aviso
    numero_da_sala = verificador_input(
        "da sala (pra por a sessão)", salas, 'in', "Opção inválida!")
    # Se existir, a sessão é adicionada na sala e é criado um filme com as informações da sessão
    salas[numero_da_sala - 1].adicionar_sessao(sessoes[-1])
    filmes.append(Filme(sessoes[-1].nome, sessoes[-1].generos))

# Função do pagamento


def pagamento(quantidade_ingressos, quantidade_meias, numero_da_sessao, horario, poltronas_escolhidas, sala):
    # Inicia o pagamento
    pagamento = Pagamento(quantidade_ingressos, quantidade_meias)
    # Mostrar o preço total
    print(f"Preço total: R$ {pagamento.valor}")
    # Pergunta se o usuário deseja pagar com crédito, dinheiro ou débito
    print("Forma de pagamento:\n1 - Crédito\n2 - Débito\n3 - Dinheiro")
    # Formas de pagamento
    formas = ["Crédito", "Débito", "Dinheiro"]
    # Pega a forma que o usuário deseja pagar
    forma = verificador_input(
        "da forma de pagamento", formas, "in", "Opção inválida")
    # Modificia a forma de pagamento do pagamento
    pagamento.set_forma(formas[forma - 1])

    while True:
        # Pergunta pro usuário se ele deseja confirmar a compra
        confirmar = input("Confirmar compra? (S/N) ").upper()

        # Se ele confirmar, mostra o pagamento
        if confirmar == "S":
            # Pagamento realizado com sucesso!
            print("Pagamento realizado com sucesso!")

            # Comprovante do pagamento
            comprovante(numero_da_sessao, horario,
                        poltronas_escolhidas, pagamento)

            # Adiciona o pagamento na lista de pagamentos
            pagamentos.append(pagamento)
            break

        # Se ele não confirmar, pergunta se ele quer cancelar a compra
        cancelar = input(
            "Deseja cancelar a compra? (S/N) ").upper()

        # Se ele quer cancelar
        if cancelar == "S":
            # Cancela o pagamento
            print("Compra cancelada!")
            # Esvazia as poltronas escolhidas pelo usuário
            sala.esvaziar_poltronas(
                poltronas_escolhidas, sessoes[numero_da_sessao - 1].id, horario)
            # Printa a sala depois de esvaziar as poltronas
            sala.printar_poltronas(
                sessoes[numero_da_sessao - 1].id, horario)
            print("-----------------------------------------------------")
            break


# Função que mostra o cronograma de uma sala
def mostrar_cronograma_de_uma_sala():
    numero_da_sala = verificador_input(
        "da sala (pra ver o cronograma)", salas, 'in', "Opção inválida!")
    if len(salas[numero_da_sala - 1].sessoes) == 0:
        print("Não há sessões nessa sala!")
    salas[numero_da_sala - 1].print_info()

# Função que calcula e printa a fatura atual


def total_faturado():
    # Se não existir nenhuma compra confirmada, é printado um aviso
    if pagamentos == []:
        print("Não existem pagamentos cadastrados")
    else:
        # É somado cada um dos pagamentos
        total = sum(pagamento.valor for pagamento in pagamentos)
        # Printa do valor total faturado
        print(f"Total faturado: R$ {total:.2f}")
        print(
            # Printa a quantidade de ingressos totais vendidos
            f"Quantidade total de ingressos vendidos: {sum(pagamento.ingressos for pagamento in pagamentos)}")
        print(
            # Printa apenas a quantidade dos ingressos vendidos com o valor original
            f"Quantidade de ingressos inteiros vendidos: {sum(pagamento.ingressos - pagamento.meias for pagamento in pagamentos)}")
        print(
            # Printa apenas a quantidade dos ingressos vendidos pela metade do preço
            f"QUantidade de meia-entradas vendidas: {sum(pagamento.meias for pagamento in pagamentos)}")

    print()

# Função do Administrador


def admin():
    # Menu com as operações que o administrador pode operar
    print()
    print("Menu: ")
    print("1: Consultar sessões")
    print("2: Alterar sessão")
    print("3: Adicionar sessão")
    print("4: Excluir sessão")
    print("5: Consultar fatura atual")
    print("6: Mostrar cronograma de uma sala")
    print("7: Sair")

    # Verifica se a opção escolhid existe, se não, então é printado um aviso
    op = verificador_input("da opção", list(
        range(7)), 'in', "Opção inválida!")

    # Consultar sessões
    if op == 1:
        # Função que printa as sessões
        mostra_sessoes_de_cada_sala()
    # Alterar sessão
    elif op == 2:
        # Função que Altera um sessão
        alterar_sessao()
    # Adicionar sessão
    elif op == 3:
        # Função que adiciona uma nova sessão
        adicionar_sessao()
    # Excluir sessão
    elif op == 4:
        # Função que exclui uma sessão
        excluir_sessao()
    # Consultar fatura atual
    elif op == 5:
        # Função que calcula e printa a fatura atual
        total_faturado()
    elif op == 6:
        mostrar_cronograma_de_uma_sala()
    # Sair
    elif op == 7:
        return ['', input("Voce é administrador? (S/N) ").upper()]
    return ['admin', 'S']

# Função do Usuario


def usuario():

    # Printa a lista de filmes
    printar_filmes()
    if len(filmes) == 0:
        return 2
    # Pergunta qual o número do filme que o usuário deseja
    numero_do_filme = verificador_input(
        "do filme", filmes, "in", "Opção inválida")

    # Pega o nome do filme relacionado com o número digitado pelo usuário
    nome_do_filme = filmes[numero_do_filme - 1].nome

    # Printa a lista de sessões do filme
    printar_sessoes(nome_do_filme)

    # Pergunta qual a sessão que o usuário deseja assistir
    numero_da_sessao = verificador_input(
        "da sessão", [sessao for sessao in sessoes if sessao.nome == nome_do_filme], "in", "Opção inválida")
    numero_da_sessao = sessoes.index(
        [sessao for sessao in sessoes if sessao.nome == nome_do_filme][numero_da_sessao - 1]) + 1
    # Mostra a sessão escolhida e seus horários
    mostrar_sessao(numero_da_sessao, mostrar_horarios=True)

    # Pergunta qual o horário que o usuário deseja assistir
    numero_do_horario = verificador_input(
        "do horário", sessoes[numero_da_sessao - 1].horarios, "in", "Opção inválida")

    # Pega o horário relacionado com o número digitado pelo usuário
    horario = sessoes[numero_da_sessao -
                      1].horarios[numero_do_horario - 1]

    # Mostra a sessão escolhida
    mostrar_sessao(numero_da_sessao)

    # Mostra o horário escolhido
    print(horario)
    print()

    # Quantidade de lugares disponíveis na sala mais vazia que passa a sessão escolhida
    quantidade_lugares_disponiveis_sala_mais_vazia = most_empty(
        [
            [
                sala.cronograma[
                    f"{sessoes[numero_da_sessao - 1].id} {horario}"
                ]
                for sessao in sala.sessoes
                if sessao.id == sessoes[numero_da_sessao - 1].id
            ]
            for sala in salas
        ]
    )

    # Pergunta quantos ingressos o usuário deseja comprar
    quantidade_ingressos = verificador_input("de ingressos", [
        quantidade_lugares_disponiveis_sala_mais_vazia], "<=", "Não temos nenhuma sala com essa quantidade de poltronas!")

    # Pergunta quantos desses ingressos são meia entrada
    quantidade_meias = verificador_input("de meias entradas", [
        quantidade_ingressos], "<=", "Quantidade de meias não pode ser maior que a quantidade de ingressos")

    # Printar as poltronas da sala mais vazia que passa a sessão escolhida para o usuário escolher as poltronas
    sala = sala_mais_vazia(
        quantidade_lugares_disponiveis_sala_mais_vazia, sessoes[numero_da_sessao - 1])

    # Preenche as poltronas da sala mais vazia com as poltronas escolhidas pelo usuário
    poltronas_escolhidas = preencher_poltronas(
        sala, quantidade_ingressos, sessoes[numero_da_sessao - 1].id, horario)

    # Printa a sala depois de preencher as poltronas
    sala.printar_poltronas(sessoes[numero_da_sessao - 1].id, horario)
    print("-----------------------------------------------------")

    # Chama a função pagamento
    pagamento(quantidade_ingressos, quantidade_meias,
              numero_da_sessao, horario, poltronas_escolhidas, sala)

    print("1: Comprar novos ingressos\n2: Sair ")

    return verificador_input("da opção (Comprar ou Sair)", [0, 0], 'in', 'Opção inválida')

# Função main


def main():
    # Loop pra saber se o usuario é adm ou não

    # Pergunta pro usuário se ele é um administrador
    is_adm = input("Voce é administrador? (S/N) ").upper()
    senha = ""
    while True:

        # Se ele for pede confirmação por senha, e mostra o menu para administrador
        if is_adm == "S":

            # Pergunta por senha
            if senha != "admin":
                senha = input("Digite a senha: (0 para sair) ")
            # Se a senha for correta, mostra o menu para o administrador
            while senha not in ["admin", "0"]:
                print("Senha incorreta!")
                senha = input("Digite a senha: (0 para sair) ")
            if senha == "admin":
                senha, is_adm = admin()

            if senha == "0":
                is_adm = input("Voce é administrador? (S/N) ").upper()
        # Se for um usuario
        elif is_adm == "N":
            while True:
                # Entra na função do usuario
                encerrar = usuario()
                if encerrar == 1:
                    continue
                elif encerrar == 2:
                    is_adm = input("Você é administrador? (S/N) ").upper()
                    break
        else:
            is_adm = input("Você é administrador? (S/N) ").upper()


# Chama a função main no início do programa
if __name__ == '__main__':
    main()

