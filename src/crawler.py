
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import time


def coletar_links_livros(max_paginas=None):

    url_atual = "https://books.toscrape.com/index.html"

    links_livros = []
    paginas_visitadas = set()

    # Criando uma sessão para realizar as requisições
    sessao = requests.Session()

    sessao.headers.update({
        "User-Agent": "Mozilla/5.0"
    })

    numero_pagina = 0

    while url_atual:

        # Evita visitar a mesma página mais de uma vez
        if url_atual in paginas_visitadas:
            break

        paginas_visitadas.add(url_atual)
        numero_pagina += 1

        print(f"Acessando página {numero_pagina}: {url_atual}")

        try:
            resposta = sessao.get(url_atual, timeout=20)
            resposta.raise_for_status()

        except requests.RequestException as erro:
            print(f"Erro ao acessar a página: {erro}")
            break

        # Interpretando o conteúdo HTML
        soup = BeautifulSoup(resposta.text, "html.parser")

        # Encontrando todos os livros da página
        livros = soup.select("article.product_pod")

        for livro in livros:

            link = livro.select_one("h3 a")

            if link:
                url_livro = urljoin(url_atual, link["href"])
                links_livros.append(url_livro)

        print(f"Livros encontrados: {len(livros)}")

        # Verificando se existe uma próxima página
        proxima_pagina = soup.select_one("li.next a")

        if proxima_pagina:
            url_atual = urljoin(
                url_atual,
                proxima_pagina["href"]
            )
        else:
            url_atual = None

        # Limite opcional para testes
        if max_paginas and numero_pagina >= max_paginas:
            break

        # Pequena pausa entre as requisições
        time.sleep(1)

    sessao.close()

    # Removendo possíveis links duplicados
    links_livros = list(dict.fromkeys(links_livros))

    print("\n===== RESULTADO DO CRAWLER =====")
    print(f"Páginas visitadas: {numero_pagina}")
    print(f"Total de livros encontrados: {len(links_livros)}")

    return links_livros


if __name__ == "__main__":

    links = coletar_links_livros(max_paginas=2)

    print("\nPrimeiros links encontrados:")

    for link in links[:5]:
        print(link)
