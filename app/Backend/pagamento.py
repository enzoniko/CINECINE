# Classe Pagamento
class Pagamento():

    # Construtor da classe Pagamento, recebe os atributos do pagamento (ingressos, meias, forma = "Dinheiro")
    def __init__(self, ingressos, meias, forma="Dinheiro"):
        self.ingressos = ingressos
        self.meias = meias
        self.valor = 0
        self.set_valor(ingressos, meias)
        self.forma = forma
        self.id = id(self)

    # get_valor retorna o valor total dos ingressos
    def get_valor(self):
        return self.valor

    # get_forma retorna a forma de pagamento esoclhida pelo usuário
    def get_forma(self):
        return self.forma

    # get_ingressos retorna a quantidade de ingressos comprados
    def get_ingressos(self):
        return self.ingressos

    # get_meias retorna a quantidade de meias-entradas compradas
    def get_meias(self):
        return self.meias

    # set_ingressos modifica a quantidade de ingressos comprados
    def set_ingressos(self, ingressos):
        self.ingressos = ingressos

    # set_meias modifica a quantidade de mais compradas
    def set_meias(self, meias):
        self.meias = meias

    # set_valor modifica o valor, calculando com base nos ingressos e nas meias
    def set_valor(self, ingressos, meias):
        self.valor = 30 * (ingressos - meias) + 15 * meias

    # set_forma modifica a forma de pagamento
    def set_forma(self, forma):
        self.forma = forma

    # print_info imprime os informações da compra
    def print_info(self):
        print(f"Inteiras: {self.get_ingressos() - self.get_meias()}")
        print(f"Meias: {self.get_meias()}")
        print(f"Valor: R${self.get_valor()},00")
        print(f"Forma de pagamento: {self.get_forma()}")
