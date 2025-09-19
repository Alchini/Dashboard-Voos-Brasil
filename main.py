import streamlit as st
import pandas as pd
import plotly.express as px
import warnings

warnings.simplefilter(action='ignore', category=FutureWarning)

#Config da pag
st.set_page_config(
    page_title="Dashboard de Voos no Brasil",
    page_icon="✈️",
    layout="wide",
    initial_sidebar_state="expanded"
)

@st.cache_data
def carregar_dados():
    arquivos = {
        2022: 'dataset/flights_2022.csv',
        2023: 'dataset/flights_2023.csv',
        2024: 'dataset/flights_2024.csv',
    }
    lista_de_dfs = []
    for ano, caminho in arquivos.items():
        try:
            df_temp = pd.read_csv(caminho, sep=';', encoding='utf-8', dtype={'Código Justificativa': str})
            df_temp['ano'] = ano
            lista_de_dfs.append(df_temp)
        except FileNotFoundError:
            pass

    if not lista_de_dfs:
        st.error("Nenhum arquivo de dados encontrado em 'dataset/'.")
        st.stop()

    df_completo = pd.concat(lista_de_dfs, ignore_index=True)

    df_realizados = df_completo[df_completo['Situação Voo'] == 'REALIZADO'].copy()

    # Converte datas
    colunas_de_data = ['Partida Prevista', 'Partida Real']
    for coluna in colunas_de_data:
        df_realizados[coluna] = pd.to_datetime(df_realizados[coluna], format='%d/%m/%Y %H:%M', errors='coerce')
    df_realizados.dropna(subset=colunas_de_data, inplace=True)

    #cálculos de atraso
    df_realizados['atraso_partida_min'] = (df_realizados['Partida Real'] - df_realizados['Partida Prevista']).dt.total_seconds() / 60
    df_realizados['voo_atrasado'] = (df_realizados['atraso_partida_min'] > 15).astype(int)

    df_realizados['dia_da_semana'] = df_realizados['Partida Prevista'].dt.day_name()
    bins = [-1, 6, 12, 18, 24]
    labels = ['Madrugada', 'Manhã', 'Tarde', 'Noite']
    df_realizados['periodo_dia'] = pd.cut(df_realizados['Partida Prevista'].dt.hour, bins=bins, labels=labels, right=False)

    return df_realizados

df_realizados = carregar_dados()

st.title("Atrasos de Voos no Brasil")

# -------------------------------
st.sidebar.header("Filtros")
anos_disponiveis = sorted(df_realizados['ano'].unique())
anos_selecionados = st.sidebar.multiselect(
    "Selecione o Ano", options=anos_disponiveis, default=anos_disponiveis
)
if not anos_selecionados:
    st.sidebar.warning("Por favor, selecione pelo menos um ano.")
    st.stop()

df_filtrado = df_realizados[df_realizados['ano'].isin(anos_selecionados)]


#geral
st.header("Visão Geral do Período Selecionado")
total_voos = df_filtrado.shape[0]
total_atrasos = df_filtrado['voo_atrasado'].sum()
percentual_atrasos = (total_atrasos / total_voos) * 100 if total_voos > 0 else 0

col1, col2, col3 = st.columns(3)
col1.metric("Total de Voos Realizados", f"{total_voos:,}".replace(",", "."))
col2.metric("Atrasos na Partida (>15 min)", f"{total_atrasos:,}".replace(",", "."))
col3.metric("Percentual de Atrasos", f"{percentual_atrasos:.2f}%")

st.divider()

#tabs
tab1, tab2, tab3 = st.tabs(["🏆 Aeroportos", "✈️ Companhias", "📅 Dias/Períodos"])

with tab1:
    st.subheader("Top 10 Aeroportos com Mais Atrasos")
    atrasos_por_aeroporto = df_filtrado.groupby('ICAO Aeródromo Origem')['voo_atrasado'].sum().nlargest(10)
    if not atrasos_por_aeroporto.empty:
        fig = px.bar(
            atrasos_por_aeroporto.reset_index(),
            x="voo_atrasado",
            y="ICAO Aeródromo Origem",
            orientation="h",
            color="voo_atrasado",
            color_continuous_scale="Blues",
            title="Top 10 Aeroportos com Mais Atrasos"
        )
        st.plotly_chart(fig, use_container_width=True)

with tab2:
    st.subheader("Comparativo Anual de Atrasos (Top 10 Companhias)")
    if len(anos_selecionados) > 1:
        top_10 = df_filtrado.groupby('ICAO Empresa Aérea')['voo_atrasado'].sum().nlargest(10).index
        df_top = df_filtrado[df_filtrado['ICAO Empresa Aérea'].isin(top_10)]
        comp = df_top.groupby(['ano', 'ICAO Empresa Aérea'])['voo_atrasado'].sum().reset_index()

        fig = px.bar(
            comp, x="ICAO Empresa Aérea", y="voo_atrasado", color="ano",
            barmode="group", title="Comparativo de Atrasos por Companhia Aérea"
        )
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("Selecione mais de um ano para comparar companhias.")

