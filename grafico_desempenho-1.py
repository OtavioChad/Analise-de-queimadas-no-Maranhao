# grafico_desempenho.py
# Gera gráfico de barras agrupadas (Tempo, Comparações e Trocas)

import plotly.graph_objects as go

def plot_comparison(results):
    # filtra entradas inválidas
    results = {k: v for k, v in results.items() if k and v is not None}

    algs = list(results.keys())
    tempos = [results[a].tempo for a in algs]
    comps = [results[a].comparacoes for a in algs]
    swaps = [results[a].trocas for a in algs]

    # Normaliza o tempo para aparecer na mesma escala visual das comparações/trocas
    tempo_visual = [t * 1_000_000 for t in tempos]  # 1 segundo = 1.000.000 "unidades" visuais

    fig = go.Figure()

    # Barras agrupadas (cada métrica tem cor distinta)
    fig.add_trace(go.Bar(
        x=algs,
        y=tempo_visual,
        name="Tempo (s)",
        text=[f"{t:.6f}s" for t in tempos],  # exibe o valor real
        textposition="outside",
        marker_color="orange"
    ))

    fig.add_trace(go.Bar(
        x=algs,
        y=comps,
        name="Comparações",
        text=comps,
        textposition="outside",
        marker_color="#636EFA"
    ))

    fig.add_trace(go.Bar(
        x=algs,
        y=swaps,
        name="Trocas",
        text=swaps,
        textposition="outside",
        marker_color="#00CC96"
    ))

    # Layout final
    fig.update_layout(
        barmode="group",
        title="Desempenho dos Algoritmos de Ordenação",
        xaxis_title="Algoritmo",
        yaxis_title="Métricas (Comparações / Trocas / Tempo em s)",
        uniformtext_minsize=8,
        uniformtext_mode='hide'
    )

    # ✅ Legenda no canto superior direito
    fig.update_layout(
        legend=dict(
            x=1,
            y=1,
            xanchor="right",
            yanchor="top",
            bgcolor="rgba(255,255,255,0.8)",
            bordercolor="lightgray",
            borderwidth=1,
            font=dict(size=12, color="black")
        )
    )

    # Observação no rodapé
    fig.add_annotation(
        text="Obs: Barras de tempo multiplicadas por 1.000.000 para melhor visualização (valores reais exibidos sobre as barras).",
        xref="paper", yref="paper",
        x=0.5, y=-0.25, showarrow=False,
        font=dict(size=10, color="gray")
    )

    return fig
