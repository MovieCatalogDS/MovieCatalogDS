# Lab08 - Modelo Lógico e Análise de Dados em Grafos

# Equipe MovieCatalogDS - MCDS
* Maicon Gabriel de Oliveira - 221329
* Mylena Roberta dos Santos - 222687
* Jhonatan Cléto - 256444

## Modelo Lógico Combinado do Banco de Dados de Grafos

![Modelo Lógico de Grafos](images/modelo-logico-grafos.png)

## Perguntas de Pesquisa/Análise Combinadas e Respectivas Análises

### Pergunta/Análise 1

* Quais são os filmes mais relevantes de acordo com a premiação mais importante da indústria cinematográfica?
    * Para responder esta questão utilizaremos uma análise de centralidade, na qual iremos aumentar a relevância do filme (PageRank) a partir do número de Oscars recebidos pelas pessoas que participaram dele aliado ao número de Oscars que o próprio filme recebeu.
    * Possíveis dados a serem utilizados:
        * Número de premiações recebidas por cada pessoa;
        * Número de premiações recebidas por cada filme.

### Pergunta/Análise 2

* Quais são os universos cinematográficos mais rentáveis?
    * Para responder esta pergunta utilizaremos uma análise de comunidade/modularidadade, na qual cada universo representa uma comunidade de filmes e, a partir de cada uma delas, iremos definir as mais rentáveis pela soma total dos lucros (receita - orçamento) dos filmes integrantes.
    * Possíveis dados a serem utilizados:
        * Orçamento de cada um dos filmes;
        * Receita de cada um dos filmes.

### Pergunta/Análise 3

* Quais são as plataformas de streaming com o melhor custo-benefício relativo à qualidade dos seus filmes?
    * Para responder esta pergunta desenvolveremos um sistema de pontuação para as plataformas de streaming, utilizando as avaliações dos filmes que cada uma possui e então classificaremos as plataformas de acordo com as maiores pontuações. A análise utilizada mesclaria conceitos de comunidade/modularidade e de centralidade para, respectivamente, identificar filmes em um determinado intervalo de avaliações e aumentar a relevância das plataformas de streaming.
    * Possíveis dados a serem utilizados:
        * Preço da assinatura mais completa das plataformas;
        * Número de filmes disponíveis nas plataformas;
        * Avaliações dos filmes pela crítica especializada.