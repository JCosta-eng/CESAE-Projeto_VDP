import streamlit as st

def show():
    st.title("ℹ️ Sobre 🚦")
    st.write("Projeto de análise de dados com Streamlit e Pandas.")

    st.subheader("📌 Informações")
    st.markdown(
    """
    **Data Analyst | VDP - PL01**  
    **CESAE DIGITAL PORTO**  
    **Reskilling 4 Employment - Data Analyst 2024**  

    **Data:** 2 de Abril de 2025  
    **Docente:** Pedro Mendonça  
    **Autores:** Adriano Rodrigues, Bruno Bernardo e Jorge Costa
    """)

    # Objetivos do projeto
    st.subheader("🎯 Objetivos")
    st.markdown(
    """
    - Trabalhar datasets com **Pandas**  
    - Criar visualizações de dados com **Matplotlib, Seaborn e Plotly**  
    - Construir dashboards interativos com **Streamlit**  
    """)


    st.subheader("📊 Sobre o projeto")
    st.markdown(
    """
    Este projeto tem como objetivo a **análise e visualização de dados da Fórmula 1**, explorando estatísticas sobre corridas, equipas, pilotos e desempenhos ao longo das temporadas.  
    Através do **Streamlit**, é possível criar dashboards interativos que permitem uma compreensão intuitiva e dinâmica dos dados.  
    """
    )
