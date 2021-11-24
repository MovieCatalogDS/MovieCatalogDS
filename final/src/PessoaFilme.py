import pandas as pd
from tmdbv3api import TMDb
from tmdbv3api import Movie


''' 

    Esse cod depende do arquivo "Filme.csv" e chave da API do tmdb em "key.txt"
    Arquivos necessarios devem estar dentro de load_path
    #ra221329

'''

#load_path = "../data/tmp_data/"        #path de testes
load_path = "../data/processed/"      #path definitivo do github
save_path = load_path

tmdb = TMDb()
movie_instance = Movie()

with open(load_path + 'key.txt') as f:
    tmdb.api_key = f.readline()


def load_csv(file_name="", index_col="id_TMDB"):
    try:
        file_name += '.csv'
        return pd.read_csv(file_name, index_col=index_col)

    except FileNotFoundError:
        print("Arquivo [" + file_name + "] nao encontrado!")


def write_csv(dataframe, name='out', indice=True):
    # Grava csv com nome dado ou out.csv por padrao
    filename = name + '.csv'
    dataframe.to_csv(save_path + filename, index=indice)
    print("Arquivo salvo com nome " + filename)


def print_person_debug(person):
    del person['adult']
    del person['gender']
    del person['original_name']
    del person['profile_path']
    del person['credit_id']
    if 'known_for_department' in person:
        del person['known_for_department']

    print(person)


def load_person(movie_id):
    people = []
    character_writers = []
    try:
        movie = movie_instance.details(movie_id)

        for person in movie['casts']['cast']:
            if "(uncredited)" not in person['character']:
                #print_person_debug(person)
                people.append((person['id'], movie_id, True, False, False))

        for person in movie['casts']['crew']:
            if person['job'] == 'Director':
                #print_person_debug(person)
                people.append((person['id'], movie_id, False, True, False))
            if person['department'] == 'Writing' and (person['job'] == 'Novel' or person['job'] == 'Story' or person['job'] == 'Comic Book' or person['job'] == 'Writer' or person['job'] == 'Series Composition'):# and (person['job'] == 'Novel' or person['job'] == 'Story' or person['job'] == 'Comic Book' or person['job'] == 'Writer' or person['job'] == 'Series Composition' or person['job'] == 'Characters'):       # person['department'] == 'Writing' person['department'] == 'Directing' person['job'] == 'Novel'
                #print_person_debug(person)
                people.append((person['id'], movie_id, False, False, True))
            elif person['department'] == 'Writing' and person['job'] == 'Characters':
                character_writers.append(person)

        if character_writers:
            ''' inclui o personagem (que participa do filme) de maior popularidade do 
                departamento de escritores como escritor, pois o tmdb tem varios escritores 
                marcados errados (como mangakas) '''
            guessed_writer = sorted(character_writers, key=lambda d: d['popularity'])
            people.append((guessed_writer[-1]['id'], movie_id, False, False, True))
            print("E como escritor de " + str(movie['original_title']) + ':\n' + str(guessed_writer[-1]['name']) + " eu escolho voce! OwO")

    except Exception as e:
        print(movie_id, e)
    finally:
        return people


def merge_entries(person_movie_list):
    for pos1 in range(len(person_movie_list)):
        for pos2 in range(pos1, len(person_movie_list)):
            if person_movie_list[pos1] and person_movie_list[pos2] and person_movie_list[pos1][0] == person_movie_list[pos2][0] and person_movie_list[pos1][1] == person_movie_list[pos2][1] and pos1 != pos2:
                actor = False
                director = False
                writer = False

                if person_movie_list[pos1][2] or person_movie_list[pos2][2]:
                    actor = True
                if person_movie_list[pos1][3] or person_movie_list[pos2][3]:
                    director = True
                if person_movie_list[pos1][4] or person_movie_list[pos2][4]:
                    writer = True

                person_movie_list[pos1] = (person_movie_list[pos1][0], person_movie_list[pos1][1], actor, director, writer)
                person_movie_list[pos2] = None

    return list(filter(None.__ne__, person_movie_list))


def table_optimizer(person_movie_table_raw):
    ''' Mescla entradas repetidas '''
    person_movie_table = person_movie_table_raw[:]
    person_movie_table.set_index('id_filme_TMDB', append=True, inplace=True)
    person_movie_table_raw.reset_index(inplace=True)
    repeated_entries = []

    duplicates = person_movie_table.index.duplicated(keep=False)

    person_movie_list = [tuple(x) for x in person_movie_table_raw.values]       # pandas tem bug onde drop nao funciona para multiindex com linhas repetidas
    person_movie_size = len(person_movie_list)-1

    for row in range(person_movie_size, -1, -1):
        if duplicates[row]:
            repeated_entries.append(person_movie_list.pop(row))

    person_movie_list += merge_entries(repeated_entries)

    return pd.DataFrame(person_movie_list, columns=['id_pessoa_TMDB', 'id_filme_TMDB', 'ator', 'diretor', 'roteirista']).set_index('id_pessoa_TMDB')


def get_previous_person_movie(file_name="PessoaFilme"):
    ''' Procura se ja existe "PessoaFilme.csv" e se existir retorna '''
    previous_person_movie_table = load_csv(load_path + file_name, "id_pessoa_TMDB")
    prev_movie_id_list = ''

    if previous_person_movie_table is not None and len(previous_person_movie_table.index):
        print("Arquivo " + file_name + ".csv encontrado!")
        print("O carregamento sera continuado a partir da ultima entrada!")

        prev_movie_id_list_raw = previous_person_movie_table["id_filme_TMDB"].to_list()
        prev_movie_id_list = list(set(prev_movie_id_list_raw))

    else:
        print("Gerando aquivo do zero!")

    return previous_person_movie_table, prev_movie_id_list


def load_data():
    ''' Carrega aquivos necessarios e anteriormente gerados(se houver)
        para otimizar a consulta dos dados '''
    df = load_csv(load_path + "Filme")

    movies_id_list_raw = df.index.to_list()     # gera lista de id_tmdb dos filmes
    prev_person_movie_table, prev_movie_id_list = get_previous_person_movie()       # carrega arquivo gerado anteriormente(se houver)
    movies_id_list = set(movies_id_list_raw) - set(prev_movie_id_list)

    return movies_id_list, prev_person_movie_table


def merge_person_movie_table(previous_person_movie, current):
    current_person_movie = pd.DataFrame(current, columns=['id_pessoa_TMDB', 'id_filme_TMDB', 'ator', 'diretor', 'roteirista']).set_index('id_pessoa_TMDB')

    if previous_person_movie is not None and len(previous_person_movie.index) and current_person_movie is not None and len(current_person_movie.index):
        return pd.concat([previous_person_movie, current_person_movie])
    elif previous_person_movie is not None and len(previous_person_movie.index):
        return previous_person_movie
    else:
        return current_person_movie


def pessoa_filme():
    movies_id_list, prev_person_movie_table = load_data()
    person_movie_table = []

    counter = 0
    items_amount = str(len(movies_id_list))

    for movie_id in movies_id_list:
        counter += 1
        print(str(counter) + "/" + items_amount)
        person_movie_table += load_person(movie_id)     # concatena as listas

    person_movie_table_raw = merge_person_movie_table(prev_person_movie_table, person_movie_table)

    return table_optimizer(person_movie_table_raw)


person_movie = pessoa_filme()
print(person_movie)
write_csv(person_movie, 'PessoaFilme')
