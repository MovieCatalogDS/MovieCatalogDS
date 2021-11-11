

import tmdbv3api as tmdb
import csv
import json
import pandas as pd

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

# Retorna o id da coleção que o filme pertence
# se o filme não tem a coleção registrada retorna -1
def get_movie_collection_id(movie_id):
  movie_tools = tmdb.Movie()
  movie_collection = movie_tools.details(movie_id)
  if movie_collection['belongs_to_collection'] != None:
    return movie_collection['belongs_to_collection']['id']
  return -1

# Retorna o id da coleção de cada filme da lista
def get_collections_ids(movies_ids):
  return list(map(get_movie_collection_id, movies_ids))

def get_collection(collection_id):
  collection_tools = tmdb.Collection()
  return collection_tools.details(collection_id)

def find_movie_sequel(movie_id, movie_year, collection):
  min_year = 2022
  year = 0
  sequel_id = -1
  for movie in collection['parts']:
    if movie['id'] != movie_id:
      if 'release_date' not in movie.keys():
        continue

      date = movie['release_date'].split('-')
      if date[0] != '':
        year = int(date[0])
      if movie_year < year < min_year:
        min_year = year
        sequel_id = movie['id']
  
  return sequel_id

def get_movie_sequel(movie_id, movie_year):
  collection_id = get_movie_collection_id(movie_id)
  if collection_id != -1:
    collection = get_collection(collection_id)
    return find_movie_sequel(movie_id, movie_year, collection)
  return -1

def get_sequels_ids(movies_ids, movies_years):
  return list(map(get_movie_sequel, movies_ids, movies_years))

def build_sequel_list_csv(movies_ids:list, sequels_ids, fieldnames:list):
  with open('Sequencia.csv', 'w', newline='') as sequel_csv:
    writer = csv.DictWriter(sequel_csv, fieldnames=fieldnames)
    writer.writeheader()
    for i in range(len(movies_ids)):
      ms = {fieldnames[0]: movies_ids[i], fieldnames[1]: sequels_ids[i]}
      writer.writerow(ms)

def corrigir_ano(ano):
  if type(ano) == str:
    ano = ano.split('-')[0]
  
  return int(ano)

def gerar_tabela_sequencia():

  movies = pd.read_csv('Filme.csv')
  ids = movies['id_TMDB']


  years = movies['ano']
  years = list(map(corrigir_ano, years))
  sequels_ids = get_sequels_ids(ids, years)
  atributos = ['id_filme_TMDB', 'id_filme_sequencia_TMDB']
  build_sequel_list_csv(ids, sequels_ids, atributos)

gerar_tabela_sequencia()