
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
api.language = 'en-US'

"""# **Ponto de Entrada**"""

def get_movie_infos(movie_id):
  movie_tools = tmdb.Movie()
  movie = movie_tools.details(movie_id)
  return {
            'collection': movie['belongs_to_collection'],
            'keywords': movie['keywords']['keywords']
         }

def fit_collection_words(words):
  false_keywords = ['the', 'of', 'a', 'o', 'an']
  for word in words:
    if word.lower() in false_keywords:
      words.remove(word)

def franchise_is_collection_2(collection, fcs):
  for fc in fcs:
    words = fc.split()
    count = 0
    match_words = []
    for word in words:
      if word in collection:
        count += 1
        match_words.append(word)
    if count >= 1 and not (
        ('The' in match_words and len(match_words) == 1) or
        ('of the' in fc and len(match_words) == 2)):
      return fc
  return 'Not Collection'

def franchise_is_collection(collection, fcs):
  for fc in fcs:
    words = fc.split()
    fit_collection_words(words)
    count = 0
    match_words = []
    for word in words:
      if word in collection:
        count += 1
        match_words.append(word)
    if ((count == 1 and len(words) == 1) or
        count >= 2):
      return fc
  return 'Not Collection'

def franchise_is_keyword(keywords, fcs):
  for fc in fcs:
      word = fc.lower()
      for keyword in keywords:
        if word in keyword['name']:
          return fc
  return 'Not keyword'

def find_movie_franchise(fcs, movie_id, match_results):
  movie_infos = get_movie_infos(movie_id)
  collection = movie_infos['collection']
  result = ''
  if collection != None:
    collection_name = collection['name']
    result = franchise_is_collection(collection_name, fcs)
    if result != 'Not Collection':
      match_results.append({
          'nome_franquia': result,
          'id_filme_TMDB': movie_id
      })
    else:
      fcs.append(collection_name)
      match_results.append({
          'nome_franquia': collection_name,
          'id_filme_TMDB': movie_id
      })      

  keywords = movie_infos['keywords']
  keyword_result = franchise_is_keyword(keywords, fcs)
  if keyword_result not in ['Not keyword', result]:
      match_results.append({
          'nome_franquia': keyword_result,
          'id_filme_TMDB': movie_id
      })    
  
def build_franchise_films_rows(fcs, films):
  rows = []
  for film in films:
    find_movie_franchise(fcs, film, rows)
  
  return rows


def build_movie_list_csv(rows:list):
  fieldnames = ['nome_franquia', 'id_filme_TMDB']
  with open('FranquiaFilme.csv', 'w', newline='') as ff_csv:
    writer = csv.DictWriter(ff_csv, fieldnames=fieldnames)
    writer.writeheader()
    for row in rows:
      writer.writerow(row)


def gerar_tabela_franquia():
  fcs = pd.read_csv('Franquia.csv')
  fcs_names = list(fcs['nome'])
  #fcs_names.remove('Alien')
  #print(fcs_names[0].split())

  films = pd.read_csv('Filme.csv')
  films_ids = films['id_TMDB']
  #print(films_ids)

  rows = build_franchise_films_rows(fcs_names, films_ids)
  build_movie_list_csv(rows)


  ff = pd.read_csv('FranquiaFilme.csv')
  #print(ff['nome_franquia'].nunique())

  teste = ff.groupby('nome_franquia').count()
  teste.columns = ['num_filmes']
  teste.to_csv('Franquia.csv', encoding='utf-8', index=True)

  franquia = pd.read_csv('Franquia.csv')
  franquia.columns = ['nome','num_filmes']
  franquia = franquia.drop(columns=['num_filmes'])
  franquia.to_csv('Franquia.csv', encoding='utf-8', index=False)

gerar_tabela_franquia()