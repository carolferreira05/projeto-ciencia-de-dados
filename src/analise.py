
import pandas as pd
import matplotlib.pyplot as plt

from pathlib import Path
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score

PASTA_PROJETO = Path(__file__).resolve().parent.parent

ARQUIVO_ENTRADA = PASTA_PROJETO / "dados" / "dados_com_grupos.csv"
PASTA_GRAFICOS = PASTA_PROJETO / "graficos"


def analisar_dados():

    print("Iniciando a análise dos resultados...")

    if not ARQUIVO_ENTRADA.exists():
        print("Arquivo dados_com_grupos.csv não encontrado!")
        return

    df = pd.read_csv(ARQUIVO_ENTRADA)

    PASTA_GRAFICOS.mkdir(parents=True, exist_ok=True)

    X = df[["preco"]]
    scaler = StandardScaler()
    X_padronizado = scaler.fit_transform(X)

    modelo = KMeans(
        n_clusters=3,
        random_state=42,
        n_init=10
    )

    modelo.fit(X_padronizado)

    silhouette = silhouette_score(
        X_padronizado,
        df["grupo"]
    )

    inercia = modelo.inertia_

    print("\n===== MÉTRICAS DO K-MEANS =====")
    print(f"Silhouette Score: {silhouette:.4f}")
    print(f"Inércia: {inercia:.4f}")

    print("\n===== RESUMO DOS GRUPOS =====")

    resumo = df.groupby("grupo")["preco"].agg(
        ["count", "min", "mean", "max"]
    )

    print(resumo.round(2))

    # GRÁFICO 1
    plt.figure(figsize=(9, 5))

    plt.hist(df["preco"], bins=10, edgecolor="black")

    plt.title("Distribuição dos preços dos livros")
    plt.xlabel("Preço (£)")
    plt.ylabel("Quantidade de livros")
    plt.tight_layout()

    plt.savefig(PASTA_GRAFICOS / "distribuicao_precos.png")
    plt.close()

    # GRÁFICO 2
    plt.figure(figsize=(10, 5))

    plt.scatter(
        range(len(df)),
        df["preco"],
        c=df["grupo"],
        cmap="viridis",
        s=60
    )

    plt.title("Agrupamento dos livros pelo K-Means")
    plt.xlabel("Índice do livro")
    plt.ylabel("Preço (£)")
    plt.colorbar(label="Grupo")
    plt.tight_layout()

    plt.savefig(PASTA_GRAFICOS / "grupos_precos.png")
    plt.close()

    # GRÁFICO 3
    plt.figure(figsize=(8, 5))

    quantidade = df["grupo"].value_counts().sort_index()

    quantidade.plot(kind="bar", edgecolor="black")

    plt.title("Quantidade de livros por grupo")
    plt.xlabel("Grupo")
    plt.ylabel("Quantidade de livros")
    plt.xticks(rotation=0)
    plt.tight_layout()

    plt.savefig(PASTA_GRAFICOS / "quantidade_grupos.png")
    plt.close()

    print("\n===== GRÁFICOS GERADOS =====")
    print(f"Arquivos salvos em: {PASTA_GRAFICOS}")


if __name__ == "__main__":
    analisar_dados()
