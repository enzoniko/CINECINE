from typing import List
from pessoa import Pessoa
from dataclasses import dataclass, field

@dataclass
class Admin(Pessoa):

    salas: List = field(default_factory = list)

    def modificar_sala(self, sala):
        self.salas.append(sala)
    
    def print_info(self):
        super().print_info()
        print("Salas: ", self.salas)
    
