import pandas as pd
from tmdbv3api import TMDb
from tmdbv3api import Movie


''' 

    Esse cod depende do arquivo "Filme.csv"
    Arquivos necessarios devem estar dentro da pasta "data"
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


def load_person(movie_id, movie_instance):
    people = []
    movie = movie_instance.details(movie_id)

    for person in movie['casts']['cast']:
        people.append((person['id'], movie_id, True, False, False))

    for person in movie['casts']['crew']:
        if person['known_for_department'] == 'Directing':
            people.append((person['id'], movie_id, False, True, False))
        if person['known_for_department'] == 'Writing':
            people.append((person['id'], movie_id, False, False, True))
    
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
    previous_person_movie_table = load_csv("data/" + file_name, "id_pessoa_TMDB")
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
    df = load_csv("data/Filme")

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
    movie_instance = Movie()
    counter = 0
    items_amount = str(len(movies_id_list))

    for movie_id in movies_id_list:
        counter += 1
        print(str(counter) + "/" + items_amount)
        person_movie_table += load_person(movie_id, movie_instance)     # concatena as listas

    person_movie_table_raw = merge_person_movie_table(prev_person_movie_table, person_movie_table)

    return table_optimizer(person_movie_table_raw)


person_movie = pessoa_filme()
print(person_movie)
write_csv(person_movie, 'PessoaFilme')
