# Importa a super classe Filme do módulo Filme
from dataclasses import dataclass, field
from random import randint
from app.Backend.filme import Filme

# Importa a função lista_strings_para_string do módulo helpers
from app.Backend.helpers import lista_strings_para_string

# Importa a super classe Filme do módulo Filme
# from filme import Filme

# # Importa a função lista_strings_para_string do módulo helpers
# from helpers import lista_strings_para_string

# Cria a sub classe Sessao que herda de Filme
@dataclass
class Sessao(Filme):
    legenda: bool = False
    DDD: bool = False
    horarios: list[str] = field(default_factory=list)
    id: int = 0

    def __post_init__(self):
        self.id = randint(0, 1000000)
    # print_info imprime os informações da sessão
    def print_info(self):
        # super().print_info()
        # Imprime se a sessão é legendada ou dublada
        if self.legenda == True:
            print("LEGENDADO", end=' ')
        else:
            print("DUBLADO", end=' ')

        # Imprime se a sessão é 3D ou 2D
        if self.DDD == True:
            print("3D")
        else:
            print("2D")

        # Printa os horários
        print(f"Horários: {lista_strings_para_string(self.horarios)}")

    # modifica_info modifica as informações da sessão
    def modifica_info(self, nome, generos, horarios, DDD, legenda):
        self.nome = nome
        self.generos = generos
        self.horarios = horarios
        self.DDD = DDD
        self.legenda = legenda

