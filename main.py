import os
import sys
from pathlib import Path

PASTA_PROJETO = Path(__file__).resolve().parent

sys.path.insert(0, str(PASTA_PROJETO / "src"))

os.chdir(PASTA_PROJETO)

# Importa as funções dos outros arquivos
from scraping import coletar_dados_livros
from tratamento import tratar_dados
from algoritmo import aplicar_kmeans
from analise import analisar_dados

def executar_projeto():

    print("=" * 50)
    print("PROJETO DE MINERAÇÃO WEB")
    print("ANÁLISE DE PREÇOS DE LIVROS")
    print("=" * 50)

    print("\n[1/4] COLETA DOS DADOS")

    dados_brutos = coletar_dados_livros(
        max_livros=50,
        max_paginas=3
    )

    if not dados_brutos:
        print("Não foi possível coletar os dados.")
        return

    print("\n[2/4] TRATAMENTO DOS DADOS")

    dados_tratados = tratar_dados()

    if dados_tratados is None or dados_tratados.empty:
        print("Não foi possível tratar os dados.")
        return

    print("\n[3/4] APLICAÇÃO DO K-MEANS")

    dados_classificados = aplicar_kmeans()

    if dados_classificados is None:
        print("Não foi possível aplicar o K-Means.")
        return

    print("\n[4/4] ANÁLISE DOS RESULTADOS")

    analisar_dados()

    print("\n" + "=" * 50)
    print("PROJETO EXECUTADO COM SUCESSO!")
    print("=" * 50)


if __name__ == "__main__":
    executar_projeto()
