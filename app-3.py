# app.py
import streamlit as st
import pandas as pd
import os
from algoritmos import bubble_sort, insertion_sort, merge_sort, quick_sort
from grafico_desempenho import plot_comparison
from download_data import download_and_extract_ma
from grafico_queimadas import plot_queimadas

# -------------------------------------------------
# CONFIGURAÇÃO INICIAL
# -------------------------------------------------
st.set_page_config(page_title="APS - Ordenação (MA)", layout="wide")
st.title("APS - Análise de Performance de Algoritmos (Maranhão)")
st.markdown(
    "Upload CSV opcional — se não houver, o app tentará baixar os dados oficiais do INPE para MA (2023 e 2024)."
)

# -------------------------------------------------
# DOWNLOAD OU UPLOAD DE DADOS
# -------------------------------------------------
if st.button("Baixar dados do INPE (MA 2023 & 2024)"):
    with st.spinner("Baixando e extraindo..."):
        download_and_extract_ma()
    st.success("Download concluído. Arquivos em /dados/")

uploaded = st.file_uploader("Ou envie um CSV manualmente (opcional)", type=["csv"])
if uploaded is not None:
    df = pd.read_csv(uploaded)
else:
    # tenta abrir o primeiro CSV em /dados/
    os.makedirs("dados", exist_ok=True)
    csvs = [f for f in os.listdir('dados') if f.lower().endswith('.csv') and 'focos_br_ma_ref' in f.lower()]
    if not csvs:
        st.warning("Nenhum CSV encontrado. Clique em 'Baixar dados' ou faça upload.")
        st.stop()
    df = pd.read_csv(os.path.join('dados', csvs[0]))


# -------------------------------------------------
# CONFIGURAÇÕES DE ORDENAÇÃO
# -------------------------------------------------
st.sidebar.header("Configurações")
campo = st.sidebar.selectbox("Campo para ordenar", options=list(df.columns), index=0)
alg = st.sidebar.selectbox("Algoritmo", ["bubble", "insertion", "merge", "quick"])
show_plot = st.sidebar.checkbox("Mostrar gráfico comparativo (tempo & comparações)", value=True)

st.subheader("Pré-visualização dos dados")
st.dataframe(df)


# -------------------------------------------------
# EXECUÇÃO DOS ALGORITMOS
# -------------------------------------------------
if st.button("Executar ordenações e comparar"):
    dados = df.to_dict(orient='records')
    results = {}

    for name, func in [
        ('bubble', bubble_sort),
        ('insertion', insertion_sort),
        ('merge', merge_sort),
        ('quick', quick_sort)
    ]:
        with st.spinner(f"Executando {name}..."):
            res = func(dados, campo)
            results[name] = res
            st.write(
                f"**{name}** — Tempo: {res.tempo:.6f}s | Comparações: {res.comparacoes} | Trocas: {res.trocas}"
            )

    st.success("Todas as ordenações concluídas.")
    # mostra a última lista ordenada (do último algoritmo executado)
    st.dataframe(pd.DataFrame(res.lista))

    if show_plot:
        # Gráfico de comparação dos algoritmos (retorna figura Plotly)
        fig = plot_comparison(results)
        st.plotly_chart(fig, use_container_width=True)


    # -------------------------------------------------
    # GRÁFICO DE QUEIMADAS (AGORA MENSAL)
    # -------------------------------------------------
    st.header("📊 Análise de Queimadas (INPE 2023–2024)")

    os.makedirs("dados", exist_ok=True)
    csvs = [f for f in os.listdir('dados') if f.lower().endswith('.csv') and ("2023" in f or "2024" in f)]

    if not csvs:
        st.warning("Nenhum CSV de queimadas encontrado. Clique em 'Baixar dados' ou faça upload.")
    else:
        try:
            # Junta todos os CSVs do INPE (2023 e 2024)
            lista_dfs = []
            for f in csvs:
                df_q = pd.read_csv(os.path.join("dados", f))
                lista_dfs.append(df_q)
            df_total = pd.concat(lista_dfs, ignore_index=True)

            # Salva um CSV consolidado (apenas para referência)
            df_total.to_csv("dados/dados_queimadas.csv", index=False)

            # Gera gráficos mensais e anuais
            fig_mes, fig_total, tabela = plot_queimadas("dados/dados_queimadas.csv")

            # --- Exibição no Streamlit ---
            st.subheader("🔥 Queimadas por Mês")
            st.pyplot(fig_mes)

            st.subheader("📋 Dados Consolidados por Mês (INPE)")
            st.dataframe(
                tabela.style.format({"Quantidade": "{:,.0f}"}).highlight_max(
                    subset=["Quantidade"], color="#ffb366"
                ),
                use_container_width=True
            )

            st.subheader("📈 Total de Focos de Queimada por Ano")
            st.pyplot(fig_total)

        except Exception as e:
            st.error(f"Erro ao gerar gráficos de queimadas: {e}")
