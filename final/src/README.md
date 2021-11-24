# Instruções para construir o Movie Catalog Dataset (MCDS)

Os scripts que constroem o Movie Catalog Dataset foram elaborados em Python. Portanto, certifique-se de ter o [Interpretador de Python](https://www.python.org/downloads/) instalado.

É necessária também uma [key para a API do TMDB](https://www.themoviedb.org/documentation/api), que deve ser adicionada no arquivo key.json, no campo indicado no exemplo abaixo.

~~~json
{
  "key": "Insira sua key do TMDB"
}
~~~

## Ambiente de execução

Recomendamos o uso de um ambiente virtual (venv) para a instalação das dependência de modo a evitar conflitos com os pacotes python instalados no seu computador. Para instalar e iniciar um venv use os seguintes comandos no terminal:

~~~bash
# Instalar o modulo venv
pip install venv

# Criar o ambiente virtual
python3 -m venv nome_do_venv

# Ativar o ambiente virtual (Linux)
source nome_do_venv/bin/activate
~~~

## Dependências

Para que os scripts funcionem corretamente é necessário instalar as dependencias do projeto definidas no arquivo `requirements.txt`. Para tal rode o seguinte comando no terminal:

~~~bash
pip install -r requirements.txt
~~~

## Execução do Script

Após instalar as dependencias do projeto, no ambiente virtual, ou no seu sistema, basta executar o script bash `build_MCDS.sh` ou o arquivo `main.py`, para iniciar a construção do dataset como nos exemplos abaixo.

~~~bash
# Tonar o script um executável (linux)
chmod +x build_MCDS.sh

# Iniciar a construção pelo script bash
./build_MCDS.sh num_paginas ordenar_por
~~~

~~~bash
# Iniciar a construção pelo main.py
python main.py num_paginas ordenar_por
~~~

Para executar os scripts são necessários os seguintes parâmetros:

**num_paginas:** Número de páginas de filmes a serem requeridas do TMDB, cada página costuma conter 20 filmes, assim o número de filmes no Dataset será aproximadamente `num_paginas*20`

**ordenar_por:** Define o modo de busca/ordenação dos filmes no TMDB.
* Alguns valores aceitos:
    * "revenue.desc" - pela receita - decrescente
    * "popularity.asc" - pela popularidade - crescente
    * "release_date.asc" - pela data de nacimento - crescente 
    * "original_title.desc" - pelo titulo original - decrescente
    * "vote_count.asc" - pela contagem de votos - crescente

* Para mais informações consulte a documentação da [API do TMDB](https://developers.themoviedb.org/3/discover/movie-discover) 

O processo de construção do Dataset depende da quantidade de filmes que seram incluidos.

Ao final do procedimento os dados estarão no no subdiretório [processed](../data/processed) do diretório **data**.