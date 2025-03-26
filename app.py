# Trabalho PL01 - VDP
## CESAE DIGITAL - PORTO - DATA ANALYST 2024
### Docente: Pedro Mendonça
#### Membros: Bruno Bernardo, Adriano Rodrigues, Jorge Costa.
##### 02 de Abril de 2025

#HOW TO ---------------------------------
### 1- Criar env
#run: python -m venv env
#run: env\Scripts\activate

### 2- Install libraries
#1 pip install -r requirements.txt
#2 python.exe -m pip install --upgrade pip


####3 
# verificar se está no environment "env", se não, correr env\Scripts\activate
# run: 

#-----------------------------------------

#Libraries 
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import sys
import os

#Paginas
sys.path.append(os.path.abspath("views"))

import home
import plots
import about

#dataframes
def read_dataset():
    datasets = {
        "dfcircuits": pd.read_csv("dataset/circuits.csv"),
        "dfconstructor_results": pd.read_csv("dataset/constructor_results.csv"),
        "dfconstructor_standings": pd.read_csv("dataset/constructor_standings.csv"),
        "dfconstructors": pd.read_csv("dataset/constructors.csv"),
        "dfdriver_standings": pd.read_csv("dataset/driver_standings.csv"),
        "dfdrivers": pd.read_csv("dataset/drivers.csv"),
        "dflap_times": pd.read_csv("dataset/lap_times.csv"),
        "dfpit_stops": pd.read_csv("dataset/pit_stops.csv"),
        "dfqualifying": pd.read_csv("dataset/qualifying.csv"),
        "dfraces": pd.read_csv("dataset/races.csv"),
        "dfresults": pd.read_csv("dataset/results.csv"),
        "dfseasons": pd.read_csv("dataset/seasons.csv"),
        "dfsprint_results": pd.read_csv("dataset/sprint_results.csv"),
        "dfstatus": pd.read_csv("dataset/status.csv")
    }
    return datasets
#-----------------------------------------
#Functions:
def StreamDash():
    
    #Dados
    #dfcircuits = data["dfcircuits"]
    #dfdrivers = data["dfdrivers"]
    
    #Config
    st.set_page_config(page_title="Dashboard", page_icon="📊", layout="wide")

    #Sidebar
    st.sidebar.title("Menu")
    page = st.sidebar.radio("Escolha uma página", ["Home", "Plots and Graphs", "About"])

    #Funcoes paginas
    if page == "Home":
        home.show()
        
    elif page == "Plots and Graphs":
        plots.show()
        
        
    elif page == "About":
        about.show()
    
    grafico_melhor_pitstop_por_ano(dfs)
    mostrar_top10_tabela(dfs)
    pilotos_por_nacionalidades(dfs)
    circuitos_com_mais_dnfs(dfs)
    piloto_com_mais_vitorias(dfs)
  
    # Display
    
    
    
    


######## FUNÇÕES BRUNO

def data_to_df(data): #auxiliar
    dfs = {
    "circuits": data["dfcircuits"],
    "constructor_results": data["dfconstructor_results"],
    "constructor_standings": data["dfconstructor_standings"],
    "constructors": data["dfconstructors"],
    "driver_standings": data["dfdriver_standings"],
    "drivers": data["dfdrivers"],
    "lap_times": data["dflap_times"],
    "pit_stops": data["dfpit_stops"],
    "qualifying": data["dfqualifying"],
    "races": data["dfraces"],
    "results": data["dfresults"],
    "seasons": data["dfseasons"],
    "sprint_results": data["dfsprint_results"],
    "status": data["dfstatus"]
}
    return dfs

