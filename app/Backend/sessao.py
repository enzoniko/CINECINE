from dataclasses import dataclass, field
from random import randint

# Importa a super classe Filme do módulo Filme
from app.Backend.filme import Filme

# Cria a sub classe Sessao que herda de Filme
@dataclass
class Sessao(Filme):
    legenda: bool = False
    DDD: bool = False
    horarios: list[str] = field(default_factory=list)
    id: int = 0

    def __post_init__(self):
        super().__post_init__()
        if self.id == 0:
            self.id = randint(0, 1000000)

