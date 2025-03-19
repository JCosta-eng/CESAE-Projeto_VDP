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
import plotly as px
import sys
import os

#Paginas
sys.path.append(os.path.abspath("views"))

import home
import plots
import about

#-----------------------------------------
#Functions:
def StreamDash():
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
    
### >>>>>>>>>>>>>> Call Functions <<<<<<<<<<<<<<
StreamDash()