def ms_para_legivel(ms): #auxiliar
    
    total_seconds = ms / 1000
    minutos = int(total_seconds // 60)
    segundos = int(total_seconds % 60)
    milissegundos = int(ms % 1000)
    return f"{minutos}m {segundos}.{milissegundos:03}s"

def format_rank(idx): #auxiliar

    emojis = {0: "🥇", 1: "🥈", 2: "🥉"}
    return emojis.get(idx, f"{idx+1}º")

def highlight_top3(row): #auxiliar
    base_colors = {
        0: "background-color: rgba(255, 215, 0, 0.2);",   # Ouro suave
        1: "background-color: rgba(192, 192, 192, 0.2);",  # Prata suave
        2: "background-color: rgba(205, 127, 50, 0.2);"    # Bronze suave
    }
    style = base_colors.get(row.name, "")
    return [style] * len(row)

def pilotos_por_nacionalidades(datasets):  # AnálisXe 1

    top10_nacionalidades = datasets["drivers"]["nationality"].value_counts().head(10)

    cores = ['#FF9999', '#FFCC99', '#FFFF99', '#CCFFCC', '#99CCFF', 
             '#CBA6F7', '#FFC0CB', '#B0E0E6', '#FFE4B5', '#E6E6FA']

    fig1, ax1 = plt.subplots(figsize=(7, 4))
    barras = ax1.bar(top10_nacionalidades.index, top10_nacionalidades.values, color=cores, edgecolor='black')
    ax1.bar_label(barras, label_type='center', color='black', fontsize=9)
    ax1.set_xlabel("Nacionalidade")
    ax1.set_ylabel("Nº de Pilotos")
    ax1.set_title("Top 10 Nacionalidades dos Pilotos")
    plt.xticks(rotation=45)
    fig1.tight_layout()
    st.pyplot(fig1)

def mostrar_top10_tabela(dfs):  # Análise 2

    df = dfs["pit_stops"].merge(
        dfs["results"][['raceId', 'driverId', 'constructorId']], on=['raceId', 'driverId']
    )
    df = df.merge(
        dfs["races"][['raceId', 'year', 'circuitId']], on='raceId'
    )
    df = df.merge(
        dfs["circuits"][['circuitId', 'name']], on='circuitId'
    ).rename(columns={'name': 'Circuito'})
    df = df.merge(
        dfs["drivers"][['driverId', 'forename', 'surname']], on='driverId'
    )
    df = df.merge(
        dfs["constructors"][['constructorId', 'name']], on='constructorId'
    ).rename(columns={'name': 'Equipa'})

    df['milliseconds'] = pd.to_numeric(df['milliseconds'], errors='coerce')
    df = df[df['milliseconds'] <= 300000]

    anos_disponiveis = ["História"] + sorted(df['year'].unique())
    selecao = st.radio("Seleciona o ano ou vê os melhores da história", anos_disponiveis, horizontal=True)

    if selecao == "História":
        top10 = df.nsmallest(10, 'milliseconds').copy()
        st.subheader("📋 Top 10 Pitstops da História")
    else:
        ano = int(selecao)
        top10 = df[df['year'] == ano].nsmallest(10, 'milliseconds').copy()
        st.subheader(f"📋 Top 10 Pitstops – {ano}")

    top10['Tempo (s)'] = (top10['milliseconds'] / 1000).round(3).astype(str) + "s"
    top10['Piloto'] = top10['forename'] + ' ' + top10['surname']
    top10.reset_index(drop=True, inplace=True)
    top10['Rank'] = [format_rank(i) for i in top10.index]

    colunas_base = ['Rank', 'Piloto', 'Equipa', 'Circuito', 'Tempo (s)']
    if selecao == "História":
        colunas_base.append('year')
        tabela = top10[colunas_base].rename(columns={'year': 'Ano'})
    else:
        tabela = top10[colunas_base]

    col_widths = [{"selector": f"th.col{i}", "props": [("width", width)]}
                  for i, width in enumerate(["40px", "200px", "200px", "200px", "100px", "80px"])]
    styled_tabela = tabela.style.set_table_styles(col_widths).apply(highlight_top3, axis=1)

    st.dataframe(styled_tabela, use_container_width=True, hide_index=True)

def grafico_melhor_pitstop_por_ano(dfs):  # Análise 2 Parte 2

    df = dfs["pit_stops"].merge(
        dfs["results"][['raceId', 'driverId', 'constructorId']], on=['raceId', 'driverId']
    )
    df = df.merge(
        dfs["races"][['raceId', 'year']], on='raceId'
    )
    df = df.merge(
        dfs["drivers"][['driverId', 'forename', 'surname']], on='driverId'
    )
    df = df.merge(
        dfs["constructors"][['constructorId', 'name']], on='constructorId'
    )

    df['milliseconds'] = pd.to_numeric(df['milliseconds'], errors='coerce')
    df = df[df['milliseconds'] <= 300000]

    melhores = df.sort_values('milliseconds').groupby('year').first().reset_index()
    melhores['Tempo (s)'] = (melhores['milliseconds'] / 1000).round(3)
    melhores['Piloto'] = melhores['forename'] + ' ' + melhores['surname']
    melhores['Equipa'] = melhores['name']

    fig = px.line(
        melhores,
        x='year',
        y='Tempo (s)',
        markers=True,
        hover_name='Piloto',
        hover_data={'Equipa': True, 'Tempo (s)': True, 'year': False},
        title="📈 Melhor Pitstop por Ano"
    )

    fig.update_traces(line=dict(width=2), marker=dict(size=8))
    fig.update_layout(xaxis_title="Ano", yaxis_title="Tempo", hovermode="x unified")

    st.plotly_chart(fig, use_container_width=True)

def circuitos_com_mais_dnfs(dfs):  # Análise 3 - versão final 100% correta


    # Merge dos dados principais
    df = dfs["results"].merge(dfs["status"], on="statusId")
    df = df.merge(dfs["races"][["raceId", "year", "circuitId"]], on="raceId")
    df = df.merge(dfs["circuits"][["circuitId", "name"]], on="circuitId").rename(columns={"name": "Circuito"})

    # Definir status que significam que o piloto terminou a corrida
    terminou_status = dfs["status"]["status"].str.contains(r"Finished|\+[1-9] Lap", case=False)
    status_ids_terminou = dfs["status"][terminou_status]["statusId"].unique()

    # Marcar como DNF todos os que NÃO terminaram
    df["DNF"] = ~df["statusId"].isin(status_ids_terminou)

    # Seleção do ano
    anos_disponiveis = ["Total"] + sorted(df["year"].unique())
    selecao = st.radio("Seleciona um ano ou vê o total histórico de abandonos", anos_disponiveis, horizontal=True)

    if selecao == "Total":
        df_filtrado = df.copy()
        titulo = "📉 Circuitos com Maior Percentagem de DNFs na História"
    else:
        df_filtrado = df[df["year"] == selecao]
        titulo = f"📉 Circuitos com Maior Percentagem de DNFs em {selecao}"

    # Total de participações por circuito
    total_participacoes = df_filtrado.groupby("Circuito")["driverId"].count()

    # Total de DNFs por circuito
    total_dnfs = df_filtrado[df_filtrado["DNF"]].groupby("Circuito")["driverId"].count()

    # Percentagem de DNFs por circuito
    percentagens = (total_dnfs / total_participacoes).dropna() * 100

    # Top 10 circuitos com mais DNFs
    top_percentagens = percentagens.sort_values(ascending=False).head(10)

    # Gráfico
    st.subheader(titulo)
    fig, ax = plt.subplots(figsize=(8, 5))
    cores = ['#FF9999', '#FFCC99', '#FFFF99', '#CCFFCC', '#99CCFF', 
             '#CBA6F7', '#FFC0CB', '#B0E0E6', '#FFE4B5', '#E6E6FA']
    barras = ax.barh(top_percentagens.index[::-1], top_percentagens.values[::-1],
                     color=cores[:len(top_percentagens)], edgecolor="black")
    ax.bar_label(barras, labels=[f"{v:.1f}%" for v in top_percentagens.values[::-1]],
                 fontsize=9, color='black')
    ax.set_xlabel("Percentagem de DNFs (por participação)")
    ax.set_ylabel("Circuito")
    ax.set_title("Top 10 Circuitos com Mais DNFs (%)")
    st.pyplot(fig)


def piloto_com_mais_vitorias(dfs):  # Análise 4

    dfresults = dfs["results"]
    dfdrivers = dfs["drivers"]

    # Filtrar apenas os vencedores (positionOrder == 1)
    vitorias = dfresults[dfresults['positionOrder'] == 1]
    contagem = vitorias['driverId'].value_counts().reset_index()
    contagem.columns = ['driverId', 'vitorias']

    # Juntar com os dados dos pilotos
    dados = contagem.merge(dfdrivers, on='driverId')
    dados['Piloto'] = dados['forename'] + ' ' + dados['surname']

    # Gráfico de dispersão
    fig = px.scatter(
        dados.head(10),
        x='vitorias',
        y='Piloto',
        size='vitorias',
        color='vitorias',
        title='🏁 Pilotos com Mais Vitórias',
        labels={'vitorias': 'Vitórias', 'Piloto': 'Piloto'},
        color_continuous_scale='Blues'
    )

    # Inverter ordem dos pilotos no eixo Y (mais vitórias no topo)
    fig.update_layout(
        yaxis=dict(autorange="reversed"),
        xaxis_title="Vitórias",
        yaxis_title="Piloto"
    )

    st.plotly_chart(fig, use_container_width=True)

### >>>>>>>>>>>>>> Call Functions <<<<<<<<<<<<<<

data = read_dataset()
dfs = data_to_df(data)
StreamDash()
