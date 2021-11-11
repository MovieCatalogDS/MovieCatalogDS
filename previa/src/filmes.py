
# **Instalar Biblioteca do TMDB**
"""

"""# **Importar Bibliotecas**"""

import tmdbv3api as tmdb
from imdb import IMDb
import pandas as pd
import csv
import json

"""# **Configuração da API do TMDB**"""

# instanciar a configuração da api
api = tmdb.TMDb()

# Ler a key para a api a partir de um arquivo
# Subir um json com a sua key no colab
with open('key.json', 'r') as f:
  key = f.read()

key = json.loads(key)
key = key['key']

# Pode subistituir key pela string da key diretamente também
api.api_key = key
# Configura o idioma de resposta da api
api.language = 'pt-BR'

"""# **Funções**

## **Obter dos Filmes no TMDB**
"""

# Retorna um dicionário com todos os detalhes que a api do TMDB fornece
def get_movie_details(movie):
  movie_tools = tmdb.Movie()
  id = movie['id']
  return movie_tools.details(id)

# Retorna uma lista com os filmes em uma página do TMDB
# Cada página costuma ter 20 filmes
def get_movies_in_page(page):
  discover = tmdb.Discover()
  movie_list = discover.discover_movies({
      'primary_release_date.gte': '1900-01-01',
      'primary_release_date.lte': '2021-12-31',
      'sort_by': 'revenue.desc',
      'page': page
  })
  return list(map(get_movie_details, movie_list))

# Ober uma lista de filmes extraidos de quantidade de páginas (num_pages)
# Cada Filme é um dicionario em que os campos são as informações do filme
# Podemos passar a página inicial de busca e o passo para as outras páginas
# Cada página têm 20 filmes, o número de filmes obtidos no total é 20*num_pages
def get_movies(num_pages, start_page=1, step=1):
  movies = []
  for i in range(num_pages):
    movies += get_movies_in_page(start_page + i*step)
  return movies

"""## **Gerar arquivo CSV**"""

# Construir um dicionário contendo só as informações desejadas
# do filme (fieldnames)
def build_movie_struct(movie, fieldnames, moviefields):
  movie_struct = dict()
  for i in range(len(fieldnames)):
    movie_struct[fieldnames[i]] = movie[moviefields[i]]
  return movie_struct

# Cria um arquivo csv com os filme obtidos do TMDB
# No csv adicionamos alguns dos campos fornecidos pelo TMDB (mfields)
# dependendo dos campos que queremos (fieldnames)
def build_movie_list_csv(movies:list, fieldnames:list, mfields:list):
  with open('Filme.csv', 'w', newline='') as movies_csv:
    writer = csv.DictWriter(movies_csv, fieldnames=fieldnames)
    writer.writeheader()
    for movie in movies:
      ms = build_movie_struct(movie, fieldnames, mfields)
      writer.writerow(ms)


def get_imdb_movie_data(imdb, movie_id):
  return imdb.get_movie(movie_id)

def get_certification(movie):
  if 'certificates' in movie.keys():
    certificates = movie['certificates']
    for i in certificates:
      if i.find('United States') != -1:
        return i
  return 'desconhecida'

def insert_movie_details(imdb,movie_table):
  print('inserir detalhes do filme:')
  for index, row in movie_table.iterrows():
    print(f'filme número {index}')
    imdb_id = row['id_IMDB']
    if type(imdb_id) != str or imdb_id == "":
      continue
    movie_id = int(imdb_id[2:])
    movie = get_imdb_movie_data(imdb, movie_id)
    if 'year' in movie.keys():
      year = movie['year']
      movie_table.loc[index,'ano'] = year
    certification = get_certification(movie)
    movie_table.loc[index,'classificacao'] = certification

def get_num_oscars(imdb, movie_id):
  movie = imdb.get_movie(movie_id, info=['awards'])
  if 'awards' not in movie.keys():
    return 0

  n_oscars = 0

  for award in movie['awards']:
    if award['award'].find('Oscar') != -1:
      if award['result'] == 'Winner':
        n_oscars+=1

  return n_oscars

def insert_num_oscars(imdb, movie_table):
  print('inserir número de Oscars do filme:')
  for index, row in movie_table.iterrows():
    print(f'filme número {index}')
    imdb_id = row['id_IMDB']
    if type(imdb_id) != str or imdb_id == "":
      continue
    movie_id = int(imdb_id[2:])
    num_oscars = get_num_oscars(imdb, movie_id)
    movie_table.loc[index,'num_oscars'] = int(num_oscars)

"""# **Ponto de Entrada**"""
def gerar_tabala_filmes():
  # obter a lista de filmes (100 no total)
  # movies = get_movies(100)

  # # Informações Necessárias no CSV
  # atributos = ["id_TMDB", "id_IMDB", "titulo", "titulo_original", "sinopse", "duracao", "ano", 
  #              "classificacao", "situacao", "idioma_original", 
  #              "orcamento", "receita", "num_oscars"]

  # # Campos com as informações no objeto do filme do TMDB
  # atributos_tmdb = ["id", "imdb_id", "title", "original_title", "overview", "runtime",
  #                   "release_date", "adult", "status","original_language",
  #                   "budget", "revenue", "popularity"]

  # # Criar o arquivo csv
  # build_movie_list_csv(movies, atributos, atributos_tmdb)

  # Inserir Classificação, Ano e Nacionalidade dos filmes usando o IMDB
  # Inserir número de Oscars dos filmes usando IMDB
  imdb = IMDb()
  movies_table = pd.read_csv('Filme.csv')
  insert_movie_details(imdb, movies_table)
  movies_table.to_csv('Filme.csv', encoding='utf-8', index=False)
  movies_table = pd.read_csv('Filme.csv')
  insert_num_oscars(imdb, movies_table)
  movies_table.to_csv('Filme.csv', encoding='utf-8', index=False)
