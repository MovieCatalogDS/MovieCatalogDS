# Queries no Dataset

## Pergunta/Análise 2

### Como os gêneros dos filmes se relacionam em uma determinada década?

~~~cypher
// Criação dos nós de filmes

LOAD CSV WITH HEADERS FROM 'http://localhost:11001/project-fac27eda-1e01-4fb3-828e-3f97433df316/Filme.csv' as line
CREATE (:Filme {id: line.id_TMDB, titulo: line.titulo,
         tituloOriginal: line.titulo_original, duracao: line.duracao,
         num_oscars: line.num_oscars, ano: line.ano,
         orcamento: line.orcamento, receita: line.receita,
         classificacao: line.classificacao, situacao: line.situacao})

CREATE INDEX FOR (f:Filme) on (f.id)


// Criação dos nós de gêneros

LOAD CSV WITH HEADERS FROM 'http://localhost:11001/project-fac27eda-1e01-4fb3-828e-3f97433df316/Genero.csv' AS line
CREATE (:Genero {nome:line.nome})


// Construção da relação entre gêneros e filmes

LOAD CSV WITH HEADERS FROM 'http://localhost:11001/project-fac27eda-1e01-4fb3-828e-3f97433df316/GeneroFilme.csv' AS line
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

MATCH (g1:Genero)<-[e:Cogen_2000]->(g2:Genero) RETURN g1.nome AS source, g2.nome AS target, e.num_filmes as weight
~~~

## Pergunta/Análise 3

### Quais são as comunidades de pessoas que podem ser mapeadas? E quais são as pessoas mais relevantes dentre elas?

~~~cypher
// Criação dos nós de filmes

LOAD CSV WITH HEADERS FROM 'http://localhost:11001/project-fac27eda-1e01-4fb3-828e-3f97433df316/Filme.csv' as line
CREATE (:Filme {id: line.id_TMDB, titulo: line.titulo,
         tituloOriginal: line.titulo_original, duracao: line.duracao,
         num_oscars: line.num_oscars, ano: line.ano,
         orcamento: line.orcamento, receita: line.receita,
         classificacao: line.classificacao, situacao: line.situacao})

CREATE INDEX FOR (f:Filme) on (f.id)


// Criação dos nós de pessoas

LOAD CSV WITH HEADERS FROM 'http://localhost:11001/project-3f1aab97-b531-4572-9d14-e92d174db195/Pessoa.csv' as line
CREATE (:Pessoa {id: line.id_TMDB, nome: line.nome,
         nacionalidade: line.nacionalidade, 
         num_oscars: line.num_oscars})


// Construção da relação entre pessoas e filmes

LOAD CSV WITH HEADERS FROM 'http://localhost:11001/project-3f1aab97-b531-4572-9d14-e92d174db195/PessoaFilme.csv' AS line
MATCH (f:Filme {id: line.id_filme_TMDB})
MATCH (p:Pessoa {id: line.id_pessoa_TMDB})
CREATE (p)-[:Participa {ator:line.ator, diretor:line.diretor, roteirista:line.roteirista}]->(f)


// Construção do grafo homogêneo de pessoas ligadas por filmes com pesos

MATCH (p1:Pessoa)-[a]->(f:Filme)<-[b]-(p2:Pessoa)
WHERE p1.id <> p2.id
MERGE (p1)<-[r:Coparticipa]->(p2)
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

MATCH (p1:Pessoa)-[e:Coparticipa]->(p2:Pessoa)
WHERE e.num_filmes/2 >= 5
RETURN DISTINCT p1.nome AS nome, p1.pagerank AS pagerank

MATCH (p1:Pessoa)<-[e:Coparticipa]->(p2:Pessoa)
WHERE e.num_filmes/2 >= 5
RETURN DISTINCT p1.nome AS nome, p1.pagerank AS pagerank
ORDER BY nome

CALL gds.pageRank.stream({
nodeQuery:'MATCH (p:Pessoa) RETURN id(p) as id',
relationshipQuery:'MATCH (p1:Pessoa)-[r:Coparticipa]->(p2:Pessoa)
WHERE r.num_filmes/2 >= 5
RETURN id(p1) as source, id(p2) as target,r.num_filmes/2 as weight',
relationshipWeightProperty: 'weight'
})
YIELD nodeId,score
return gds.util.asNode(nodeId).nome AS nome, score AS pagerank
ORDER BY pagerank DESC
LIMIT 10000

// Definição das comunidades

~~~