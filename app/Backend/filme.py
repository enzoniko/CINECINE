# Importa a função lista_strings_para_string do módulo helpers
from app.Backend.helpers import lista_strings_para_string

# Importa a função lista_strings_para_string do módulo helpers
# from helpers import lista_strings_para_string

# Cria a super classe Filme


class Filme:

    # Construtor da classe Filme, recebe os atributos do filme (nome, generos)
    def __init__(self, nome, generos):
        self.nome = nome
        self.generos = generos

    # getters e setters:

    # get_nome retorna o nome do filme
    def get_nome(self):
        return self.nome

    # get_generos retorna os generos do filme
    def get_generos(self):
        return self.generos

    # set_nome modifica o nome do filme
    def set_nome(self, nome):
        self.nome = nome

    # set_generos modifica os generos do filme
    def set_generos(self, generos):
        self.generos = generos

    # print_info imprime os informações do filme
    def print_info(self):
        print(self.nome, end=" (")
        print(lista_strings_para_string(self.generos), end=")\n")