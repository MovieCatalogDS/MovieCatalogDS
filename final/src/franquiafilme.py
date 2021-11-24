from multiprocessing import Process, cpu_count
import tmdbv3api as tmdb
import pandas as pd
import csv
import json
from concat_tables import concatenar
from sequencia import build_sequel_table
from franquiaKeywords import cpmt_franchise_table

def config_tmdb():
    """# **Configuração da API do TMDB**"""

    # instânciar a configuração da api
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

movie_tools = tmdb.Movie()

def get_movie_collection(movie_id:int):
    global movie_tools
    movie = {}
    collection = None
    try:
        movie = movie_tools.details(movie_id)
        collection = movie['belongs_to_collection']
    except Exception as e:
        print(e)
        print(f"Erro ao obter informações sobre o filme com id: {movie_id}.\nContinuando sem ele.")

    if collection == None:
        return None

    pos = collection['name'].find('Collection')
    name_collection = collection['name'][:pos].strip()
    return {
        'nome_franquia': name_collection,
        'id_filme_TMDB': movie_id
    }

def build_franchise_csv(table_num, rows:list):
    fieldnames = ['nome_franquia', 'id_filme_TMDB']
    with open(f'../data/processed/FranquiaFilme_{table_num}.csv', 'w', newline='') as ff_csv:
        writer = csv.DictWriter(ff_csv, fieldnames=fieldnames)
        writer.writeheader()
        size = len(rows)
        for i in range(size):
            print(f'pr ({table_num}) - Filme #{i+1} - {(i+1)*100/size:.2f}% Concluído')
            if rows[i] != None:
                writer.writerow(rows[i])

def franchise_job(movie_ids, pr):
    rows = list(map(get_movie_collection, movie_ids))   
    build_franchise_csv(pr, rows)

def build_franchise_table():
    config_tmdb()
    films = pd.read_csv('../data/processed/Filme.csv')
    films_ids = list(films['id_TMDB'])
    
    # Número de Núcleos Lógicos do processador
    num_pp = cpu_count()

    # Quantidade de trabalho para cada Processo
    ipp = len(films_ids)//num_pp
    pr_array = list()

    # Dividir os indices dos filmes entre os Processos 
    start = 0
    for i in range(num_pp-1):
        stop = ipp*(i+1)
        ids_clip = list(films_ids[start: stop])
        start = stop
        # Criar e iniciar o processo
        pr = Process(target=franchise_job, args=(ids_clip, i))
        pr_array.append(pr)
        pr.start()
        print(f"ID do processo p{i}: {pr.pid}")

    # Iniciar o último processo (Pode possuir alguns ids a mais)
    ids_clip = list(films_ids[stop: ])
    pr =Process(target=franchise_job, args=(ids_clip, num_pp-1))
    pr_array.append(pr)
    pr.start()  

    # Esperar que todos os Processos terminem
    for i in range(len(pr_array)):
        pr_array[i].join()  

    # Unir a tabela de franquias
    concatenar(('FranquiaFilme', num_pp))

    # Montar a tabela de sequencias
    build_sequel_table()

    # Completar a tabela de franquias
    cpmt_franchise_table()

    # Gerar a tabela Franquia
    ff = pd.read_csv('../data/processed/FranquiaFilme.csv')
    franchises = ff.groupby('nome_franquia').count()
    frc_names = list(franchises.index)
    frc = pd.DataFrame(frc_names, columns=['nome'])
    frc.to_csv('../data/processed/Franquia.csv', encoding='utf-8', index=False)

if __name__ == "__Main__":
    build_franchise_table()