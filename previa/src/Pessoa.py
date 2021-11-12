import pandas as pd
from tmdbv3api import TMDb
from tmdbv3api import Person
import imdb
import time


''' 
    
    Esse cod depende do arquivo "PessoaFilme.csv"
    Arquivos necessarios devem estar dentro da pasta "data"
    Obs. Execução lenta
    #ra221329
    
'''


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


def get_awards_number(imdb_person_id, imdb_obj):
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
            return get_awards_number(imdb_person_id, imdb_obj)
        except Exception as error:
            print(error)
        finally:
            return awards_amount
    return awards_amount


def load_person(person_id, person_obj, imdb_obj):
    person_data = person_obj.details(person_id)     # aqui demora! (proporcinal ao numero de linhas em PessoaFilme.csv)

    imdb_person_id = person_data['imdb_id']
    number_of_awards = get_awards_number(imdb_person_id, imdb_obj)

    return (person_id, imdb_person_id, person_data['name'], person_data['place_of_birth'], number_of_awards)


def pessoa():
    df = load_csv("data/PessoaFilme", "id_pessoa_TMDB")
    person_id_list_raw = df.index.to_list()
    person_id_list = list(set(person_id_list_raw))      # remove elementos duplicados da lista
    person_obj = Person()
    imdb_obj = imdb.IMDb()
    person_list = []
    person_array_size = str(len(person_id_list))
    counter = 0

    for person_id in person_id_list:
        counter += 1
        print(str(counter) + "/" + person_array_size)
        person_list.append(load_person(person_id, person_obj, imdb_obj))

    return pd.DataFrame(person_list, columns=['id_TMDB', 'id_IMDB', 'nome', 'nacionalidade', 'num_oscars'])


person = pessoa()
print(person)
write_csv(person, 'Pessoa', indice=False)
