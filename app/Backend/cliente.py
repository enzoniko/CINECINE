from pessoa import Pessoa
from dataclasses import dataclass, field
from random import randint

@dataclass
class Cliente(Pessoa):
    id: int = field(default=randint(0, 1000000))
    _compras: list = field(default_factory=list)
   
    def add_compra(self, compra):
        self._compras.append(compra)
    
    def print_info(self):
        super().print_info()
        print("ID: ", self.id)
        print("Compras: ", self._compras)
   
# c1 = Cliente(20, 12345678900)
# c1.print_info()
# c1.add_compra('Compra 1')
# c1.set_email('ooioi')
# c1.nome = "Enzo"

# c1.print_info()

