# Importa a super classe Filme do módulo Filme
from app.Backend.filme import Filme

# Importa a função lista_strings_para_string do módulo helpers
from app.Backend.helpers import lista_strings_para_string

# Importa a super classe Filme do módulo Filme
# from filme import Filme

# # Importa a função lista_strings_para_string do módulo helpers
# from helpers import lista_strings_para_string

# Cria a sub classe Sessao que herda de Filme


class Sessao(Filme):

    # Construtor da sub classe Sessao, recebe os atributos da super classe Filme e os atributos específicos da sub classe Sessao (legenda = False, horários, DDD = False)
    def __init__(self, nome='', generos='', horarios='', DDD=False, legenda=False):
        super().__init__(nome, generos)
        self.legenda = legenda
        self.horarios = horarios
        self.DDD = DDD
        self.id = id(self)

    # getters e setters:

    # get_legenda retorna se a sessão é legendada
    def get_legenda(self):
        return self.legenda

    # get_horarios retorna os horários da sessão
    def get_horarios(self):
        return self.horarios

    # get_DDD retorna se a sessão é 3D
    def get_DDD(self):
        return self.DDD

    # get_id retorna o id da sessão
    def get_id(self):
        return str(self.id)

    # set_legenda modifica se a sessão é legendada
    def set_legenda(self, legenda):
        self.legenda = legenda

    # set_horarios modifica os horários da sessão
    def set_horarios(self, horarios):
        self.horarios = horarios

    # set_DDD modifica se a sessão é 3D
    def set_DDD(self, DDD):
        self.DDD = DDD

    # print_info imprime os informações da sessão
    def print_info(self):
        # super().print_info()
        # Imprime se a sessão é legendada ou dublada
        if self.get_legenda() == True:
            print("LEGENDADO", end=' ')
        else:
            print("DUBLADO", end=' ')

        # Imprime se a sessão é 3D ou 2D
        if self.get_DDD() == True:
            print("3D")
        else:
            print("2D")

        # Printa os horários
        print(f"Horários: {lista_strings_para_string(self.horarios)}")

    # modifica_info modifica as informações da sessão
    def modifica_info(self, nome, generos, horarios, DDD, legenda):
        self.set_nome(nome)
        self.set_generos(generos)
        self.set_horarios(horarios)
        self.set_DDD(DDD)
        self.set_legenda(legenda)
