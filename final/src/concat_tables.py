import pandas as pd
import sys

def concatenar(args):
    table_name, num_tables = args
    num_tables = int(num_tables)
    tb_list = list()
    for i in range(num_tables):
        tb_name = f'../data/processed/{table_name}_{i}.csv'
        tb = pd.read_csv(tb_name)
        tb_list.append(tb)

    tb = pd.concat(tb_list, ignore_index=True)

    if table_name.find('Filme') == 0:
        tb = tb.fillna(0)
        tb = tb.astype({'receita': int, 
                        'duracao': int,
                        'orcamento': int,
                        'ano': int,
                        'num_oscars': int})

    tb.to_csv(f'../data/processed/{table_name}.csv', index=False, encoding='utf-8')

if __name__ == '__main__':
    args = sys.argv[1:]
    concatenar(args)