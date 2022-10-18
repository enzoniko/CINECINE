# Função lista_strings_para_string: recebe uma lista de strings e retorna uma string com todas as strings separadas por vírgula
from functools import partial


def lista_strings_para_string(lista):
    return ", ".join(lista)

# Função printa_matriz: recebe uma matriz e imprime a matriz


def printa_matriz(matriz):
    for linha in matriz:
        print(linha)

# Função check_1: recebe um número e retorna um x se o número for 1 e um espaço se o número for 0


def check_1(n):
    return "X" if n == 1 else " "

# Função lugares_disponiveis: recebe uma matriz e retorna o número de lugares disponíveis na matriz


def lugares_disponiveis(matriz):
    return sum(linha.count(0) for linha in matriz)

# Função most_empty: recebe uma lista de salas e retorna a sala com mais lugares disponíveis

# Função que verifica qual sala está mais vazia


def most_empty(matrizes):
    quantidade_de_lugares_disponiveis_da_matriz_mais_vazia = 0
    for i in matrizes:
        for matriz in i:
            if matriz != [] and (quantidade_de_lugares_disponiveis_da_matriz_mais_vazia == 0 or quantidade_de_lugares_disponiveis_da_matriz_mais_vazia != 0 and lugares_disponiveis(matriz) > quantidade_de_lugares_disponiveis_da_matriz_mais_vazia):
                quantidade_de_lugares_disponiveis_da_matriz_mais_vazia = lugares_disponiveis(
                    matriz)
    return quantidade_de_lugares_disponiveis_da_matriz_mais_vazia


# Função que verifica se a informação foi escrita corretamente
def verificador_input(coisa, lista, condicao, mensagem_erro):
    while True:
        # Pede um numero para o usuario
        numero = int(
            input(f"Digite o número {coisa} que você deseja: "))
        # Se o numero dado pelo usuario existir dentro da lista de coisas que ele está buscando, ele vai retornar a opção escolhida
        if (condicao == 'in' and numero - 1 in range(len(lista))) or (condicao == '<=' and numero <= lista[0] and numero > 0):
            return numero
        # Se o numero não existir, é printado um aviso
        else:
            print(mensagem_erro)

def automatic_getters_and_setters(original_class):
    privateatributeslist = [name for name, _ in original_class.__dict__.items() if name.startswith("_") and not name.startswith("__")]

    for name in privateatributeslist:
        setattr(original_class, f'get{name}', classmethod(partial(lambda cls, name: getattr(cls, name), name=name)))
        setattr(original_class, f'set{name}', classmethod(partial(lambda cls, value, name: setattr(cls, name, value), name=name)))

    return original_class