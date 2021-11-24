import pandas as pd
from tmdbv3api import TMDb
from tmdbv3api import Person
import imdb
import time
import multiprocessing
import json

''' 
    
    Esse cod depende do arquivo "PessoaFilme.csv" e chave da API do tmdb em "key.txt"
    Arquivos necessarios devem estar dentro de load_path
    Caso surja erro na consulta de alguma pessoa essa sera pulada sem comprometer as demais
    Obs. Execução lenta
    #ra221329
    
'''

threads_number = 12     # max 12, diminuir caso der erro 503

#load_path = "../data/tmp_data/"        #path de testes
load_path = "../data/processed/"      #path definitivo do github
save_path = load_path

tmdb = TMDb()
imdb_obj = imdb.IMDb()
person_obj = Person()

# with open(load_path + 'key.txt') as f:
#     tmdb.api_key = f.readline()

total_progress = 0
current_progress = multiprocessing.Value('i', 0)

def config_tmbd():
    global tmdb
    # Ler a key para a api a partir de um arquivo
    # Subir um json com a sua key no colab
    with open('key.json', 'r') as f:
        key = f.read()

        key = json.loads(key)
        key = key['key']

        # Pode subistituir key pela string da key diretamente também
        tmdb.api_key = key

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


def get_awards_number(imdb_person_id):
    awards_amount = 0
    if imdb_person_id:
        person_id = imdb_person_id[2:]
        try:
            person_awards = imdb_obj.get_person_awards(person_id)['data']

            if 'awards' in person_awards:
                for award in person_awards['awards']:
                    if award and 'result' in award and award['result'] == 'Winner' and award['prize'] == 'Oscar':
                        awards_amount += 1
        except ConnectionResetError as err:
            print("Erro de conexao com " + imdb_person_id + "! Tentando novamente em 5 segundos...")
            time.sleep(5)
            return get_awards_number(imdb_person_id)
        except Exception as error:
            print("Imdb - Erro na consulta da pessoa: " + str(imdb_person_id))
            print(error)
            print("Continuando sem ela!")
        finally:
            return awards_amount
    return awards_amount


def load_person(person_id):
    a_person = ()

    try:
        person_data = person_obj.details(person_id)     # aqui demora! (proporcinal ao numero de linhas em PessoaFilme.csv)

        imdb_person_id = person_data['imdb_id']
        number_of_awards = get_awards_number(imdb_person_id)

        a_person = (person_id, imdb_person_id, person_data['name'], person_data['place_of_birth'], number_of_awards)
    except Exception as e:
        print(str(person_id) + ":" + str(e))
    finally:
        return a_person


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


def call_load_person(person_id_list, return_list):
    local_progress = 0
    last_percent_status = 0

    for person_id in person_id_list:
        local_progress += 1
        local_progress, last_percent_status = show_status(local_progress, last_percent_status)

        person_line = load_person(person_id)

        if person_line:
            return_list.append(person_line)


def call_load_person_single_thread(person_id_list, total_size):
    counter = 0
    person_list = []

    for person_id in person_id_list:
        counter += 1
        print(str(counter) + "/" + str(total_size))
        person_list.append(load_person(person_id))

    return person_list


def person_loader(person_id_list):
    config_tmbd()
    global threads_number
    size_person_id_list = len(person_id_list)
    size_per_thread = size_person_id_list // threads_number

    if size_per_thread >= 1:
        jobs = []
        manager = multiprocessing.Manager()
        return_list = manager.list()
        print("Modo multi-thread!")
        print("Tempo total estimado:" + str(0.001 * total_progress) + "m")

        for thread in range(threads_number):
            last_pos = size_per_thread*(thread+1)
            if thread+1 == threads_number:
                last_pos = None

            process = multiprocessing.Process(target=call_load_person, args=(person_id_list[size_per_thread*thread:last_pos], return_list))
            jobs.append(process)
            process.start()

        for proc in jobs:
            proc.join()

        full_person_list = list(return_list)
    else:
        print("Modo single-thread!")
        print("Tempo total estimado:" + str(0.01 * total_progress) + "m")
        full_person_list = call_load_person_single_thread(person_id_list, size_person_id_list)

    return full_person_list


def pessoa():
    config_tmbd()
    global total_progress
    df = load_csv("PessoaFilme", "id_pessoa_TMDB")
    person_id_list_raw = df.index.to_list()
    person_id_list = list(set(person_id_list_raw))      # remove referencias duplicadas de uma mesma pessoa em diversos filmes
    total_progress = len(person_id_list)
    print("Serao processadas " + str(total_progress) + " pessoas!")

    person_list = person_loader(person_id_list)

    person = pd.DataFrame(person_list, columns=['id_TMDB', 'id_IMDB', 'nome', 'nacionalidade', 'num_oscars'])
    print(person)
    write_csv(person, 'Pessoa', indice=False)

