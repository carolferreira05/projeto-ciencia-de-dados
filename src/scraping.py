import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import csv
import os
import time

from crawler import coletar_links_livros

avaliacoes = {
    "One": 1,
    "Two": 2,
    "Three": 3,
    "Four": 4,
    "Five": 5
}


def extrair_dados_livro(url, sessao):

    try:
        resposta = sessao.get(url, timeout=20)
        resposta.raise_for_status()

    except requests.RequestException as erro:
        print(f"Erro ao acessar {url}: {erro}")
        return None

    soup = BeautifulSoup(resposta.text, "html.parser")

    titulo = soup.select_one("div.product_main h1")
    titulo = titulo.get_text(strip=True) if titulo else None

    preco = soup.select_one("p.price_color")

    if preco:
        preco = preco.get_text(strip=True)
        preco = float(preco.replace("£", "").replace("Â", ""))
    else:
        preco = None

    avaliacao_elemento = soup.select_one(
        "p.star-rating"
    )

    avaliacao = None

    if avaliacao_elemento:
        classes = avaliacao_elemento.get("class", [])

        for classe in classes:
            if classe in avaliacoes:
                avaliacao = avaliacoes[classe]
                break

    disponibilidade = soup.select_one(
        "p.instock.availability"
    )

    if disponibilidade:
        disponibilidade = disponibilidade.get_text(
            strip=True
        )
    else:
        disponibilidade = None

    categorias = soup.select("ul.breadcrumb li a")

    if categorias:
        categoria = categorias[-1].get_text(strip=True)
    else:
        categoria = None

    return {
        "titulo": titulo,
        "preco": preco,
        "avaliacao": avaliacao,
        "disponibilidade": disponibilidade,
        "categoria": categoria,
        "url": url
    }


def coletar_dados_livros(max_livros=5, max_paginas=2):

    print("\nIniciando o processo de scraping...")

    links = coletar_links_livros(
        max_paginas=max_paginas
    )

    if max_livros is not None:
        links = links[:max_livros]

    dados_livros = []

    sessao = requests.Session()

    sessao.headers.update({
        "User-Agent": "Mozilla/5.0"
    })

    for indice, link in enumerate(links, start=1):

        print(
            f"Extraindo livro {indice} de {len(links)}"
        )

        dados = extrair_dados_livro(link, sessao)

        if dados:
            dados_livros.append(dados)

        time.sleep(1)

    sessao.close()

    os.makedirs("dados", exist_ok=True)

    caminho_arquivo = os.path.join(
        "dados",
        "dados_brutos.csv"
    )

    colunas = [
        "titulo",
        "preco",
        "avaliacao",
        "disponibilidade",
        "categoria",
        "url"
    ]

    with open(
        caminho_arquivo,
        "w",
        newline="",
        encoding="utf-8-sig"
    ) as arquivo:

        escritor = csv.DictWriter(
            arquivo,
            fieldnames=colunas
        )

        escritor.writeheader()
        escritor.writerows(dados_livros)

    print("\n===== RESULTADO DO SCRAPING =====")
    print(f"Livros processados: {len(dados_livros)}")
    print(f"Arquivo salvo em: {caminho_arquivo}")

    return dados_livros


if __name__ == "__main__":

    dados = coletar_dados_livros(
        max_livros=50,
        max_paginas=3
    )

    print("\nPrimeiros resultados:")

    for livro in dados[:3]:
        print(livro)
