from dataclasses import dataclass, field
from typing import Dict, List
from app.Backend.sessao import Sessao

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
        letras_erradas: List[str] = []
        # Lista de números errados
        numeros_errados: List[int] = []
        # Lista de poltronas indisponiveis
        poltronas_indisponiveis: List[str] = []
        # Pra cada poltronas na lista de poltronas a serem preenchidas
        for poltrona in poltronas:
            # Pega a letra da poltrona
            letra: str = poltrona[0]
            # Pega o número da poltrona
            numero: int = int(poltrona[1:])
            # Caso as poltronas sejam inválidas adiciona às listas de erradas
            if letra not in letras:
                letras_erradas.append(letra)
            if numero <= 0 or numero > len(self.cronograma[f"{id} {horario}"][0]):
                numeros_errados.append(numero)
            if (letra in letras and numero <= len(self.cronograma[f"{id} {horario}"][0]) and numero > 0 and self.cronograma[f"{id} {horario}"][letras.index(letra)][numero - 1] == 1):
                poltronas_indisponiveis.append(poltrona)

        # Caso as poltronas sejam inválidas
        if letras_erradas or numeros_errados or poltronas_indisponiveis:
            # Retornas as listas de erradas
            return [letras_erradas, numeros_errados, poltronas_indisponiveis]

        # Se tudo estiver correto
        # Pra cada poltronas na lista de poltronas a serem preenchidas
        for poltrona in poltronas:
            # Pega a letra da poltrona
            letra: str = poltrona[0]
            # Pega o número da poltrona
            numero: int = int(poltrona[1:])
            # Pega o índice da letra na lista de letras
            indice = letras.index(letra)
            # Faz uma cópia da linha de índice "incide" da matriz de poltronas
            linha: List[int] = self.cronograma[f"{id} {horario}"][indice][:]
            # Substitui o número da poltrona pelo valor 1
            linha[numero - 1]: int = 1
            # Atualiza a linha na matriz de poltronas
            self.cronograma[f"{id} {horario}"][indice]: List[int] = linha

        # Retorna nenhuma lista de erradas
        return []

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
        for horario in sessao.horarios:
            # Se a sessão e seu respectivo horário estiverem no cronograma
            if f"{sessao.id} {horario}" in self.cronograma:
                # Remove a matriz de poltronas do cronograma
                del self.cronograma[f"{sessao.id} {horario}"]

        # Remove a sessão da lista de sessões
        if sessao in self.sessoes:
            self.sessoes.remove(sessao)

