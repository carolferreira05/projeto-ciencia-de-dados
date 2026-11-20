import requests

url = "https://books.toscrape.com/"

resposta = requests.get(url, timeout=20)

print("Status da conexão:", resposta.status_code)

if resposta.status_code == 200:
    print("Conexão realizada com sucesso!")
    print("Tamanho do conteúdo:", len(resposta.text))
else:
    print("Não foi possível acessar o site.")
