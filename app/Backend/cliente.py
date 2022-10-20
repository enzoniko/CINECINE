from typing import List
from pessoa import Pessoa
from dataclasses import dataclass, field
from random import randint

@dataclass
class Cliente(Pessoa):
    id: int = field(default=randint(0, 1000000))
    _compras: List = field(default_factory=list, init=False)
   
    def add_compra(self, compra):
        self._compras.append(compra)
    
    def print_info(self):
        super().print_info()
        print("ID: ", self.id)
        print("Compras: ", self._compras)
   
