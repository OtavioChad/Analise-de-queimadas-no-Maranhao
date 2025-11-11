# arquivo: grafico_queimadas.py
import pandas as pd
import matplotlib.pyplot as plt

def plot_queimadas(caminho_csv):
    """
    Lê um arquivo CSV do INPE com coluna de data (dia/mês/ano)
    e gera gráficos mensais e anuais das queimadas no Maranhão.
    Retorna: (fig_mensal, fig_anual, df_mensal)
    """

    # Lê o CSV
    df = pd.read_csv(caminho_csv)

    # Normaliza colunas
    df.columns = [c.strip().capitalize() for c in df.columns]

    # Detecta automaticamente a coluna de data
    col_data = next((c for c in df.columns if "data" in c.lower()), None)
    if col_data is None:
        raise ValueError("O CSV precisa conter uma coluna de data (ex: 'datahora').")

    # Converte para datetime
    df["Data"] = pd.to_datetime(df[col_data], errors="coerce")
    df = df.dropna(subset=["Data"])

    # Cria colunas de ano e mês
    df["Ano"] = df["Data"].dt.year
    df["Mes"] = df["Data"].dt.month

    # Agrupa por mês e ano (total mensal)
    df_mensal = df.groupby(["Ano", "Mes"], as_index=False).size()
    df_mensal.rename(columns={"size": "Quantidade"}, inplace=True)

    # Cria coluna de data representando o primeiro dia do mês
    df_mensal["DataMes"] = pd.to_datetime(df_mensal["Ano"].astype(str) + "-" + df_mensal["Mes"].astype(str).str.zfill(2) + "-01")

    # Agrupa também por ano (para o gráfico anual)
    df_anual = df_mensal.groupby("Ano", as_index=False)["Quantidade"].sum()

    # --- Gráfico 1: evolução mensal ---
    fig_mensal, ax1 = plt.subplots(figsize=(10, 5))
    ax1.plot(df_mensal["DataMes"], df_mensal["Quantidade"], marker="o", color="orange", linewidth=2)
    ax1.set_title("Evolução Mensal das Queimadas no Maranhão (Fonte: INPE/COIDS)", fontsize=14)
    ax1.set_xlabel("Mês/Ano", fontsize=12)
    ax1.set_ylabel("Número de Focos de Queimada", fontsize=12)
    ax1.grid(True, linestyle="--", alpha=0.6)
    fig_mensal.autofmt_xdate(rotation=45)
    fig_mensal.tight_layout()

    # --- Gráfico 2: total anual ---
    fig_anual, ax2 = plt.subplots(figsize=(8, 5))
    ax2.bar(df_anual["Ano"], df_anual["Quantidade"], color="orange")
    ax2.set_title("Totais de Focos de Queimada por Ano (Maranhão)", fontsize=14)
    ax2.set_xlabel("Ano", fontsize=12)
    ax2.set_ylabel("Número de Focos de Queimada", fontsize=12)
    ax2.grid(axis="y", linestyle="--", alpha=0.6)
    fig_anual.tight_layout()

    return fig_mensal, fig_anual, df_mensal
