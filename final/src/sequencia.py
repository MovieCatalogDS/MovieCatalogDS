from os import name
import pandas as pd
import csv

def build_sequels_csv(rows:list):
    fieldnames = ['id_filme_TMDB', 'id_filme_sequencia_TMDB']
    with open(f'../data/processed/Sequencia.csv', 'w', newline='') as seq_csv:
        writer = csv.DictWriter(seq_csv, fieldnames=fieldnames)
        writer.writeheader()
        size = len(rows)
        for i in range(size):
            if rows[i] != None:
                writer.writerow(rows[i])

def build_sequel_table():
    films = pd.read_csv('../data/processed/Filme.csv')
    ff = pd.read_csv('../data/processed/FranquiaFilme.csv')

    m_ids = list(films['id_TMDB'])
    m_years = list(films['ano'])
    ff_names = list(ff['nome_franquia'])
    ff_ids = list(ff['id_filme_TMDB'])

    ff_dict = dict()

    for i in range(len(m_ids)):
        try:
            index = ff_ids.index(m_ids[i])
            name = ff_names[index]
            if not name in ff_dict.keys():
                ff_dict[name] = []
            
            ff_dict[name].append({
                'id_filme_TMDB': m_ids[i],
                'ano': m_years[i]
            })
        except ValueError as e:
            continue
    
    sequels = list()

    for i in range(len(ff_ids)):
        ff_list = ff_dict[ff_names[i]]
        f_year = 0
        for mv in ff_list:
            if mv['id_filme_TMDB'] == ff_ids[i]:
                f_year = mv['ano']

        seq_id  = -1
        min_year = 2100
        year = 0
        for mv in ff_list:
            # Não considerar o mesmo filme
            if mv['id_filme_TMDB'] == ff_ids[i]:
                continue
            
            # Encontrar o filme com menor ano
            year = mv['ano']
            if f_year < year < min_year:
                min_year = year
                seq_id = mv['id_filme_TMDB']

        # Se o filme possui sequencia o adiciona na lista de sequencias
        if seq_id != -1:
            sequels.append({
                'id_filme_TMDB': ff_ids[i],
                'id_filme_sequencia_TMDB': seq_id
            })

    # criar a tabela de sequencias
    build_sequels_csv(sequels)

if __name__ == "__Main__":
    build_sequel_table()