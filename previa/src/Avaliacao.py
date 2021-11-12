import pandas as pd
import imdb
from tmdbv3api import TMDb
from tmdbv3api import Movie


''' 

    Essa func depende do arquivo "Avaliador.csv" e "Filme.csv"
    Arquivos necessarios devem estar dentro da pasta "data"
    Obs. Execução lenta
    #ra221329

'''


imdb_obj = imdb.IMDb()
tmdb = TMDb()
tmdb.api_key = ''


def load_csv(file_name="", index_col="id_TMDB"):
    try:
        file_name += '.csv'
        return pd.read_csv(file_name, index_col=index_col)

    except FileNotFoundError:
        print("Arquivo [" + file_name + "] nao encontrado!")


def write_csv(dataframe, name='out', indice=True):
    # Grava csv com nome dado ou out.csv por padrao
    filename = name + '.csv'
    dataframe.to_csv("data/" + filename, index=indice)
    print("Arquivo salvo com nome " + filename)


def get_imdb_movie_grade(imdb_id, imdb_obj):
    ''' Baixa nota do site e retorna ela em escala de 0 a 10 '''
    movie = imdb_obj.get_movie(imdb_id)

    return movie['rating']


def get_tmdb_movie_grade(movie_id):
    return Movie().details(movie_id).vote_average


def get_grade(evaluator, movie_title, imdb_movie_id, movie_id):
    ''' Seleciona o avaliador e chama funcao para pegar
        nota do filme (devolver nota entre 0 a 10)
        ADD novos avaliadores aqui '''
    if evaluator == 'imdb':
        return get_imdb_movie_grade(imdb_movie_id, imdb_obj)
    if evaluator == 'tmdb':
        return get_tmdb_movie_grade(movie_id)


def load_grades(movie_id, imdb_movie_id, movie_title, evaluator_id_list):       # aqui tenho um unico filme
    movie_in_evaluators = []

    for evaluator in evaluator_id_list:
        movie_grade = get_grade(evaluator, movie_title, imdb_movie_id, movie_id)
        if movie_grade:
            movie_in_evaluators.append((evaluator, movie_id, movie_grade))

    return movie_in_evaluators


def avaliacao():
    df = load_csv("data/Avaliador", "id")
    evaluator_id_list = df.index.to_list()
    movie = load_csv("data/filme")

    itens_amount = str(len(movie.index))
    counter = 0
    grades_table = []

    print("Serao processados " + itens_amount + " filmes!")

    for index, row in movie.iterrows():
        counter += 1
        print(str(counter) + "/" + itens_amount)
        grades_table += load_grades(index, row['id_IMDB'][2:], row['titulo_original'], evaluator_id_list)

    grades_df = pd.DataFrame(grades_table, columns=['id_avaliador', 'id_filme_TMDB', 'nota'])

    return grades_df


grades = avaliacao()
write_csv(grades, 'Avaliacao', indice=False)
