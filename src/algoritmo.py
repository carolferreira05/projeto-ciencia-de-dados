
import pandas as pd
from pathlib import Path

from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler

PASTA_PROJETO = Path(__file__).resolve().parent.parent

ARQUIVO_ENTRADA = PASTA_PROJETO / "dados" / "dados_tratados.csv"
ARQUIVO_SAIDA = PASTA_PROJETO / "dados" / "dados_com_grupos.csv"


def aplicar_kmeans():

    print("Iniciando a aplicação do K-Means...")

    if not ARQUIVO_ENTRADA.exists():
        print("Arquivo dados_tratados.csv não encontrado!")
        return None

    df = pd.read_csv(ARQUIVO_ENTRADA)

    print(f"\nLivros carregados: {len(df)}")

    X = df[["preco"]]

    scaler = StandardScaler()
    X_padronizado = scaler.fit_transform(X)

    modelo = KMeans(
        n_clusters=3,
        random_state=42,
        n_init=10
    )

    df["grupo"] = modelo.fit_predict(X_padronizado)

    resultado = df.groupby("grupo")["preco"].agg(
        ["count", "min", "mean", "max"]
    )

    print("\n===== RESULTADO DO K-MEANS =====")
    print(resultado.round(2))

    df.to_csv(
        ARQUIVO_SAIDA,
        index=False,
        encoding="utf-8-sig"
    )

    print(f"\nArquivo salvo em: {ARQUIVO_SAIDA}")

    return df


if __name__ == "__main__":
    dados = aplicar_kmeans()

    if dados is not None:
        print("\nPrimeiros livros classificados:")
        print(
            dados[["titulo", "preco", "grupo"]]
            .head(10)
            .to_string(index=False)
        )