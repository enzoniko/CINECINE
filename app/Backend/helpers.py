# Importar Pickle para salvar e carregar objetos
import pickle
from typing import List

# Função lista_strings_para_string: recebe uma lista de strings e retorna uma string com todas as strings separadas por vírgula
def lista_strings_para_string(lista) -> str:
    return ", ".join(lista)

# Função lugares_disponiveis: recebe uma matriz e retorna o número de lugares disponíveis na matriz
def lugares_disponiveis(matriz) -> int:
    return sum(linha.count(0) for linha in matriz)

# Função most_empty: recebe uma lista de salas e retorna a quantidade de lugares na sala com mais lugares disponíveis
def most_empty(matrizes) -> int:
    quantidade_de_lugares_disponiveis_da_matriz_mais_vazia = 0
    for i in matrizes:
        for matriz in i:
            if matriz != [] and (quantidade_de_lugares_disponiveis_da_matriz_mais_vazia == 0 or quantidade_de_lugares_disponiveis_da_matriz_mais_vazia != 0 and lugares_disponiveis(matriz) > quantidade_de_lugares_disponiveis_da_matriz_mais_vazia):
                quantidade_de_lugares_disponiveis_da_matriz_mais_vazia = lugares_disponiveis(
                    matriz)
    return quantidade_de_lugares_disponiveis_da_matriz_mais_vazia

# Helper functions for the database:

def save_object(obj: callable, filename: str):
    with open(filename, 'wb') as output:
        pickle.dump(obj, output, pickle.HIGHEST_PROTOCOL)

def load_object(filename: str) -> callable:
    with open(filename, 'rb') as input:
        return pickle.load(input)

def save_objects(objs: list, filename: str):
    with open(filename, 'wb') as output:
        for obj in objs:
            pickle.dump(obj, output, pickle.HIGHEST_PROTOCOL)

def load_objects(filename: str):
    with open(filename, 'rb') as input:
        while True:
            try:
                yield pickle.load(input)
            except EOFError:
                break

def store_objects(objs: list, filename: str) -> List[callable]:
    save_objects(objs, filename)
    return list(load_objects(filename))

def update_objects(new_objs: list, filename: str) -> List[callable]:
    old_objects = list(load_objects(filename))
    old_objects.extend(new_objs)
    save_objects(old_objects, filename)
    return list(load_objects(filename))
