# Importa a função lista_strings_para_string do módulo helpers

from dataclasses import dataclass, field
from typing import List
from app.Backend.helpers import lista_strings_para_string


# Importa a função lista_strings_para_string do módulo helpers
# from helpers import lista_strings_para_string

# Cria a super classe Filme

@dataclass
class Filme:
    nome: str = ""
    generos: List[str] = field(default_factory=list)
    classification: float = 0.0
    description: str = ""
    imagem: str = ""

    # print_info imprime os informações do filme
    def print_info(self):
        print(self.nome, end=" (")
        print(lista_strings_para_string(self.generos), end=")\n")

