from dataclasses import dataclass

@dataclass(repr=False)
class Pessoa:
    idade: int = 0
    cpf: int = 000000000000
    email: str = 'Email não informado'
    nome: str = 'Nome não informado'
    
    def print_info(self) -> None:
        print("Nome: ", self.nome)
        print("Idade: ", self.idade)
        print("CPF: ", self.cpf)
        print("Email: ", self.email)

