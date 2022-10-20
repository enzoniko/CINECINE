# Importa a sub classe Sessao do módulo sessao
# from app.Backend.sessao import Sessao

# Importa check_1 do módulo helpers
from dataclasses import dataclass, field
from typing import Dict, List
from app.Backend.helpers import check_1
from app.Backend.sessao import Sessao

# from helpers import check_1, printa_matriz

# Constantes de colunas e linhas da matriz de poltronas
COLUNAS: int = 10
LINHAS: int = 15

# Lista de letras para associar letra com número da poltrona
letras: List[str] = ["a", "b", "c", "d", "e", "f", "g",
          "h", "i", "j", "k", "l", "m", "n", "o", "p", "q", "r", "s", "t", "u", "v", "w", "x", "y", "z"][:LINHAS]

# Cria a classe Sala que se associa com a classe Sessao

@dataclass
class Sala:
    cronograma: Dict[str, List] = field(default_factory=dict)
    poltronas: List[List[int]] = field(default_factory=lambda: [[0] * COLUNAS] * LINHAS)
    sessoes: List[Sessao] = field(default_factory=list)

    # Método que preenche a matriz de poltronas com as poltronas a serem preenchidas
    def preencher_poltronas(self, poltronas, id, horario):

        # Lista de letras erradas
        letras_erradas = []
        # Lista de números errados
        numeros_errados = []
        # Lista de poltronas indisponiveis
        poltronas_indisponiveis = []
        # Pra cada poltronas na lista de poltronas a serem preenchidas
        for poltrona in poltronas:
            # Pega a letra da poltrona
            letra = poltrona[0]
            # Pega o número da poltrona
            numero = int(poltrona[1:])
            # Caso as poltronas sejam inválidas adiciona às listas de erradas
            if letra not in letras:
                letras_erradas.append(letra)
            if numero <= 0 or numero > len(
                self.cronograma[f"{id} {horario}"][0]
            ):
                numeros_errados.append(numero)
            if (
                letra in letras
                and numero <= len(self.cronograma[f"{id} {horario}"][0])
                and numero > 0
                and self.cronograma[f"{id} {horario}"][letras.index(letra)][
                    numero - 1
                ]
                == 1
            ):
                poltronas_indisponiveis.append(poltrona)

        # Caso as poltronas sejam inválidas
        if letras_erradas or numeros_errados or poltronas_indisponiveis:
            # Retornas as listas de erradas
            return [letras_erradas, numeros_errados, poltronas_indisponiveis]

        # Se tudo estiver correto
        # Pra cada poltronas na lista de poltronas a serem preenchidas
        for poltrona in poltronas:
            # Pega a letra da poltrona
            letra = poltrona[0]
            # Pega o número da poltrona
            numero = int(poltrona[1:])
            # Pega o índice da letra na lista de letras
            indice = letras.index(letra)
            # Faz uma cópia da linha de índice "incide" da matriz de poltronas
            linha = self.cronograma[f"{id} {horario}"][indice][:]
            # Substitui o número da poltrona pelo valor 1
            linha[numero - 1] = 1
            # Atualiza a linha na matriz de poltronas
            self.cronograma[f"{id} {horario}"][indice] = linha

        # Retorna nenhuma lista de erradas
        return []

    # Método que remove da matriz de poltronas as poltronas a serem removidas
    def esvaziar_poltronas(self, poltronas, id, horario):

        # Pra cada poltronas na lista de poltronas a serem removidas
        for poltrona in poltronas:
            # Pega a letra da poltrona
            letra = poltrona[0]
            # Pega o número da poltrona
            numero = int(poltrona[1:])
            # Pega o índice da letra na lista de letras
            indice = letras.index(letra)
            # Faz uma cópia da linha de índice "incide" da matriz de poltronas
            linha = self.cronograma[f"{id} {horario}"][indice][:]
            # Substitui o número da poltrona pelo valor 0
            linha[numero - 1] = 0
            # Atualiza a linha na matriz de poltronas
            self.cronograma[f"{id} {horario}"][indice] = linha

    def printar_poltronas(self, id, horario):
        # Printa a numeração das colunas
        print(" ", end=" ")
        for coluna in range(len(self.cronograma[f"{id} {horario}"][0]), 0, -1):
            if coluna <= 9:
                print(f"  {coluna}  ", end=" ")
            else:
                print(f"  {coluna} ", end=" ")

        # Printa a letra da linha seguida por cada poltrona da linha
        for linha in range(len(self.cronograma[f"{id} {horario}"]), 0, -1):
            print()
            print(letras[linha - 1], end=" ")
            for coluna in range(len(self.cronograma[f"{id} {horario}"][0]), 0, -1):
                # Bota um x na poltrona se ela estiver ocupada
                print(
                    f"[ {check_1(self.cronograma[f'{id} {horario}'][linha -1][coluna - 1])} ]",
                    end=" ",
                )

        # Printa a posição da TELA
        print()
        t = "TELA"
        print(
            t.center(int(len(self.cronograma[f"{id} {horario}"][0]) * 6) - 4))

    # print_info imprime os informações do cronograma da sala
    def print_info(self):

        # Pra cada sessao na lista de sessões
        for sessao in self.sessoes:
            # Printa o nome da sessão
            print(sessao.nome.upper(), end=" ")
            # Printa as informações da sessão
            sessao.print_info()
            # Pra cada elemento do cronograma
            for chave in self.cronograma:
                # Se o id do elemento for igual ao id da sessão
                if chave.split()[0] == str(sessao.id):
                    # Pra cada horário da sessão
                    for horario in sessao.horarios:
                        # Se o horário do elemento for igual ao horário da sessão
                        if horario == chave.split()[1]:
                            # Printa o horário da sessão
                            print(f"{horario}: ")
                            # Printa a matriz de poltronas respectiva ao horário
                            self.printar_poltronas(sessao.id, horario)
                            print()

    # Função que adiciona uma sessão à sala (cronograma)

    def adicionar_sessao(self, sessao):

        # Pra cada horário da sessão
        for horario in sessao.horarios:

            # Adiciona uma matriz de poltronas vazias no cronograma respectivo ao horário da sessão
            self.cronograma[f"{sessao.id} {horario}"] = self.poltronas[:]

        # Adiciona a sessão à lista de sessões
        self.sessoes.append(sessao)
    # Função que remove sessão da sala (cronograma)

    def remover_sessao(self, sessao):

        # Remove a sessão do cronograma
        # Pra cada horário da sessão
        for horario in sessao.horarios():
            # Se a sessão e seu respectivo horário estiverem no cronograma
            if f"{sessao.id} {horario}" in self.cronograma:
                # Remove a matriz de poltronas do cronograma
                del self.cronograma[f"{sessao.id} {horario}"]

        # Remove a sessão da lista de sessões
        if sessao in self.sessoes:
            self.sessoes.remove(sessao)

    # Função que devolve as sessões que passarão em um determinado horário

    def get_sessao_from_cronograma(self, horario):
        for chave in self.cronograma:
            if horario == chave.split()[1]:
                for sessao in self.sessoes:
                    if str(sessao.id) == chave.split()[0]:
                        sessao.print_info()


# Exemplo de lista de salas
sala1 = Sala()

sala2 = Sala()

salas = [sala1, sala2]
