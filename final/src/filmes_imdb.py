from imdb import IMDb
import pandas as pd

# Obtem informações sobre um filme no imdb
def get_imdb_movie_data(imdb, movie_id):
  return imdb.get_movie(movie_id, info=['main', 'awards'])

# Obter a classificação do filme
def get_certification(movie):
  if 'certificates' in movie.keys():
    certificates = movie['certificates']
    for i in certificates:
      if i.find('United States') != -1:
        return i
  return 'desconhecida'

# Obter o número de oscars do filme
def get_oscars(movie):
  if 'awards' not in movie.keys():
    return 0

  n_oscars = 0
  for award in movie['awards']:
    if award['award'].find('Oscar') != -1:
      if award['result'] == 'Winner':
        n_oscars+=1
  return n_oscars  

def save_error(e, movie, index):
    with open('movie_erro.txt', 'a') as file:
        file.write(f'Erro:{e} - Nome do Filme: {movie} - Posição na Tabela: {index}\n')

# Inserir os detalhes adicionais do filme na tabela
def insert_movie_details(imdb, movie_table, p_num):
    print('inserir detalhes do filme:')
    num_movies = len(movie_table.index) 
    for index, row in movie_table.iterrows():
        try:
            print(f'pr({p_num}) - Filme #{index+1} - {(index+1)*100/num_movies:.2f}% Concluído')
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
            num_oscars = get_oscars(movie)
            movie_table.loc[index,'num_oscars'] = int(num_oscars)
        except Exception as e:
            movie_name = movie_table.loc[index,'titulo']
            save_error(e, movie_name, index)


# Inserir Classificação, Ano e Nacionalidade dos filmes usando o IMDB
# Inserir número de Oscars dos filmes usando IMDB

def get_more_movie_infos(table_name, p_num):
    imdb = IMDb()
    movies_table = pd.read_csv(table_name)
    try:
        insert_movie_details(imdb, movies_table, p_num)
        #movies_table.to_csv(table_name, encoding='utf-8', index=False)
    finally:
        movies_table.to_csv(table_name, encoding='utf-8', index=False)