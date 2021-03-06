import sys
from multiprocessing import Process, cpu_count
from time import sleep

import filmes
import filmes_imdb
from franquiafilme import build_franchise_table
from concat_tables import concatenar
from generofilme import gerar_tabela_genero
from Pessoa import pessoa
from PessoaFilme import pessoa_filme
from Avaliacao import avaliacao
from StreamingFilme import run_streaming_filme, run_streaming

def movie_job(num_pages:int, order_by:str, tb_name:str, start_page:int, p_num):
    filmes.gerar_tabala_filmes(num_pages, order_by, tb_name, start_page, p_num)
    sleep(0.0001)
    filmes_imdb.get_more_movie_infos(tb_name, p_num)

def person_job():
    pessoa_filme()
    pessoa()

def streming_job():
    run_streaming_filme()
    run_streaming()

def main(args):
    num_pages, order_by  = args
    num_pages = int(num_pages)
    table_name = 'Filme' # Nome da tabela de filmes
    num_pss = cpu_count() # Número de Treads do CPU
    print("Gerando tabelas relacionadas a filmes!")
    # páginas por processador = ceil(num_pages/num_pss)
    ppp = num_pages//num_pss + 1
    pr_array = list()

    for i in range(num_pss):
        t_name = f'../data/processed/{table_name}_{i}.csv'
        s_page = ppp*i + 1
        pr = Process(target=movie_job, args=(ppp, order_by, t_name, s_page, i))
        pr_array.append(pr)
        pr.start()
        print(f"ID do processo p{i}: {pr.pid}") 

    for i in range(len(pr_array)):
        pr_array[i].join()

    concatenar((table_name, num_pss))

    # Construir tabelas de franquias, sequencias e generos em Paralelo
    p1 = Process(target=build_franchise_table)
    p2 = Process(target=gerar_tabela_genero)
    p1.start()
    p2.start()
    p1.join()
    p2.join()

    print("Gerando tabelas relacionadas a Pessoas, Avaliações e Streaming!")
    # Construção das Tabelas relacionadas a Pessoas, Avaliações e Streaming
    p1 = Process(target=person_job)
    p2 = Process(target=avaliacao)
    p3 = Process(target=streming_job)
    p1.start()
    p2.start()
    p3.start()
    p1.join()
    p2.join()
    p3.join()


params = sys.argv[1:]
main(params)