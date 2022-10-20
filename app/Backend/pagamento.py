# Classe Pagamento
from dataclasses import dataclass
from random import randint

@dataclass
class Pagamento():
    ingressos: int = 0
    meias: int = 0
    valor: float = 0
    forma: str = "Dinheiro"
    id: int = 0

    def __post_init__(self):
        self.id = randint(0, 1000000)
        self.set_valor(self.ingressos, self.meias)
   
    # set_valor modifica o valor, calculando com base nos ingressos e nas meias
    def set_valor(self, ingressos, meias):
        self.valor = 30 * (ingressos - meias) + 15 * meias

    # print_info imprime os informações da compra
    def print_info(self):
        print(f"Inteiras: {self.ingressos - self.meias}")
        print(f"Meias: {self.meias}")
        print(f"Valor: R${self.valor},00")
        print(f"Forma de pagamento: {self.forma}")

