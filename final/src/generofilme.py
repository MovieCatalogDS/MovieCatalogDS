import tmdbv3api as tmdb
import csv
import json
import pandas as pd

def config_api():
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


def get_genres():
  genre_tools = tmdb.Genre()
  return genre_tools.movie_list()

def build_genres_csv(genres:list, fieldnames:list, mfields:list):
  with open('../data/processed/Genero.csv', 'w', newline='') as genres_csv:
    writer = csv.DictWriter(genres_csv, fieldnames=fieldnames)
    writer.writeheader()
    for genre in genres:
      ms = dict()
      for i in range(len(fieldnames)):
        ms[fieldnames[i]] = genre[mfields[i]]
      writer.writerow(ms)

def genre_table():
  movie_genres = get_genres()
  atributos = ['nome']
  atributos_ingles = ['name']
  build_genres_csv(movie_genres, atributos, atributos_ingles)

def get_movie_genres(movie_id):
  movie_tools = tmdb.Movie()
  movie = movie_tools.details(movie_id)
  if movie['genres'] != None:
    return movie['genres']
  return None

def get_movies_genres(movies_ids):
  return list(map(get_movie_genres, movies_ids))

def build_genre_movie_csv(movies_ids:list, movies_genres:list, fieldnames:list):
  with open('../data/processed/GeneroFilme.csv', 'w', newline='') as gm_csv:
    writer = csv.DictWriter(gm_csv, fieldnames=fieldnames)
    writer.writeheader()
    for i in range(len(movies_ids)):
      for genre in movies_genres[i]:
        if genre != None:
          ms = {fieldnames[0]: genre['name'], fieldnames[1]: movies_ids[i]}
          writer.writerow(ms)


def gerar_tabela_genero():
  config_api() # configura o idioma da api
  genre_table() # Criar tabela de generos

  movies = pd.read_csv('../data/processed/Filme.csv')

  movies_ids = movies['id_TMDB']
  movies_genres = get_movies_genres(movies_ids)
  atributos = ['nome_genero', 'id_filme_TMDB']
  build_genre_movie_csv(movies_ids, movies_genres, atributos)

if __name__ == "__Main__":
  gerar_tabela_genero()