# Modelo de Apresentação da Final

# Estrutura de Arquivos e Pastas

A estrutura aqui apresentada é uma simplificação daquela proposta pelo [Cookiecutter Data Science](https://drivendata.github.io/cookiecutter-data-science/). Também será aceito que o projeto adote a estrutura completa do Cookiecutter Data Science e isso será considerado um diferencial. A estrutura geral é a seguinte e será detalhada a seguir:

~~~
├── README.md  <- arquivo apresentando a proposta
│
├── data
│   ├── external       <- dados de terceiros em formato usado para entrada na transformação
│   ├── interim        <- dados intermediários, e.g., resultado de transformação
│   ├── processed      <- dados finais usados para a publicação
│   └── raw            <- dados originais sem modificações
│
├── notebooks          <- Jupyter notebooks ou equivalentes
│
├── slides             <- arquivo de slides em formato PDF
│
├── src                <- fonte em linguagem de programação ou sistema (e.g., Orange, Cytoscape)
│   └── README.md      <- instruções básicas de instalação/execução
│
└── assets             <- mídias usadas no projeto
~~~

Na raiz deve haver um arquivo de nome `README.md` contendo a apresentação do projeto, como detalhado na seção seguinte.

## `data`

Arquivos de dados usados no projeto, quando isso ocorrer.

## `notebooks`

Testes ou prototipos relacionados ao projeto que tenham sido executados no Jupyter.

## `src`

Projeto na linguagem escolhida caso não seja usado o notebook, incluindo todos os arquivos de dados e bibliotecas necessários para a sua execução. Só coloque código Pyhton ou Java aqui se ele não rodar dentro do notebook.

 Acrescente na raiz um arquivo `README.md` com as instruções básicas de instalação e execução.

## `assets`

Qualquer mídia usada no seu projeto: vídeo, imagens, animações, slides etc. Coloque os arquivos aqui (mesmo que você mantenha uma cópia no diretório do código).

# Modelo para Apresentação da Entrega Prévia do Projeto

# Projeto Movie Catalog Dataset

# Equipe MovieCatalogDS - MCDS
* Maicon Gabriel de Oliveira - 221329
* Mylena Roberta dos Santos - 222687
* Jhonatan Cléto - 256444

## Resumo do Projeto

Filmes são uma das formas de entretenimento mais populares e lucrativas, logo não é por acaso que atualmente existem inúmeros serviços de streaming de vídeo tentando pegar a sua fatia em um mercado crescente. Com a grande quantidade de serviços, além da popularidade das franquias e universos cinematográficos, a escolha de quais filmes assistir ou por onde começar a acompanhar uma certa franquia de filmes tem se tornado uma tarefa difícil.

Mesmo que os serviços de streaming ofereçam features de recomendações de filmes baseadas nos gostos do usuário, elas são disponíveis apenas para os assinantes das plataformas e limitadas ao catálogo da plataforma.

Segundo o IMDB, a média de filmes produzidos por ano é de 2577. Empresas cinematográficas estão explorando maneiras de aumentar seu faturamento bruto de bilheteria. É difícil saber o que o público gosta antes de realmente ver suas críticas. Muitos fatores podem influenciar o gosto do público e a bilheteria bruta de um filme, como diretor, elenco, gênero e orçamento. Assim, encontrar as características que fazem um filme ter sucesso, pode ajudar as produtoras a ajustar seu planejamento, melhorando o lucro e diminuindo os riscos com a produção. 

Nesse contexto o Movie Catalog Dataset, objetiva-se a ser uma base de dados sobre a indústria cinematográfica, permitindo a construção de mecanismos de busca e análise a respeito de diversos aspectos relacionados aos cinema. Sendo que alguns deles são: gêneros, pessoas que participaram de filmes (diretores, roteiristas e atores) e os filmes por si só.


## Slides da Apresentação
> Coloque aqui o link para o PDF da apresentação final


## Modelo Conceitual

![Modelo Conceitual](images/modelo-conceitual.png)


## Modelos Lógicos

Modelo Lógico Relacional

~~~
FILME(_id_TMDB_, id_IMDB, titulo, titulo_original, sinopse, duracao, ano, classificacao, situacao, idioma_original, orcamento, receita, num_oscars)
AVALIADOR(_id_, nome)
AVALIACAO(_id_avaliador_, _id_filme_TMDB_, nota)
  id_avaliador chave estrangeira -> AVALIADOR(id)
  id_filme_TMDB chave estrangeira -> FILME(id_TMDB)
FRANQUIA(_nome_)
FRANQUIAFILME(_nome_franquia_, _id_filme_TMDB_)
  nome_franquia chave estrangeira -> FRANQUIA(nome)
  id_filme_TMDB chave estrangeira -> FILME(id_TMDB)
GENERO(nome)
GENEROFILME(_nome_genero_, _id_filme_TMDB_)
  nome_genero chave estrangeira -> GENERO(nome)
  id_filme_TMDB chave estrangeira -> FILME(id_TMDB)
PESSOA(_id_TMDB_, id_IMDB, nome, nacionalidade, num_oscars)
PESSOAFILME(_id_pessoa_TMDB_, _id_filme_TMDB_, ator, diretor, roteirista)
  id_pessoa_TMDB chave estrangeira -> PESSOA(id_TMDB)
  id_filme_TMDB chave estrangeira -> FILME(id_TMDB)
SEQUENCIA(_id_filme_TMDB_, _id_filme_sequencia_TMDB_)
  id_filme_TMDB chave estrangeira -> FILME(id_TMDB)
  id_filme_sequencia_TMDB chave estrangeira -> FILME(id_TMDB)
STREAMING(_nome_)
STREAMINGFILME(_nome_streaming_, _id_filme_TMDB)
  nome_streaming chave estrangeira -> STREAMING(nome)
  id_filme_TMDB chave estrangeira -> FILME(id_TMDB)
~~~


Modelo Lógico de Grafos - Grafo de Propriedades

![Modelo Lógico de Grafos](images/modelo-logico-grafos.png)


## Dataset Publicado
> Elencar os arquivos/bases preliminares dos datasets serão publicados.

título do arquivo/base | link | breve descrição
----- | ----- | -----
Filme | [Filme](./data/processed/Filme.csv) | Tabela com dados de filmes.
Sequencia | [Sequencia](./data/processed/Sequencia.csv) | Relação de sequencia entre filmes.
Franquia | [Franquia](./data/processed/Franquia.csv) | Lista das franquias que contêm os filmes na tabela Filme.
FranquiaFilme | [FranquiaFilme](./data/processed/FranquiaFilme.csv) | Relaciona franquias com seus respectivos filmes.
Genero | [Genero](./data/processed/Genero.csv) | Lista de gêneros obtidos no TMDB.
GeneroFilme | [GeneroFilme](./data/processed/GeneroFilme.csv) | Cada linha na tabela relaciona um filme com um gênero que ele possui.
Pessoa | [Pessoa](./data/processed/Pessoa.csv) | Tabela com dados sobre Pessoas que participam da produção de filmes da tabela Filme.
PessoaFilme | [PessoaFilme](./data/processed/PessoaFilme.csv) | Relaciona pessoas e filmes indicando o tipo de participação da pessoa: Ator, Diretor ou Roterista.
Avaliador | [Avaliador](./data/processed/Avaliador.csv) | Lista com alguns portais de avaliação de filmes.
Avaliacao | [Avaliacao](./data/processed/Avaliacao.csv) | Armazena as avaliações de filmes na tabela Filmes obtida dos avaliadores na tabela Avaliador.
Streaming | [Streaming](./data/processed/Streaming.csv) | Lista de plataformas de streaming de filmes obtidas no TMDB.
StreamingFilme | [StreamingFilme](./data/processed/StreamingFilme.csv) | Cada linha da tabela relaciona um filme com uma plataforma na qual ele pode ser encontrado.

> Os arquivos finais do dataset publicado devem ser colocados na pasta `data`, em subpasta `processed`. Outros arquivos serão colocados em subpastas conforme seu papel (externo, interim, raw). A diferença entre externo e raw é que o raw é em formato não adaptado para uso. A pasta `raw` é opcional, pois pode ser substituída pelo link para a base original da seção anterior.
> Coloque arquivos que não estejam disponíveis online e sejam acessados pelo notebook. Relacionais (usualmente CSV), XML, JSON e CSV ou triplas para grafos.
> Este é o conjunto mínimo de informações que deve constar na disponibilização do Dataset, mas a equipe pode enriquecer esta seção.

## Bases de Dados
> Elencar as bases de dados fonte utilizadas no projeto.

título da base | link | breve descrição
----- | ----- | -----
TMDB | [TMDB](https://www.themoviedb.org/?language=pt-BR) |  Base de dados gratuita e de código aberto sobre Filmes e Séries de TV.
IMDB | [IMDB](https://www.imdb.com) |  Base de dados online de informação sobre cinema TV, música e games.
RT_db | [TODO](https://www.rottentomatoes.com/) |  Dataset com avaliações de filmes obtidas do Rotten Tomatoes.

## Detalhamento do Projeto
> Apresente aqui detalhes do processo de construção do dataset e análise. Nesta seção ou na seção de Perguntas podem aparecer destaques de código como indicado a seguir. Note que foi usada uma técnica de highlight de código, que envolve colocar o nome da linguagem na abertura de um trecho com `~~~`, tal como `~~~python`.
> Os destaques de código devem ser trechos pequenos de poucas linhas, que estejam diretamente ligados a alguma explicação. Não utilize trechos extensos de código. Se algum código funcionar online (tal como um Jupyter Notebook), aqui pode haver links. No caso do Jupyter, preferencialmente para o Binder abrindo diretamente o notebook em questão.

~~~python
df = pd.read_excel("/content/drive/My Drive/Colab Notebooks/dataset.xlsx");
sns.set(color_codes=True);
sns.distplot(df.Hemoglobin);
plt.show();
~~~

> Se usar Orange para alguma análise, você pode apresentar uma captura do workflow, como o exemplo a seguir e descrevê-lo:
![Workflow no Orange](images/orange-zombie-meals-prediction.png)

> Coloque um link para o arquivo do notebook, programas ou workflows que executam as operações que você apresentar.

> Aqui devem ser apresentadas as operações de construção do dataset:
* extração de dados de fontes não estruturadas como, por exemplo, páginas Web
* agregação de dados fragmentados obtidos a partir de API
* integração de dados de múltiplas fontes
* tratamento de dados
* transformação de dados para facilitar análise e pesquisa

> Se for notebook, ele estará dentro da pasta `notebook`. Se por alguma razão o código não for executável no Jupyter, coloque na pasta `src` (por exemplo, arquivos do Orange ou Cytoscape). Se as operações envolverem queries executadas atraves de uma interface de um SGBD não executável no Jupyter, como o Cypher, apresente na forma de markdown.

## Evolução do Projeto
> Relatório de evolução, descrevendo as evoluções na modelagem do projeto, dificuldades enfrentadas, mudanças de rumo, melhorias e lições aprendidas. Referências aos diagramas, modelos e recortes de mudanças são bem-vindos.
> Podem ser apresentados destaques na evolução dos modelos conceitual e lógico. O modelo inicial e intermediários (quando relevantes) e explicação de refinamentos, mudanças ou evolução do projeto que fundamentaram as decisões.
> Relatar o processo para se alcançar os resultados é tão importante quanto os resultados.

## Perguntas de Pesquisa/Análise Combinadas e Respectivas Análises

> Apresente os resultados da forma mais rica possível, com gráficos e tabelas. Mesmo que o seu código rode online em um notebook, copie para esta parte a figura estática. A referência a código e links para execução online pode ser feita aqui ou na seção de detalhamento do projeto (o que for mais pertinente).

> Liste aqui as perguntas de pesquisa/análise e respectivas análises. Nem todas as perguntas precisam de queries que as implementam. É possível haver perguntas em que a solução é apenas descrita para demonstrar o potencial da base. Abaixo são ilustradas três perguntas, mas pode ser um número maior a critério da equipe.
>
### Perguntas/Análise com Resposta Implementada

> As respostas às perguntas podem devem ser ilustradas da forma mais rica possível com tabelas resultantes, grafos ou gráficos que apresentam os resultados. Os resultados podem ser analisados e comentados. Veja um exemplo de figura ilustrando uma comunidade detectada no Cytoscape:

> ![Comunidade no Cytoscape](images/cytoscape-comunidade.png)

#### Pergunta/Análise 1

* Os filmes que mais fizeram sucesso com o público também são aqueles que mais fizeram sucesso com a crítica?
  
  * De modo a responder à esta pergunta, foi necessário analisarmos as receitas e as avaliações de todos os filmes obtidos. Conforme ilustrado pelo conjunto de queries SQL a seguir, calculamos a nota média de cada um dos filmes, tomando filmes julgados por todos os avaliadores considerados (TMDB, IMDb e Rotten Tomatoes), e depois geramos duas tabelas. A primeira tabela ordenada decrescentemente por receita e a segunda tabela ordenada decrescentemente por nota média. Os resultados mostraram que os filmes que mais fizeram sucesso com esses grupos, mais especificamente os 10 primeiros, são distintos entre si.

  ~~~SQL
  /* Relação entre sucesso com o público (receita)
   e sucesso com a crítica (nota média) dos filmes */

  DROP TABLE IF EXISTS FilmeReceitaNota;
  DROP TABLE IF EXISTS FilmeAvaliacao;

  CREATE VIEW FilmeAvaliacao AS
      SELECT A.id_filme, SUM(A.nota) nota_total, COUNT(A.id_filme) qtd_avaliacoes
          FROM Avaliacao A
          GROUP BY A.id_filme;

  CREATE VIEW FilmeReceitaNota AS
      SELECT A.id_filme, F.titulo, F.ano, F.receita, (A.nota_total / A.qtd_avaliacoes) nota_media
          FROM Filme F, FilmeAvaliacao A
          WHERE A.id_filme = F.id_TMDB
            AND qtd_avaliacoes > 2;

  -- Ordenação decrescente por receita
  SELECT titulo, receita, nota_media 
      FROM FilmeReceitaNota
      ORDER BY receita DESC LIMIT 10;

  -- Ordenação decrescente por nota média
  SELECT titulo, receita, nota_media
      FROM FilmeReceitaNota
      ORDER BY nota_media DESC LIMIT 10;
  ~~~

#### Pergunta/Análise 2
> * Pergunta 2
>   
>   * Explicação sucinta da análise que será feita e conjunto de queries que
>     responde à pergunta.

#### Pergunta/Análise 3
> * Pergunta 3
>   
>   * Explicação sucinta da análise que será feita e conjunto de queries que
>     responde à pergunta.

### Perguntas/Análise Propostas mas Não Implementadas

#### Pergunta/Análise 1

* Sabendo que uma pessoa X trabalhou com uma pessoa Y no filme A e com uma pessoa Z no fime B, qual é a probabilidade das pessoas Y e Z trabalharem juntas em um filme C?
  
  * Com base em nosso dataset, pode ser gerado um grafo homogêneo que relaciona pessoas (atores, diretores e roteiristas) através filmes em que elas trabalharam juntas. Realizando um análise de predição de link sobre esse grafo, é possível calcular a probabilidade de duas pessoas colaborarem em um novo filme. Sendo que tais pessoas trabalharam com uma pessoa em comum, mas nunca colaboraram juntas. A resposta dessa pergunta pode ser relevante para facilitar o processo de casting - seleção de atores, roteiristas, etc. - de um filme em pré-produção, por exemplo.


#### Pergunta/Análise 2

* Quais são as características de um filme que faz sucesso com o público?

> * Pergunta 2
>   
>   * Explicação em linhas gerais de como a base pode ser usada para responder esta pergunta e a sua relevância.

#### Pergunta/Análise 3

* Quem são as pessoas mais relevantes em cada gênero em uma determinada década?
  
  * Com base em nosso dataset, pode ser gerado um grafo homogêneo que relaciona pessoas (atores, diretores e roteiristas) através do gênero que classifica os filmes em que elas trabalharam juntas. Para delimitar a década de interesse, basta que o ano de lançamento de cada um dos filmes seja verificado na montagem do grafo. Fazendo recortes desse grafo que admitem somente pessoas que estão conectadas por um mesmo gênero, podemos aplicar uma análise de centralidade por PageRank para determinar as pessoas mais relevantes do gênero em questão. A resposta dessa pergunta pode ser relevante para o estudo da história da indústria cinematográfica, por exemplo.

> Coloque um link para o arquivo do notebook que executa o conjunto de queries. Ele estará dentro da pasta `notebook`. Se por alguma razão o código não for executável no Jupyter, coloque na pasta `src`. Se as queries forem executadas atraves de uma interface de um SGBD não executável no Jupyter, como o Cypher, apresente na forma de markdown.
