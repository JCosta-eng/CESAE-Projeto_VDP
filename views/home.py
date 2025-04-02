import streamlit as st
import os

def show():
    st.title("Fórmula 1 - Dashboard")
    st.title("História da Fórmula 1")
    st.write(historia_f1)
    def show_video():
        #Adicionar pasta "media" ao path
        media_folder = './media'

        # Liste os arquivos na pasta 'media' (se quiser listar os vídeos disponíveis)
        videos = [f for f in os.listdir(media_folder) if f.endswith(('.mp4', '.mov', '.avi'))]

        # Exibir vídeos da pasta 'media':
        for video in videos:
            video_title = video.split('.')[0]
            st.title(video_title)
            video_path = os.path.join(media_folder, video)
            st.video(video_path)
    
    show_video()
    st.title("Melhores ultrapassagens F1")
    st.video("https://www.youtube.com/watch?v=HzbGQYUDmSA&ab_channel=RacersReverie")
    
    historia_f1 = '''
    A Fórmula 1 (F1) é a principal categoria do automobilismo mundial, conhecida pela sua velocidade, inovação tecnológica e pelo espetáculo proporcionado ao público. A sua história remonta a 1950, quando foi estabelecido o primeiro Campeonato Mundial de Pilotos pela Federação Internacional de Automobilismo (FIA). A temporada inaugural contou com sete corridas, incluindo o Grande Prémio da Grã-Bretanha, realizado no circuito de Silverstone. O piloto italiano Giuseppe Farina, ao volante de um Alfa Romeo, sagrou-se o primeiro campeão mundial de F1.

    Nas décadas seguintes, a F1 evoluiu significativamente, tanto em termos tecnológicos quanto competitivos. Nos anos 1950, equipas como Alfa Romeo, Ferrari e Maserati dominaram as pistas, com pilotos lendários como Juan Manuel Fangio, que conquistou cinco títulos mundiais, estabelecendo um recorde que perduraria por décadas.

    Durante as décadas de 1960 e 1970, a F1 assistiu a avanços tecnológicos notáveis, incluindo a introdução de motores V8 e V12, além do desenvolvimento de carros com motores traseiros, melhorando a aerodinâmica e o desempenho. Equipas como a Lotus e a McLaren emergiram, e pilotos como Jim Clark e Jackie Stewart destacaram-se, com Stewart a defender melhorias significativas na segurança das corridas.

    A década de 1980 foi marcada pela introdução de motores turboalimentados, que aumentaram significativamente a potência dos veículos. Este período também foi caracterizado por intensas rivalidades, como a entre Ayrton Senna e Alain Prost, que proporcionou alguns dos momentos mais emocionantes da história da F1. Senna, com a sua habilidade excecional, conquistou três campeonatos mundiais, tornando-se uma lenda do desporto.

    Nos anos 1990, a F1 tornou-se mais global, com a introdução de novas corridas em diferentes continentes. Pilotos como Michael Schumacher estabeleceram novos padrões de domínio, especialmente com a Ferrari, conquistando cinco títulos consecutivos entre 2000 e 2004.

    A partir de 2014, a F1 adotou motores híbridos, combinando motores a combustão interna com sistemas de recuperação de energia, refletindo uma tendência global em direção à sustentabilidade. Equipas como a Mercedes dominaram essa era, com pilotos como Lewis Hamilton conquistando múltiplos campeonatos mundiais, igualando o recorde de sete títulos anteriormente estabelecido por Schumacher.

    Ao longo da sua história, a F1 tem sido um campo de inovação tecnológica, com avanços que frequentemente influenciam a indústria automóvel em geral. Além disso, a competição tem sido palco de histórias humanas emocionantes, com pilotos que se tornaram ícones globais, contribuindo para a rica tapeçaria que é a história da Fórmula 1.
    '''


    st.title("História da Fórmula 1")
    st.write(historia_f1)
    

