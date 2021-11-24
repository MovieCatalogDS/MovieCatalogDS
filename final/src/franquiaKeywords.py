import requests
import json
import pandas as pd
import csv
from multiprocessing import Process

from concat_tables import concatenar

def get_key():
  with open('key.json', 'r') as f:
    key = f.read()
    key = json.loads(key)
    key = key['key']
    return key

def check_result(response):
    if ('total_results' in response.keys() 
    and response['total_results'] > 0): 
        return True

    return False 

def tmdb_search(api_key:str, search_type:str, query:str):
    template = 'https://api.themoviedb.org/3/search/{}?api_key={}&query={}&page={}'
    query = query.replace(' ', '%20')
    page = 1
    url = template.format(search_type, api_key, query, page)
    response = requests.get(url).json()

    if not check_result(response): 
        return None

    return response['results'][0]['id']

def tmdb_keyword_search(api_key:str, keyword_id:int):
    template = 'https://api.themoviedb.org/3/keyword/{}/movies?api_key={}&language=en-US&include_adult=false&page={}'

    url = template.format(keyword_id, api_key, 1)
    response = requests.get(url).json()

    if not check_result(response): 
        return []

    search_ids = list()
    for result in response['results']:
        search_ids.append(result['id'])

    num_pages = response['total_pages']
    for pg in range(2, num_pages+1):
        url = template.format(keyword_id, api_key, pg)
        response = requests.get(url).json()
        for result in response['results']:
            search_ids.append(result['id'])        

    return search_ids

def build_row(m_id:int, universe:str):
    return {
        'nome_franquia': universe,
        'id_filme_TMDB': m_id
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

def ff_job(api_key, universe, m_ids, pr):
    rows = list()
    keyword_id = tmdb_search(api_key,'keyword', universe)
    kwm_ids = tmdb_keyword_search(api_key, keyword_id)
    for id in kwm_ids:
        if id in m_ids:
            rows.append(build_row(id, universe))

    build_franchise_csv(pr, rows)

def cpmt_franchise_table():
    films = pd.read_csv('../data/processed/Filme.csv')
    m_ids = list(films['id_TMDB'])
    api_key = get_key()
    universes = [
        'Marvel Cinematic Universe',
        'DC Extended Universe',
        'MonsterVerse',
        'Middle-earth'
    ]

    pr_list = list()

    for i in range(len(universes)):
        universe = universes[i]
        pr = Process(target=ff_job, args=(api_key, universe, m_ids, i+1))
        pr_list.append(pr)
        pr.start()

    for pr in pr_list:
        pr.join()

    concatenar(('FranquiaFilme', len(pr_list)+1))

if __name__ == "__Main__":
    cpmt_franchise_table()