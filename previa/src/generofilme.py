
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

def get_movie_genres(movie_id):
  movie_tools = tmdb.Movie()
  movie = movie_tools.details(movie_id)
  if movie['genres'] != None:
    return movie['genres']
  return None

def get_movies_genres(movies_ids):
  return list(map(get_movie_genres, movies_ids))

def build_genre_movie_csv(movies_ids:list, movies_genres:list, fieldnames:list):
  with open('GeneroFilme.csv', 'w', newline='') as gm_csv:
    writer = csv.DictWriter(gm_csv, fieldnames=fieldnames)
    writer.writeheader()
    for i in range(len(movies_ids)):
      for genre in movies_genres[i]:
        if genre != None:
          ms = {fieldnames[0]: genre['name'], fieldnames[1]: movies_ids[i]}
          writer.writerow(ms)


def gerar_tabela_genero():
  movies = pd.read_csv('Filme.csv')

  movies_ids = movies['id_TMDB']
  movies_genres = get_movies_genres(movies_ids)
  atributos = ['nome_genero', 'id_filme_TMDB']
  build_genre_movie_csv(movies_ids, movies_genres, atributos)

gerar_tabela_genero()