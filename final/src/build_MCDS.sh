#!/bin/bash
echo "Iniciando a construção do Movie Catalog Dataset"
echo "Essa operação pode demorar dependendo do número de filmes requeridos"
echo "Os dados são armazenados no Diretório data/processed"
num_pages=$1
order_by=$2

python main.py $num_pages $order_by

# Remover os arquivos temporários
rm ../data/processed/*_*.csv