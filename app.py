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
    dfcircuits = data["dfcircuits"]
    dfdrivers = data["dfdrivers"]
    
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
  
    # Display
    st.write("### Preview dos Circuitos")
    st.dataframe(dfcircuits.head())

    st.write("### Preview dos Pilotos")
    st.dataframe(dfdrivers.head()) 
  
    
### >>>>>>>>>>>>>> Call Functions <<<<<<<<<<<<<<

data = read_dataset()
StreamDash()