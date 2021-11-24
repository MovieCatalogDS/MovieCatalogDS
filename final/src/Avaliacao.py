import pandas as pd
import imdb
from tmdbv3api import TMDb
from tmdbv3api import Movie
import multiprocessing
import time

''' 

    Essa func depende do arquivo "Avaliador.csv" e "Filme.csv"
    Arquivos necessarios devem estar dentro da pasta "data"
    Obs. Execução lenta
    #ra221329

'''

threads_number = 12

#load_path = "../data/tmp_data/"  # path de testes
load_path = "../data/processed/"      #path definitivo do github
save_path = load_path

imdb_obj = imdb.IMDb()
tmdb = TMDb()

with open(load_path + 'key.txt') as f:
    tmdb.api_key = f.readline()

total_progress = 0
current_progress = multiprocessing.Value('i', 0)


def load_csv(file_name="", index_col="id_TMDB"):
    try:
        file_name += '.csv'
        return pd.read_csv(load_path + file_name, index_col=index_col)

    except FileNotFoundError:
        print("Arquivo [" + file_name + "] nao encontrado!")


def write_csv(dataframe, name='out', indice=True):
    # Grava csv com nome dado ou out.csv por padrao
    filename = name + '.csv'
    dataframe.to_csv(save_path + filename, index=indice)
    print("Arquivo salvo com nome " + filename)


def get_imdb_movie_grade(imdb_id, imdb_obj, retry=False):
    ''' Baixa nota do site e retorna ela em escala de 0 a 10 '''
    rating = None
    if imdb_id:
        try:
            movie = imdb_obj.get_movie(imdb_id)
            rating = movie['rating']

            if retry:
                print("Filme " + str(imdb_id) + " adquirido com sucesso!")
        except Exception as e:
            print(e)
            if not retry:
                print("Imdb - Erro na requisição do filme " + str(imdb_id) + ". Tentando novamente em 5s!")
                time.sleep(5)
                rating = get_imdb_movie_grade(imdb_id, imdb_obj, retry=True)
        finally:
            return rating


def get_tmdb_movie_grade(movie_id, retry=False):
    rating = None
    try:
        rating = Movie().details(movie_id).vote_average

        if retry:
            print("Filme " + str(movie_id) + " adquirido com sucesso!")
    except Exception as e:
        print(e)
        if not retry:
            print("Tmdb - Erro na requisição do filme " + str(movie_id) + ". Tentando novamente em 5s!")
            time.sleep(5)
            rating = get_tmdb_movie_grade(movie_id, retry=True)
    finally:
        return rating


def get_rotten_tomatoes_movie_grade(rt_movie, movie_info):
    try:
        for index, row in rt_movie.iterrows():
            release_year = str(row['original_release_date']).partition("-")[0]
            if row['movie_title'] == movie_info['titulo'] and release_year == str(movie_info['ano']) and row[
                'tomatometer_rating']:
                return int(row['tomatometer_rating']) / 10
    except Exception as e:
        print(e)
        print("Rotten Tomatoes - Erro na requisicao do filme: " + str(movie_info['titulo']) + ". Pulando esse!")


def get_grade(evaluator, movie_info, imdb_movie_id, movie_id, rt_movie):
    ''' Seleciona o avaliador e chama funcao para pegar
        nota do filme (devolver nota entre 0 a 10)
        ADD novos avaliadores aqui '''
    grade = None

    if evaluator == 'imdb':
        grade = get_imdb_movie_grade(imdb_movie_id, imdb_obj)
    elif evaluator == 'tmdb':
        grade = get_tmdb_movie_grade(movie_id)
    elif evaluator == 'rottentomatoes':
        grade = get_rotten_tomatoes_movie_grade(rt_movie, movie_info)

    return grade


def load_grades(movie_id, imdb_movie_id, movie_info, evaluator_id_list, rt_movie):  # aqui tenho um unico filme
    movie_in_evaluators = []

    for evaluator in evaluator_id_list:
        movie_grade = get_grade(evaluator, movie_info, imdb_movie_id, movie_id, rt_movie)
        if movie_grade:
            movie_in_evaluators.append((evaluator, movie_id, movie_grade))

    return movie_in_evaluators


def load_grades_single_thread(movies, evaluator_id_list, rt_movie):
    global total_progress
    counter = 0
    grades_table = []

    for index, row in movies.iterrows():
        counter += 1
        print(str(counter) + "/" + str(total_progress))
        movie_info = {"titulo": row['titulo_original'], "duracao": row['duracao'], "ano": row['ano']}
        imdb_id = None

        if type(row['id_IMDB']) == type(str("")):
            imdb_id = row['id_IMDB'][2:]
        grades_table += load_grades(index, imdb_id, movie_info, evaluator_id_list, rt_movie)

    return grades_table


def show_status(progress, last_percent_status):
    global current_progress, total_progress
    current_progress_percent = ((current_progress.value + progress) * 100) // total_progress

    if last_percent_status != current_progress_percent and current_progress_percent % 2 == 0:
        with current_progress.get_lock():
            current_progress.value += progress
        progress = 0
        print(str(current_progress.value) + "/" + str(total_progress) + " --> " + str(current_progress_percent) + "%")

    last_percent_status = current_progress_percent

    return progress, last_percent_status


def load_grades_multi_thread(movies, evaluator_id_list, rt_movie, return_list):
    local_progress = 0
    last_percent_status = 0

    for index, row in movies.iterrows():
        local_progress += 1
        local_progress, last_percent_status = show_status(local_progress, last_percent_status)
        movie_info = {"titulo": row['titulo_original'], "duracao": row['duracao'], "ano": row['ano']}
        imdb_id = None

        if type(row['id_IMDB']) == type(str("")):
            imdb_id = row['id_IMDB'][2:]
        return_list += load_grades(index, imdb_id, movie_info, evaluator_id_list, rt_movie)


def grades_loader(movies, evaluator_id_list, rt_movie):
    global threads_number
    size_movie_id_list = len(movies)
    size_per_thread = size_movie_id_list // threads_number

    if size_per_thread >= 1:
        jobs = []
        manager = multiprocessing.Manager()
        return_list = manager.list()
        print("Modo multi-thread!")
        print("Tempo total estimado:" + str(0.008 * total_progress) + "m")

        for thread in range(threads_number):
            last_pos = size_per_thread * (thread + 1)
            if thread + 1 == threads_number:
                last_pos = None

            process = multiprocessing.Process(target=load_grades_multi_thread,
                                              args=(
                                                  movies[size_per_thread * thread:last_pos], evaluator_id_list,
                                                  rt_movie,
                                                  return_list))
            jobs.append(process)
            process.start()

        for proc in jobs:
            proc.join()

        grades_table = list(return_list)
    else:
        print("Modo single-thread!")
        print("Tempo total estimado:" + str(0.08 * total_progress) + "m")
        grades_table = load_grades_single_thread(movies, evaluator_id_list, rt_movie)

    return grades_table


def avaliacao():
    global total_progress
    df = load_csv("Avaliador", "id")
    evaluator_id_list = df.index.to_list()
    movie = load_csv("Filme")
    rt_movie = load_csv("RT_db", "rotten_tomatoes_link")

    total_progress = len(movie.index)

    print("Serao processados " + str(total_progress) + " filmes!")
    grades_table = grades_loader(movie, evaluator_id_list, rt_movie)

    grades_df = pd.DataFrame(grades_table, columns=['id_avaliador', 'id_filme_TMDB', 'nota'])

    return grades_df


grades = avaliacao()
print(grades)
write_csv(grades, 'Avaliacao', indice=False)
