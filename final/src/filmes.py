
# **Instalar Biblioteca do TMDB**
"""

"""# **Importar Bibliotecas**"""

import tmdbv3api as tmdb
import csv
import json

"""# **Configuração da API do TMDB**"""

"""# **Funções**

## **Obter dos Filmes no TMDB**
"""
def config_tmbd():
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

# Retorna um dicionário com todos os detalhes que a api do TMDB fornece
def get_movie_details(movie):
  movie_tools = tmdb.Movie()
  id = movie['id']
  return movie_tools.details(id)

# Retorna uma lista com os filmes em uma página do TMDB
# Cada página costuma ter 20 filmes
def get_movies_in_page(page, sort_by:str):
  discover = tmdb.Discover()
  movie_list = discover.discover_movies({
      'primary_release_date.gte': '1970-01-01',
      'primary_release_date.lte': '2021-12-31',
      'sort_by': sort_by,
      'page': page
  })
  return list(map(get_movie_details, movie_list))

# Ober uma lista de filmes extraidos de quantidade de páginas (num_pages)
# Cada Filme é um dicionario em que os campos são as informações do filme
# Podemos passar a página inicial de busca e o passo para as outras páginas
# Cada página têm 20 filmes, o número de filmes obtidos no total é 20*num_pages
def get_movies(num_pages:int, sort_by:str, start_page=1, step=1):
  movies = []
  for i in range(num_pages):
    movies += get_movies_in_page(start_page + i*step, sort_by)
  return movies

"""## **Gerar arquivo CSV**"""

# Construir um dicionário contendo só as informações desejadas
# do filme (fieldnames)
def build_movie_struct(movie, fieldnames, moviefields):
  movie_struct = dict()
  for i in range(len(fieldnames) - 1):
    movie_struct[fieldnames[i]] = movie[moviefields[i]]

  movie_struct['num_oscars'] = 0
  movie_struct['classificacao'] = 'desconhecida'

  ano = movie_struct['ano']
  if type(ano) == str and '-' in ano:
    movie_struct['ano'] = ano.split('-')[0]

  return movie_struct

# Cria um arquivo csv com os filme obtidos do TMDB
# No csv adicionamos alguns dos campos fornecidos pelo TMDB (mfields)
# dependendo dos campos que queremos (fieldnames)
def build_movie_list_csv(file_name:str, movies:list, fieldnames:list, mfields:list, p_num:int):
  count = 0
  total = len(movies)
  with open(file_name, 'w', newline='') as movies_csv:
    writer = csv.DictWriter(movies_csv, fieldnames=fieldnames)
    writer.writeheader()
    for movie in movies:
      count += 1
      print(f'pr({p_num}) - Carregando Filme #{count} - {count*100/total:.2f}% Concluído')
      ms = build_movie_struct(movie, fieldnames, mfields)
      writer.writerow(ms)


"""# **Ponto de Entrada**"""
def gerar_tabala_filmes(num_pages:int, order_by:str, file_name:str, start_page:int, p_num):
  
  # Configurar a linguagem do tmdb 
  config_tmbd()

  print(f'pr({p_num}) - Obtendo Filmes do TMDB para a tabela {file_name}')
  # obter a lista de filmes
  movies = get_movies(num_pages, order_by, start_page=start_page)

  # Informações Necessárias no CSV
  atributos = ["id_TMDB", "id_IMDB", "titulo", "titulo_original", "sinopse", "duracao", "ano", 
               "classificacao", "situacao", "idioma_original", 
               "orcamento", "receita", "num_oscars"]

  # Campos com as informações no objeto do filme do TMDB
  atributos_tmdb = ["id", "imdb_id", "title", "original_title", "overview", "runtime",
                    "release_date", "adult", "status","original_language",
                    "budget", "revenue"]

  print(f'pr({p_num}) - Gerando Tabela: {file_name}')
  # Criar o arquivo csv
  build_movie_list_csv(file_name, movies, atributos, atributos_tmdb, p_num)