with tab3:
    col_dia, col_periodo = st.columns(2)

    with col_dia:
        st.markdown("##### Por Dia da Semana")
        atrasos_dia = df_filtrado.groupby('dia_da_semana')['voo_atrasado'].sum().reset_index()
        fig = px.bar(
            atrasos_dia, x="dia_da_semana", y="voo_atrasado", color="voo_atrasado",
            color_continuous_scale="Magma", title="Atrasos por Dia da Semana"
        )
        st.plotly_chart(fig, use_container_width=True)

    with col_periodo:
        st.markdown("##### Por Período do Dia")
        atrasos_periodo = df_filtrado.groupby('periodo_dia')['voo_atrasado'].sum().reset_index()
        fig = px.bar(
            atrasos_periodo, x="periodo_dia", y="voo_atrasado", color="voo_atrasado",
            color_continuous_scale="Plasma", title="Atrasos por Período do Dia"
        )
        st.plotly_chart(fig, use_container_width=True)


st.divider()
st.header("📈📉 Tendências de Atrasos nos Últimos 3 Anos (2022–2024)")

anos_necessarios_tendencia = [2022, 2023, 2024]
anos_presentes_no_filtro = df_filtrado['ano'].unique()

if all(ano in anos_presentes_no_filtro for ano in anos_necessarios_tendencia):

    df_pivot = df_filtrado.pivot_table(
        index='ICAO Aeródromo Origem',
        columns='ano',
        values='voo_atrasado',
        aggfunc='sum'
    ).fillna(0)

    for ano in anos_necessarios_tendencia:
        if ano not in df_pivot.columns:
            df_pivot[ano] = 0

    condicao_aumento = (df_pivot[2023] >= df_pivot[2022]) & (df_pivot[2024] > df_pivot[2023])
    condicao_reducao = (df_pivot[2023] <= df_pivot[2022]) & (df_pivot[2024] < df_pivot[2023])

    df_aumento = df_pivot[condicao_aumento].copy()
    df_reducao = df_pivot[condicao_reducao].copy()

    df_aumento['Variacao_Total'] = df_aumento[2024] - df_aumento[2022]
    df_reducao['Variacao_Total'] = df_reducao[2024] - df_reducao[2022]

    df_aumento.sort_values('Variacao_Total', ascending=False, inplace=True)
    df_reducao.sort_values('Variacao_Total', ascending=True, inplace=True)

    col_tend_aumento, col_tend_reducao = st.columns(2)

    with col_tend_aumento:
        st.subheader("📈 Tendência de Aumento")
        if not df_aumento.empty:
            top_10_aumento = df_aumento.head(10).reset_index()
            fig_aumento = px.bar(
                top_10_aumento,
                x="Variacao_Total",
                y="ICAO Aeródromo Origem",
                orientation="h",
                color="Variacao_Total",
                color_continuous_scale="Reds",
                title="Top 10 Aeroportos com Maior Aumento de Atrasos (2022→2024)"
            )
            st.plotly_chart(fig_aumento, use_container_width=True)
            with st.expander("🔍 Ver dados detalhados da tendência de aumento"):
                st.dataframe(top_10_aumento)
        else:
            st.info("Nenhum aeroporto apresentou tendência consistente de aumento.")

    with col_tend_reducao:
        st.subheader("📉 Tendência de Redução")
        if not df_reducao.empty:
            top_10_reducao = df_reducao.head(10).reset_index()
            top_10_reducao['Variacao_Absoluta'] = top_10_reducao['Variacao_Total'] * -1
            fig_reducao = px.bar(
                top_10_reducao,
                x="Variacao_Absoluta",
                y="ICAO Aeródromo Origem",
                orientation="h",
                color="Variacao_Absoluta",
                color_continuous_scale="Greens",
                title="Top 10 Aeroportos com Maior Redução de Atrasos (2022→2024)"
            )
            st.plotly_chart(fig_reducao, use_container_width=True)
            with st.expander("🔍 Ver dados detalhados da tendência de redução"):
                st.dataframe(top_10_reducao)
        else:
            st.info("Nenhum aeroporto apresentou tendência consistente de redução.")

    st.markdown("### 🔎 Evolução Ano a Ano dos Atrasos (2022–2024)")
    df_line = df_filtrado.groupby(['ano', 'ICAO Aeródromo Origem'])['voo_atrasado'].sum().reset_index()
    fig_line = px.line(
        df_line,
        x="ano",
        y="voo_atrasado",
        color="ICAO Aeródromo Origem",
        markers=True,
        title="Evolução dos Atrasos por Aeroporto"
    )
    st.plotly_chart(fig_line, use_container_width=True)

else:
    st.info("Para visualizar a análise de tendência, é necessário ter dados de 2022, 2023 e 2024 selecionados.")
