@ -1,142 +0,0 @@
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

def piloto_mais_rapido(data):
    # Mesclar os datasets necessários
    lap_times = data["dflap_times"].merge(data["dfdrivers"], on="driverId").merge(data["dfraces"], on="raceId").merge(data["dfcircuits"], on="circuitId")
    
    # Identificar o melhor tempo por circuito
    best_laps = lap_times.loc[lap_times.groupby("circuitId")['milliseconds'].idxmin(), ["name_x", "surname", "name_y", "milliseconds"]]
    
    # Renomear colunas
    best_laps = best_laps.rename(columns={"name_x": "Piloto", "surname": "Sobrenome", "name_y": "Circuito", "milliseconds": "Melhor Tempo (ms)"})
    
    return best_laps

def pitstop_mais_rapido(data):
    # Mesclar os datasets necessários
    pit_stops = data["dfpit_stops"].merge(data["dfdrivers"], on="driverId").merge(data["dfraces"], on="raceId").merge(data["dfcircuits"], on="circuitId")
    
    # Identificar o pit stop mais rápido
    fastest_pitstops = pit_stops.loc[pit_stops.groupby("circuitId")['milliseconds'].idxmin(), ["name_x", "surname", "name_y", "milliseconds"]]
    
    # Renomear colunas
    fastest_pitstops = fastest_pitstops.rename(columns={"name_x": "Piloto", "surname": "Sobrenome", "name_y": "Circuito", "milliseconds": "Pit Stop Mais Rápido (ms)"})
    
    return fastest_pitstops

def grafico_tempo_medio_pitstops(data):
    pit_stops = data["dfpit_stops"].merge(data["dfraces"], on="raceId")
    
    # Calcular o tempo médio de pit stops por ano
    avg_pitstops = pit_stops.groupby("year")["milliseconds"].mean().reset_index()
    
    # Criar gráfico de linhas
    fig = px.line(avg_pitstops, x="year", y="milliseconds", title="Tempo Médio de Pit Stops ao Longo dos Anos", labels={"milliseconds": "Tempo Médio (ms)", "year": "Ano"})
    
    return fig

def piloto_mais_rapido_ganhou(data):
    # Mesclar os datasets necessários
    lap_times = data["dflap_times"].merge(data["dfraces"], on="raceId").merge(data["dfresults"], on=["raceId", "driverId"]).merge(data["dfdrivers"], on="driverId")
    
  # Identificar o melhor tempo por corrida
    best_laps = lap_times.loc[lap_times.groupby("raceId")["milliseconds"].idxmin(), ["raceId", "forename", "surname", "milliseconds", "positionOrder"]]
    
    # Verificar se o piloto venceu a corrida
    best_laps["Ganhou?"] = best_laps["positionOrder"] == 1
    
    # Renomear colunas
    best_laps = best_laps.rename(columns={"name_x": "Piloto", "surname": "Sobrenome", "milliseconds": "Melhor Tempo (ms)"})
    
    return best_laps

# Streamlit Dashboard
def StreamDash():
    st.set_page_config(page_title="Dashboard", page_icon="\U0001F4CA", layout="wide")

    # Sidebar
    st.sidebar.title("Menu")
    page = st.sidebar.radio("Escolha uma página", ["Home", "Plots and Graphs", "About", "Piloto Mais Rápido", "Pit Stop Mais Rápido", "Gráfico Pit Stops", "Piloto Mais Rápido Ganhou?"])

    if page == "Home":
        home.show()
    elif page == "Plots and Graphs":
        plots.show()
    elif page == "About":
        about.show()
    elif page == "Piloto Mais Rápido":
        st.write("### Piloto mais rápido por circuito")
        fastest_pilots = piloto_mais_rapido(data)
        st.dataframe(fastest_pilots)
    elif page == "Pit Stop Mais Rápido":
        st.write("### Pit Stop mais rápido por circuito")
        fastest_pitstops = pitstop_mais_rapido(data)
        st.dataframe(fastest_pitstops)
    elif page == "Gráfico Pit Stops":
        st.write("### Tempo Médio de Pit Stops ao Longo dos Anos")
        fig = grafico_tempo_medio_pitstops(data)
        st.plotly_chart(fig)
    elif page == "Piloto Mais Rápido Ganhou?":
        st.write("### O piloto com a volta mais rápida venceu a corrida?")
        fastest_winners = piloto_mais_rapido_ganhou(data)
        st.dataframe(fastest_winners)

# Carregar dados
data = read_dataset()
StreamDash()