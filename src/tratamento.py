import pandas as pd
import re
from pathlib import Path

PASTA_PROJETO = Path(__file__).resolve().parent.parent

ARQUIVO_ENTRADA = PASTA_PROJETO / "dados" / "dados_brutos.csv"
ARQUIVO_SAIDA = PASTA_PROJETO / "dados" / "dados_tratados.csv"


def tratar_dados():

    print("Iniciando o tratamento dos dados...")

    if not ARQUIVO_ENTRADA.exists():
        print("Arquivo dados_brutos.csv não encontrado!")
        return None

    df = pd.read_csv(ARQUIVO_ENTRADA)

    print(f"\nRegistros originais: {len(df)}")

    colunas_texto = [
        "titulo",
        "disponibilidade",
        "categoria",
        "url"
    ]

    for coluna in colunas_texto:
        df[coluna] = df[coluna].astype("string").str.strip()

    df["preco"] = pd.to_numeric(
        df["preco"],
        errors="coerce"
    )

    df["avaliacao"] = pd.to_numeric(
        df["avaliacao"],
        errors="coerce"
    )

    def extrair_quantidade(texto):

        if pd.isna(texto):
            return pd.NA

        resultado = re.search(
            r"\((\d+)\s+available\)",
            str(texto)
        )

        if resultado:
            return int(resultado.group(1))

        return pd.NA

    df["quantidade_estoque"] = (
        df["disponibilidade"].apply(extrair_quantidade)
        .astype("Int64")
    )

    df["em_estoque"] = (
        df["disponibilidade"]
        .str.contains("In stock", case=False, na=False)
    )

    df = df.dropna(
        subset=["titulo", "preco", "avaliacao", "categoria", "url"]
    )

    df = df[df["preco"] >= 0]

    df = df[df["avaliacao"].between(1, 5)]

    df = df.drop_duplicates(subset=["url"])

    df["avaliacao"] = df["avaliacao"].astype(int)

    df = df[
        [
            "titulo",
            "preco",
            "avaliacao",
            "disponibilidade",
            "quantidade_estoque",
            "em_estoque",
            "categoria",
            "url"
        ]
    ]

    df.to_csv(
        ARQUIVO_SAIDA,
        index=False,
        encoding="utf-8-sig"
    )

    print("\n===== RESULTADO DO TRATAMENTO =====")

    print(f"Registros finais: {len(df)}")

    print("\nValores ausentes por coluna:")
    print(df.isna().sum())

    print("\nRegistros duplicados:")
    print(df.duplicated(subset=["url"]).sum())

    print("\nEstatísticas dos preços:")
    print(df["preco"].describe())

    print(f"\nArquivo salvo em: {ARQUIVO_SAIDA}")

    return df


if __name__ == "__main__":

    dados_tratados = tratar_dados()

    if dados_tratados is not None:
        print("\nPrimeiros registros tratados:")
        print(dados_tratados.head().to_string(index=False))
