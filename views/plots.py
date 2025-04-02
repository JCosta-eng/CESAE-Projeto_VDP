import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px

def show(data,dfs):
    st.title("📊 Análise e gráficos 🏎️")
    st.write("Aqui estão algumas visualizações de dados.")
    
    # Função auxiliar para converter milissegundos em um formato legível (ex: 1m 23.456s)
    def ms_para_legivel(ms):
        total_seconds = ms / 1000
        minutos = int(total_seconds // 60)
        segundos = int(total_seconds % 60)
        milissegundos = int(ms % 1000)
        return f"{minutos}m {segundos}.{milissegundos:03}s"

    # Função auxiliar para formatar rank com emojis
    def format_rank(idx):
        emojis = {0: "🥇", 1: "🥈", 2: "🥉"}
        return emojis.get(idx, f"{idx+1}º")

    # Função auxiliar para destacar as três primeiras linhas de uma tabela
    def highlight_top3(row):
        base_colors = {
            0: "background-color: rgba(255, 215, 0, 0.2);",   # Ouro suave
            1: "background-color: rgba(192, 192, 192, 0.2);",  # Prata suave
            2: "background-color: rgba(205, 127, 50, 0.2);"    # Bronze suave
        }
        style = base_colors.get(row.name, "")
        return [style] * len(row)

    #-----------------------------------------
    # Funções de Análise e Visualizações

    def piloto_mais_rapido(data):
        # Merge dos datasets: lap_times, drivers, races e circuits
        lap_times = data["dflap_times"].merge(data["dfdrivers"], on="driverId") \
                                    .merge(data["dfraces"], on="raceId") \
                                    .merge(data["dfcircuits"], on="circuitId")
        
        # Obter o menor tempo por circuito
        # Seleciona as colunas: nome da corrida (name_x), forename, surname, nome do circuito (name_y) e milliseconds
        best_laps = lap_times.loc[lap_times.groupby("circuitId")['milliseconds'].idxmin(),
                                ["name_x", "forename", "surname", "name_y", "milliseconds"]]
        
        # Criar a coluna "Nome" combinando forename e surname
        best_laps["Nome"] = best_laps["forename"] + " " + best_laps["surname"]
        
        # Selecionar e renomear as colunas conforme os headers desejados
        best_laps = best_laps[["name_x", "Nome", "name_y", "milliseconds"]]
        best_laps = best_laps.rename(columns={
            "name_x": "Grande Prémio",
            "name_y": "Circuito",
            "milliseconds": "Melhor volta"
        })
        
        return best_laps

    def pitstop_mais_rapido(data):
        # Mesclar os datasets necessários
        pit_stops = data["dfpit_stops"].merge(data["dfdrivers"], on="driverId").merge(data["dfraces"], on="raceId").merge(data["dfcircuits"], on="circuitId")
        
        # Identificar o pit stop mais rápido
        fastest_pitstops = pit_stops.loc[pit_stops.groupby("circuitId")['milliseconds'].idxmin(), ["name_x","forename","surname", "name_y", "milliseconds"]]
        
        # Criar a coluna "Nome" combinando forename e surname
        fastest_pitstops["Piloto"] = fastest_pitstops["forename"] + " " + fastest_pitstops["surname"]
        
        # Renomear colunas
        fastest_pitstops = fastest_pitstops.rename(columns={"name_x": "Grande Prémio", "Piloto": "Piloto", "name_y": "Circuito", "milliseconds": "Pit Stop mais rápido ms"})
        
        return fastest_pitstops

    def piloto_mais_rapido_ganhou(dfs):
    
        laps = dfs["lap_times"][["raceId", "driverId", "milliseconds"]].copy()
    
        laps = laps.merge(dfs["drivers"][["driverId", "forename", "surname"]], on="driverId")
        laps = laps.merge(dfs["races"][["raceId"]], on="raceId")
        laps = laps.merge(dfs["results"][["raceId", "driverId", "positionOrder"]], on=["raceId", "driverId"])
    
        laps = laps.dropna(subset=["milliseconds", "positionOrder"])
    
        best_laps = laps.loc[
            laps.groupby("raceId")["milliseconds"].idxmin(),
            ["raceId", "forename", "surname", "milliseconds", "positionOrder"]
        ]
    
        best_laps["Ganhou?"] = best_laps["positionOrder"] == 1
        best_laps = best_laps.rename(columns={
            "forename": "Nome",
            "surname": "Sobrenome",
            "milliseconds": "Melhor Tempo (ms)"
        })
    
        contagem = best_laps["Ganhou?"].value_counts().rename({True: "Sim", False: "Não"})
    
        fig, ax = plt.subplots(figsize=(1.6, 1.6))
        cores = ['#FF9999','#90EE90']
        labels = contagem.index.tolist()
        valores = contagem.values
        ax.pie(
            valores,
            labels=labels,
            autopct='%1.1f%%',
            colors=cores,
            startangle=90,
            wedgeprops={'edgecolor': 'white'}
        )
        #ax.set_title("O Piloto Mais Rápido Ganhou a Corrida?", fontsize=9)
    
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            st.pyplot(fig)
    
        percentagem = best_laps["Ganhou?"].mean() * 100
        st.metric("Percentagem de vitórias do piloto mais rápido", f"{percentagem:.1f}%")

    def pilotos_por_nacionalidades(dfs):
        # Top 10 nacionalidades dos pilotos
        top10_nacionalidades = dfs["drivers"]["nationality"].value_counts().head(10)
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

    def mostrar_top10_tabela(dfs):
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
            st.subheader("Top 10 Pitstops da História")
        else:
            top10 = df[df['year'] == selecao].nsmallest(10, 'milliseconds').copy()
            st.subheader(f"Top 10 Pitstops – {selecao}")

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
        
        # Configurar a largura das colunas e aplicar destaque nas top 3 posições
        col_widths = [{"selector": f"th.col{i}", "props": [("width", width)]}
                    for i, width in enumerate(["40px", "200px", "200px", "200px", "100px", "80px"])]
        styled_tabela = tabela.style.set_table_styles(col_widths).apply(highlight_top3, axis=1)
        
        # Utilizar st.write para renderizar o Styler
        st.write(styled_tabela)

    def grafico_tempo_medio_pitstops(data):
        pit_stops = data["dfpit_stops"].merge(data["dfraces"], on="raceId")
        
        # Calcular o tempo médio de pit stops por ano
        avg_pitstops = pit_stops.groupby("year")["milliseconds"].mean().reset_index()
        
        # Criar gráfico de linhas
        fig = px.line(avg_pitstops, x="year", y="milliseconds", title="Tempo Médio de Pit Stops ao Longo dos Anos", labels={"milliseconds": "Tempo Médio (ms)", "year": "Ano"})
        
        return fig

    def grafico_melhor_pitstop_por_ano(dfs):
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
            title="Melhor Pitstop por Ano"
        )
        
        fig.update_traces(line=dict(width=2), marker=dict(size=8))
        fig.update_layout(xaxis_title="Ano", yaxis_title="Tempo", hovermode="x unified")
        
        st.plotly_chart(fig, use_container_width=True)

    def circuitos_com_mais_dnfs(dfs):
        # Merge para análise dos DNFs
        df = dfs["results"].merge(dfs["status"], on="statusId")
        df = df.merge(dfs["races"][["raceId", "year", "circuitId"]], on="raceId")
        df = df.merge(dfs["circuits"][["circuitId", "name"]], on="circuitId") \
            .rename(columns={"name": "Circuito"})
        
        # Definir status que significam que o piloto terminou a corrida
        terminou_status = dfs["status"]["status"].str.contains(r"Finished|\+[1-9] Lap", case=False)
        status_ids_terminou = dfs["status"][terminou_status]["statusId"].unique()
        
        # Marcar DNFs
        df["DNF"] = ~df["statusId"].isin(status_ids_terminou)
        
        anos_disponiveis = ["Total"] + sorted(df["year"].unique())
        selecao = st.radio("Seleciona um ano ou vê o total histórico de abandonos", anos_disponiveis, horizontal=True)
        
        if selecao == "Total":
            df_filtrado = df.copy()
            titulo = "Circuitos com Maior Percentagem de DNFs na História"
        else:
            df_filtrado = df[df["year"] == selecao]
            titulo = f"Circuitos com Maior Percentagem de DNFs em {selecao}"
        
        total_participacoes = df_filtrado.groupby("Circuito")["driverId"].count()
        total_dnfs = df_filtrado[df_filtrado["DNF"]].groupby("Circuito")["driverId"].count()
        percentagens = (total_dnfs / total_participacoes).dropna() * 100
        top_percentagens = percentagens.sort_values(ascending=False).head(10)
        
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

    def piloto_com_mais_vitorias(dfs):
        dfresults = dfs["results"]
        dfdrivers = dfs["drivers"]
        
        # Filtrar os vencedores (positionOrder == 1)
        vitorias = dfresults[dfresults['positionOrder'] == 1]
        contagem = vitorias['driverId'].value_counts().reset_index()
        contagem.columns = ['driverId', 'vitorias']
        dados = contagem.merge(dfdrivers, on='driverId')
        dados['Piloto'] = dados['forename'] + ' ' + dados['surname']
        
        fig = px.scatter(
            dados.head(10),
            x='vitorias',
            y='Piloto',
            size='vitorias',
            color='vitorias',
            title='Pilotos com Mais Vitórias',
            labels={'vitorias': 'Vitórias', 'Piloto': 'Piloto'},
            color_continuous_scale='Blues'
        )
        fig.update_layout(
            yaxis=dict(autorange="reversed"),
            xaxis_title="Vitórias",
            yaxis_title="Piloto"
        )
        st.plotly_chart(fig, use_container_width=True)