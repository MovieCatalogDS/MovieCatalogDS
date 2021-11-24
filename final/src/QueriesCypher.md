# Queries no Dataset

## Pergunta/Análise 2

### Como os gêneros dos filmes se relacionam em uma determinada década?

~~~cypher
// Criação dos nós de filmes

LOAD CSV WITH HEADERS FROM 'https://raw.githubusercontent.com/MovieCatalogDS/MovieCatalogDS/main/final/data/processed/Filme.csv' as line
CREATE (:Filme {id: line.id_TMDB, titulo: line.titulo,
         tituloOriginal: line.titulo_original, duracao: line.duracao,
         num_oscars: line.num_oscars, ano: line.ano,
         orcamento: line.orcamento, receita: line.receita,
         classificacao: line.classificacao, situacao: line.situacao})

CREATE INDEX FOR (f:Filme) on (f.id)


// Criação dos nós de gêneros

LOAD CSV WITH HEADERS FROM 'https://raw.githubusercontent.com/MovieCatalogDS/MovieCatalogDS/main/final/data/processed/Genero.csv' AS line
CREATE (:Genero {nome:line.nome})


// Construção da relação entre gêneros e filmes

LOAD CSV WITH HEADERS FROM 'https://raw.githubusercontent.com/MovieCatalogDS/MovieCatalogDS/main/final/data/processed/GeneroFilme.csv' AS line
MATCH (f:Filme {id: line.id_filme_TMDB})
MATCH (g:Genero {nome: line.nome_genero})
CREATE (f)-[:Pertence]->(g)


// Construção do grafo homogêneo de gêneros ligados por filmes com pesos

MATCH (g1:Genero)<-[a]-(f:Filme)-[b]->(g2:Genero)
WHERE 2000 < toInteger(f.ano) <= 2010 AND g1.nome <> g2.nome
MERGE (g1)<-[r:Cogen_2000]->(g2)
ON CREATE SET r.num_filmes = 1
ON MATCH SET r.num_filmes = r.num_filmes + 1


// Tabela dos cogêneros

MATCH (g1:Genero)<-[e:Cogen_2000]->(g2:Genero)
RETURN g1.nome AS source, g2.nome AS target, e.num_filmes as weight
~~~

## Pergunta/Análise 3

### Quais são as comunidades de pessoas que podem ser mapeadas? E quais são as pessoas mais relevantes dentre elas?

~~~cypher
// Criação dos nós de filmes

LOAD CSV WITH HEADERS FROM 'https://raw.githubusercontent.com/MovieCatalogDS/MovieCatalogDS/main/final/data/processed/Filme.csv' as line
CREATE (:Filme {id: line.id_TMDB, titulo: line.titulo,
         tituloOriginal: line.titulo_original, duracao: line.duracao,
         num_oscars: line.num_oscars, ano: line.ano,
         orcamento: line.orcamento, receita: line.receita,
         classificacao: line.classificacao, situacao: line.situacao})

CREATE INDEX FOR (f:Filme) on (f.id)


// Criação dos nós de pessoas

LOAD CSV WITH HEADERS FROM 'https://raw.githubusercontent.com/MovieCatalogDS/MovieCatalogDS/main/final/data/processed/Pessoa.csv' as line
CREATE (:Pessoa {id: line.id_TMDB, nome: line.nome,
         nacionalidade: line.nacionalidade, 
         num_oscars: line.num_oscars})


// Construção da relação entre pessoas e filmes

LOAD CSV WITH HEADERS FROM 'https://raw.githubusercontent.com/MovieCatalogDS/MovieCatalogDS/main/final/data/processed/PessoaFilme.csv' AS line
MATCH (f:Filme {id: line.id_filme_TMDB})
MATCH (p:Pessoa {id: line.id_pessoa_TMDB})
CREATE (p)-[:Participa {ator:line.ator, diretor:line.diretor, roteirista:line.roteirista}]->(f)


// Construção do grafo homogêneo de pessoas ligadas por filmes com pesos

MATCH (p1:Pessoa)-[a]->(f:Filme)<-[b]-(p2:Pessoa)
WHERE p1.id <> p2.id
MERGE (p1)-[r:Coparticipa]->(p2)
ON CREATE SET r.num_filmes = 1
ON MATCH SET  r.num_filmes = r.num_filmes + 1

// Cálculo dos scores do PageRank

CALL gds.graph.create(
  'prGraph',
  'Pessoa',
  'Coparticipa'
)

CALL gds.pageRank.stream('prGraph')
YIELD nodeId, score
MATCH (p:Pessoa {id: gds.util.asNode(nodeId).id})
SET p.pagerank = score

// Definição das comunidades

CALL gds.graph.create(
  'communityGraph',
  'Pessoa',
  {
    Coparticipa: {
      orientation: 'UNDIRECTED'
    }
  }
)

CALL gds.louvain.stream('communityGraph')
YIELD nodeId, communityId
MATCH (p:Pessoa {id: gds.util.asNode(nodeId).id})
SET p.comunidade = communityId

// Exportando os dados para utilizar no Cytoscape (CSV)
// Utilizamos um recorte de arestas com peso maior igual a 3

MATCH (p1:Pessoa)-[e:Coparticipa]->(p2:Pessoa)
WHERE e.num_filmes >= 3
RETURN p1.nome AS source, p2.nome AS target, e.num_filmes as weight
ORDER BY source

MATCH (p1:Pessoa)-[e:Coparticipa]->(p2:Pessoa)
WHERE e.num_filmes >= 3 
RETURN DISTINCT p1.nome AS nome, p1.pagerank AS pagerank, p1.comunidade as comunidade
ORDER BY nome

~~~