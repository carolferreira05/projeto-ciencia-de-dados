# Projeto de Mineração Web — Análise de Preços de Livros

## 1. Descrição do projeto

Este projeto tem como objetivo realizar a coleta, o tratamento e a análise de dados de livros disponíveis no site [Books to Scrape](https://books.toscrape.com/), utilizando técnicas de mineração web e aprendizado de máquina.

A partir dos dados coletados, foi aplicado o algoritmo K-Means para identificar agrupamentos de livros de acordo com seus preços, permitindo observar diferentes faixas de valores presentes na amostra.

## 2. Fonte dos dados

A fonte utilizada foi o Books to Scrape, um site de demonstração desenvolvido para atividades de web scraping. Foram coletados 50 livros.

As informações extraídas foram:

- Título do livro;
- Preço;
- Avaliação;
- Disponibilidade;
- Categoria;
- URL do livro.

## 3. Tecnologias e ferramentas utilizadas

- **Python:** linguagem de programação utilizada no desenvolvimento.
- **Requests:** realização de requisições HTTP.
- **BeautifulSoup:** extração de informações das páginas HTML.
- **Pandas:** organização, tratamento e análise dos dados.
- **Scikit-learn:** aplicação do algoritmo K-Means e cálculo de métricas.
- **Matplotlib:** criação dos gráficos.
- **Visual Studio Code:** ambiente de desenvolvimento.

## 4. Estrutura do projeto

```text
projeto-mineracao-web/
│
├── dados/
│   ├── dados_brutos.csv
│   ├── dados_tratados.csv
│   └── dados_com_grupos.csv
│
├── graficos/
│   ├── distribuicao_precos.png
│   ├── grupos_precos.png
│   └── quantidade_grupos.png
│
├── src/
│   ├── crawler.py
│   ├── scraping.py
│   ├── tratamento.py
│   ├── algoritmo.py
│   └── analise.py
│
├── main.py
├── requirements.txt
└── README.md
```

## 5. Etapas de desenvolvimento

### 5.1. Crawler e scraping

O crawler percorre as páginas do catálogo e identifica os links individuais dos livros.

Em seguida, o scraping acessa as páginas dos livros e extrai as informações selecionadas.

Foram percorridas três páginas do catálogo, que disponibilizaram 60 links. Entretanto, foram extraídos apenas os primeiros 50 livros, conforme o limite definido para o projeto.

Os dados originais foram armazenados em `dados_brutos.csv`.

### 5.2. Tratamento dos dados

O tratamento foi realizado com a biblioteca Pandas.

Foram executadas as seguintes operações:

- Padronização dos campos textuais;
- Conversão dos preços e avaliações para valores numéricos;
- Extração da quantidade disponível em estoque;
- Criação da coluna que identifica se o livro está em estoque;
- Remoção de registros incompletos;
- Verificação e remoção de duplicidades;
- Organização das colunas.

O resultado foi armazenado em `dados_tratados.csv`.

Ao final, os 50 registros foram preservados, sem valores ausentes ou duplicados.

### 5.3. Aplicação do K-Means

Foi utilizado o algoritmo K-Means, da biblioteca Scikit-learn, para agrupar os livros conforme seus preços.

A variável utilizada foi `preco`, previamente padronizada com `StandardScaler`.

Foram definidos três agrupamentos (`n_clusters=3`), com `random_state=42` e `n_init=10`.

O resultado foi armazenado em `dados_com_grupos.csv`.

### 5.4. Análise dos resultados

Após a aplicação do algoritmo, foram calculadas métricas para avaliar os agrupamentos e desenvolvidos gráficos para facilitar a interpretação dos resultados.

As métricas utilizadas foram:

- **Silhouette Score:** avalia a separação e a coesão dos agrupamentos.
- **Inércia:** mede a soma das distâncias quadráticas dos dados aos centros dos grupos.

Também foram gerados três gráficos: distribuição dos preços, agrupamento dos livros e quantidade de livros por grupo.

## 6. Resultados obtidos

O K-Means identificou três grupos entre os 50 livros analisados.

| Grupo | Quantidade | Preço mínimo | Preço médio | Preço máximo |
|---|---:|---:|---:|---:|
| 0 | 19 | £44,18 | £50,76 | £57,31 |
| 1 | 19 | £12,84 | £19,86 | £26,41 |
| 2 | 12 | £30,52 | £34,60 | £40,30 |

As métricas obtidas foram:

- Silhouette Score: **0,6769**.
- Inércia: **3,5162**.

Os resultados indicam uma separação relativamente boa entre os grupos encontrados.

Os agrupamentos representam diferentes faixas de preço, não necessariamente o tema, a qualidade ou a avaliação dos livros.

## 7. Conclusão

O projeto permitiu aplicar, na prática, as etapas de mineração web, desde a coleta de informações em páginas HTML até o tratamento e a análise dos dados.

A aplicação do K-Means possibilitou identificar três faixas de preço entre os 50 livros analisados, demonstrando como técnicas de aprendizado de máquina não supervisionado podem ser utilizadas para encontrar padrões em conjuntos de dados.

Os resultados indicaram uma separação relativamente boa entre os agrupamentos, conforme o Silhouette Score obtido.

Como limitações, destaca-se o tamanho reduzido da amostra, composta por apenas 50 livros de um site de demonstração. Além disso, o algoritmo considerou exclusivamente os preços, não permitindo estabelecer relações entre os valores, as avaliações e as categorias dos livros.

## 8. Como executar o projeto

### Pré-requisitos

- Python instalado;
- Visual Studio Code ou outro ambiente de desenvolvimento;
- Conexão com a internet para realizar a coleta.

### Instalação das dependências

No terminal, dentro da pasta do projeto, execute:

```bash
pip install -r requirements.txt
```

### Execução

Para executar todas as etapas do projeto, utilize:

```bash
python main.py
```

O arquivo principal executará automaticamente a coleta, o tratamento, a aplicação do K-Means e a geração das análises e dos gráficos.