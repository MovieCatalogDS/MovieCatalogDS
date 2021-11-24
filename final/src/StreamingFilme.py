import pandas as pd
import requests
import json


''' 

    Essa func depende do arquivo "filme.csv" e precisa de uma pasta "temp" para armazenar arquivos intermediarios
    Saida "Streaming.csv" e "StreamingFilme.csv"
    Arquivos necessarios devem estar dentro de load_path
    #ra221329

'''

#load_path = "../data/tmp_data/"        #path de testes
load_path = "../data/processed/"      #path definitivo do github
save_path = load_path

# chave da api do tmdb
with open('key.json', 'r') as f:
    api_key = f.read()
    api_key = json.loads(api_key)['key']


def load_csv(file_name="", index_col="id_TMDB"):
    ''' Lê uma tabela gerada previamente e retorna um dataframe para manipulação '''
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


def providers_json_to_list(json, movie_id):
    providers_tuples = []

    try:
        for i in json['results']['US']['rent']:
            providers_tuples.append((i['provider_name'], movie_id))

    except KeyError:
        print("Sem dados! Id do filme que nao foi: " + str(movie_id))

    finally:
        return providers_tuples


def save_json(data, name):
    content = data.content
    with open(save_path + '/temp/' + str(name) + '.json', 'wb') as f:
        f.write(content)


def get_movie_providers(movie_id):
    try:
        with open(load_path + '/temp/' + str(movie_id) + '.json', 'r') as movie_providers:
            data = movie_providers.read()
            print("Arquivo " + str(movie_id) + " encontrado! Carregando a partir dele!")
            providers_json = json.loads(data)
    except FileNotFoundError:
        print("Gerando arquivo " + str(movie_id) + " arquivo ...")
        data = requests.get('https://api.themoviedb.org/3/movie/' + str(
            movie_id) + '/watch/providers?api_key=' + api_key)
        save_json(data, movie_id)
        providers_json = data.json()

    return providers_json_to_list(providers_json, movie_id)


def get_all_providers():
    data = requests.get('https://api.themoviedb.org/3/watch/providers/movie?api_key=' + api_key)
    providers_json = data.json()

    providers_tuples = []

    for element in providers_json['results']:
        providers_tuples.append(element['provider_name'])

    cleaned_providers_tuples = list(set(providers_tuples))

    return pd.DataFrame(cleaned_providers_tuples, columns=['nome'])


def generate_providers_movies_table(movies_id):
    streaming_filme = []

    for id_movie in movies_id:
        streaming_filme += get_movie_providers(id_movie)

    return pd.DataFrame(streaming_filme, columns=['nome_streaming', 'id_filme_TMDB'])


def run_streaming_filme():
    df = load_csv("Filme")
    movies_index_list = df.index.to_list()
    streaming_filme = generate_providers_movies_table(movies_index_list)
    write_csv(streaming_filme, 'StreamingFilme', indice=False)


def run_streaming():
    providers = get_all_providers()
    write_csv(providers, 'Streaming', indice=False)

if __name__ == "__main__":
    run_streaming_filme()
    run_streaming()
