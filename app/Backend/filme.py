# Importa a função lista_strings_para_string do módulo helpers

from dataclasses import dataclass, field
from typing import List
from app.Backend.helpers import lista_strings_para_string
from tmdbv3api import TMDb, Movie
import requests
tmdb = TMDb()
tmdb.api_key = 'f9a4d2a566e2cdd42678ca575cf769c0'
tmdb.language = 'pt'
movie = Movie()


# Importa a função lista_strings_para_string do módulo helpers
# from helpers import lista_strings_para_string

# Cria a super classe Filme

@dataclass
class Filme:
    nome: str = ""
    generos: List[str] = field(default_factory=list)
    classificacao: str = ''
    description: str = ""
    imagem: str = ''
       
    def __post_init__(self):
        if not (search := movie.search(self.nome)[0]):
            return
        self.nome = search.original_title
        self.description = search.overview
        self.classificacao = '+18' if search.adult else '+12'
        self.imagem = f'https://image.tmdb.org/t/p/original{search.poster_path}'
        movie_id = search.id
        response = requests.get(f'https://api.themoviedb.org/3/movie/{movie_id}?api_key={tmdb.api_key}&language=pt-BR')

        data_json = response.json()
        if data_json['genres']:
            for i in range(len(data_json['genres'])):
                self.generos.append(data_json['genres'][i]['name'])
           
        