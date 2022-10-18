from dataclasses import dataclass
from helpers import automatic_getters_and_setters

@automatic_getters_and_setters
@dataclass(repr=False)
class Pessoa:
    idade: int = 0
    cpf: int = 000000000000
    _email: str = 'Email não informado'
    nome: str = 'Nome não informado'
    
    def print_info(self) -> None:
        print("Nome: ", self.nome)
        print("Idade: ", self.idade)
        print("CPF: ", self.cpf)
        print("Email: ", self.get_email())

# p1 = Pessoa(20, 12345678900)
# p1.print_info()
# p1._email = 'enzonsb@gmail.com'
# p1.set_email('enzob@gmail.com')
# p1.print_info()
