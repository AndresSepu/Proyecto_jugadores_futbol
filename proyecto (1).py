import streamlit as st
import numpy as np
import pandas as pd
import mysql.connector
import plotly.express as px
from plotly.subplots import make_subplots
from datetime import datetime
import os
import sklearn
import pickle
from PIL import Image
import joblib

 
 # Función para conectar a la base de datos
def conexion():
    return mysql.connector.connect(
            host="localhost",
            user="root",
            password='CAsa556.',
            database='football_data',
            auth_plugin='mysql_native_password'
        )

st.set_page_config(page_title="Dashboard", page_icon=":bar_chart:", layout="wide")
tab1, tab2, tab3 = st.tabs(["Equipos", "Ligas", "Jugadores"])

with tab1:

    st.title("Futbol Dashboard")
    st.markdown("Prototipo")

       
    # Función para cargar los datos de clubes
    @st.cache_data
    def cargar_datos_clubes():
        conn = conexion()
        try:
            cursor = conn.cursor()
            query = "SELECT * FROM clubs"
            cursor.execute(query)
            columns = [desc[0] for desc in cursor.description]
            data = pd.DataFrame(cursor.fetchall(), columns=columns)
        finally:
            cursor.close()
            conn.close()
        return data

    # Función para cargar los datos de clubes y jugadores
    @st.cache_data
    def cargar_datos_clubes_y_jugadores():
        conn = conexion()
        try:
            cursor = conn.cursor()
            query = """
            SELECT clubs.*, players.*
            FROM clubs
            JOIN players ON clubs.club_id = players.club_id
            """
            cursor.execute(query)
            columns = [desc[0] for desc in cursor.description]
            data = pd.DataFrame(cursor.fetchall(), columns=columns)
        finally:
            cursor.close()
            conn.close()
        return data

    # Cargar los datos de clubes y jugadores
    try:
        datos = cargar_datos_clubes()
        datos_clubes_y_jugadores = cargar_datos_clubes_y_jugadores()
        st.subheader('Datos de valoraciones de Clubes')
        with st.expander("Mostrar datos de clubes"):
            st.dataframe(datos)
    except Exception as e:
        st.error(f"Error al cargar los datos: {e}")

    # Campo de entrada para el nombre del club
    nombre_club = st.text_input("Introduce el nombre de un club:")

    if nombre_club:
        try:
        
            # Filtrar los datos de clubes
            club = datos[datos['name'].str.contains(nombre_club, case=False, na=False)]
            
        # Modificar 
            if club.empty:
                st.write(f"No se encontraron datos para el club: {nombre_club}")
            else:
                # Extraer información del club
                tamaño_equipo = club['squad_size'].iloc[0]
                antigüedad = club['average_age'].iloc[0]
                nombre_estadio = club['stadium_name'].iloc[0]
                capacidad_estadio = club['stadium_seats'].iloc[0]
                nombre_club = club['name'].iloc[0]
                
                # Mostrar información del club en formato de etiqueta
                st.subheader(f"Datos del Club: {nombre_club}")
                st.write(f'Nombre oficial del club: {nombre_club}')
                st.write(f'Nombre del estadio: {nombre_estadio}')

                col1, col2, col3= st.columns(3)
                with col1:
                    st.title('Tamaño del equipo:');st.title(f'{tamaño_equipo} jugadores')
                with col2:
                    st.title('Antigüedad promedio de los jugadores:');st.title(f'{antigüedad} años')
                with col3:
                    st.title('Capacidad del estadio:');st.title(f'{capacidad_estadio} asientos')

                # Crear gráficos individuales
                #fig_tamaño = px.bar(x=['Tamaño del equipo'], y=[tamaño_equipo], color_discrete_sequence=['#ff9999'], title='Tamaño del equipo', labels={'y': 'Cantidad'})
                #fig_antiguedad = px.bar(x=['Antigüedad'], y=[antigüedad], color_discrete_sequence=['#66b3ff'], title='Antigüedad', labels={'y': 'Años'})
                #fig_capacidad = px.bar(x=['Capacidad del estadio'], y=[capacidad_estadio], color_discrete_sequence=['#99ff99'], title='Capacidad del estadio', labels={'y': 'Capacidad'})
                
                # Crear subplot
                #fig = make_subplots(rows=1, cols=3, subplot_titles=('Tamaño del equipo', 'Antigüedad del club', 'Capacidad del estadio'))
                #fig.add_trace(fig_tamaño['data'][0], row=1, col=1)
                #fig.add_trace(fig_antiguedad['data'][0], row=1, col=2)
                #fig.add_trace(fig_capacidad['data'][0], row=1, col=3)
                #fig.update_layout(height=600, width=1400, showlegend=False, title_text="Gráficos de Información del Club")
                #st.plotly_chart(fig)

                # Filtrar los datos de jugadores del club seleccionado
                
                club_players = datos_clubes_y_jugadores[datos_clubes_y_jugadores['current_club_name'].str.contains(nombre_club, case=False, na=False)]
        
                if not club_players.empty:
                    # Convertir columnas a string
                    club_players['first_name'] = club_players['first_name'].astype(str)
                    club_players['last_name'] = club_players['last_name'].astype(str)
                    
                    # Crear el gráfico de columnas
                    fig_jugadores = px.bar(
                        club_players,
                        x=club_players['first_name'] + ' ' + club_players['last_name'],
                        y='market_value_in_eur',
                        labels={'x': 'Jugadores', 'market_value_in_eur': 'Valor de Mercado Actual (en millones de EUR)'},
                        title=f'Valores de Mercado de los Jugadores de {nombre_club}',
                        color_discrete_sequence=['skyblue']
                    )
                    fig_jugadores.update_layout(xaxis_tickangle=-90)
                    st.plotly_chart(fig_jugadores)
                
                    # Calcular la edad de los jugadores
                    current_date = datetime.now()
                    club_players['age'] = club_players['date_of_birth'].apply(lambda x: current_date.year - pd.to_datetime(x).year)

                    # Crear gráfico de dispersión con las edades de los jugadores
                    fig_scatter = px.scatter(
                        club_players,
                        x=club_players['first_name'] + ' ' + club_players['last_name'],
                        y='age',
                        labels={'x': 'Jugadores', 'age': 'Edad'},
                        title=f'Edades de los Jugadores de {nombre_club}',
                        color_discrete_sequence=['#636EFA']
                    )
                    fig_scatter.update_layout(xaxis_tickangle=90)  # Colocar los nombres verticalmente
                    st.plotly_chart(fig_scatter)

                    fig_log = px.box(
                            club_players,
                            x='position',
                            y='market_value_in_eur',
                            labels={'x': 'Posición', 'y': 'Valor de Mercado por Posición (Escala Logarítmica)'},
                            title='Valor de Mercado en EUR (Escala Logarítmica)',
                            log_y=True  # Apply logarithmic scale to the y-axis
                            )
                    st.plotly_chart(fig_log)

                    st.write("**Análisis del Valor de Mercado por Posición (Escala Logarítmica):**")

                    # Observación de la Mediana
                    st.write("1. **Mediana de los Valores de Mercado:**")
                    st.write("La mediana, que es la línea horizontal dentro de cada caja, representa el valor de mercado central de los jugadores en cada posición. "
                    "Las posiciones con una mediana más alta indican que, en general, los jugadores en esas posiciones tienen un valor de mercado mayor.")

                    # Observación del Rango Intercuartil (IQR)
                    st.write("2. **Rango Intercuartil (IQR):**")
                    st.write("El IQR, que es el tamaño de la caja, muestra la dispersión de los valores de mercado entre el 25% y el 75% de los jugadores. "
                        "Un IQR más amplio en una posición sugiere que hay una mayor variabilidad en el valor de mercado de los jugadores en esa posición. "
                        "Por ejemplo, si los defensores tienen un IQR más estrecho que los delanteros, esto indica que los valores de mercado de los defensores son más homogéneos.")

                    # Observación de los Valores Atípicos (Outliers)
                    st.write("3. **Valores Atípicos (Outliers):**")
                    st.write("Los outliers son puntos que se encuentran fuera de los 'bigotes' del gráfico y representan jugadores cuyo valor de mercado es significativamente "
                    "mayor o menor que el resto en su posición. Una cantidad elevada de outliers en una posición puede indicar la presencia de jugadores estrellas "
                    "con un valor de mercado mucho más alto que sus compañeros de equipo en la misma posición.")

                    # Comparación General entre Posiciones
                    st.write("4. **Comparación entre Posiciones:**")
                    st.write("Comparando la distribución de los valores de mercado entre las diferentes posiciones, se puede identificar cuáles posiciones tienden a ser "
                    "más valiosas. Por ejemplo, si los delanteros y mediocampistas muestran valores de mercado más altos y con mayor dispersión, esto sugiere que "
                    "estas posiciones pueden ser más cruciales y competitivas en términos de mercado.")

                    # Conclusión General
                    st.write("**Conclusión General:**")
                    st.write("El análisis del valor de mercado por posición utilizando una escala logarítmica proporciona una visión clara de cómo se distribuyen los valores "
                    "en diferentes roles dentro del equipo. Esto puede ser útil para identificar tendencias en la valoración de jugadores según su posición, "
                    "así como para destacar posiciones clave que podrían ser estratégicamente importantes para un club.")
                    

                    # crear unas columnas para poner lado a lado las graficas
                    col5, col6 = st.columns(2)

                    # Crear gráfico de violín con las edades de los jugadores
                    with col5:
                        fig_violin = px.violin(
                                    club_players,
                                    y='age',
                                    box=True,
                                    points="all",
                                    labels={'age': 'Edad'},
                                    title=f'Distribución de Edades de los Jugadores de {nombre_club}',
                                    color_discrete_sequence=['#636EFA']
                                    )
                        fig_violin.update_layout(height=400, width=800)
                        st.plotly_chart(fig_violin)

                    # Crear histograma con las alturas de los jugadores
                    with col6:
                        fig_histogram = px.histogram(
                                        club_players,
                                        x='height_in_cm',
                                        nbins=20,
                                        labels={'height_in_cm': 'Altura (cm)'},
                                        title=f'Histograma de Alturas de los Jugadores de {nombre_club}',
                                        color_discrete_sequence=['#FFA07A']
                                        )
                        fig_histogram.update_layout(height=400, width=800) 
                        st.plotly_chart(fig_histogram)
                else:
                    st.write(f"No se encontraron jugadores para el club: {nombre_club}")
                
        except Exception as e:
            st.error(f"Error al procesar la información del club: {e}")

with tab2:
    @st.cache_data
    def cargar_datos_ligas():
        conn = conexion()
        try:
            cursor = conn.cursor()
            # Consultar los datos
            query = '''SELECT player_valuations.*, competitions.*
                    FROM player_valuations
                    INNER JOIN competitions
                    ON player_valuations.domestic_league_code = competitions.domestic_league_code'''
            cursor.execute(query)
            # Cargar los datos en un DataFrame de pandas
            columns = [desc[0] for desc in cursor.description]
            data = pd.DataFrame(cursor.fetchall(), columns=columns)
            return data
        finally:
            # Cerrar la conexión
            cursor.close()
            conn.close()

    # Llamada a la función para cargar los datos
    data_liga = cargar_datos_ligas()

    # Verifica que los datos se hayan cargado correctamente
    if data_liga.empty:
        st.write("No se cargaron datos.")
    else:
        # Crear una lista de competiciones única
        competitions = data_liga['competition_code'].unique()

        # Crear la lista desplegable en Streamlit
        sleccionar_liga = st.selectbox('Selecciona una competición', competitions)

        # Filtrar los datos según la competición seleccionada
        filtered_data = data_liga[data_liga['competition_code'] == sleccionar_liga]

        # Contar el número de jugadores en la competición seleccionada
        num_jugadores = filtered_data.shape[0]

        # Mostrar el nombre de la competición seleccionada y el número de jugadores
        st.write(f'Has seleccionado: {sleccionar_liga}')
        st.title('Comparativa entre el numero de jugadores por liga')

        # Agrupar los datos por equipo para el gráfico
        data_agru = data_liga.groupby('competition_code').size().reset_index(name='count')

        # Mostrar el métrico de número de jugadores
        st.metric(label='Número de jugadores', value=num_jugadores)

        if not data_agru.empty:
            # Crear el gráfico de barras con Plotly Express
            fig = px.bar(data_agru, 
                        x='competition_code', 
                        y='count', 
                        title='Número de jugadores por equipo en la competición seleccionada',
                        labels={'competition_code': 'Equipo', 'count': 'Número de jugadores'},
                        color='count',  # Colorea las barras según el número de jugadores
                        height=400)

            # Personalizar el gráfico
            fig.update_layout(xaxis_title='Equipo',
                            yaxis_title='Número de jugadores',
                            xaxis_tickangle=-90)  # Inclina las etiquetas del eje x para mejor legibilidad

            # Mostrar el gráfico en Streamlit
            st.plotly_chart(fig)
        else:
            st.write("No hay datos disponibles para la competición seleccionada.")

with tab3:
        #Cargo la imagen de los jugadores
        def mostrar_imagen():
            imagen = Image.open("streamlit_proyecto/futbol.jpg")

            st.image(image= imagen, caption="Jugadores")
            

        mostrar_imagen()

            
        #Cargo el df de jugadores
        df = pd.read_csv("streamlit_proyecto/df_nuevo_players.csv")

        with st.expander(label = "Datos de Jugadores"):
            st.dataframe(df)


        #Funcion para buscar un jugador en especifico
        def buscar_jugador():
            
            nombre_jugador = st.text_input("Ingresa el nombre del jugador:")

            # Filtrar el DataFrame
            if nombre_jugador:
                df_filtrado = df[df["name"].str.contains(nombre_jugador, case=False, na=False)]
                
                # Mostrar los resultados
                if not df_filtrado.empty:
                    st.write(f"Resultados para '{nombre_jugador}':")
                    st.dataframe(df_filtrado)
                else:
                    st.write(f"No se encontraron jugadores con el nombre '{nombre_jugador}'.")


        buscar_jugador()

        def crear_botones_graficas():

            caracteristicas = ["country_of_birth","position","foot","height_in_cm","current_club_domestic_competition_id","highest_market_value_in_eur","age"]
            graficos = ["Bar Chart", "Pie Chart", "Scatter Plot", "Line Chart"]
            
            # Seleccionar una característica y un tipo de gráfico
            caracteristicas_seleccionadas = st.selectbox(label="Características Más Relevantes de los Jugadores en General:", options=caracteristicas)
            tipo_grafico = st.selectbox(label="Selecciona el Tipo de Gráfico:", options=graficos)
            
            # Filtrar el df por las columnas seleccionadas
            df1 = df[[caracteristicas_seleccionadas, "name"]]
            df1 = df1.groupby(by=caracteristicas_seleccionadas).count().reset_index()

            st.text(f"Seleccionaste: {caracteristicas_seleccionadas} y {tipo_grafico}")
            
            # Mostrar el gráfico correspondiente
            if tipo_grafico == "Bar Chart":
                st.bar_chart(df1.set_index(caracteristicas_seleccionadas))
            
            elif tipo_grafico == "Pie Chart":
                fig_pie = px.pie(df1, values="name", names=caracteristicas_seleccionadas, title=f"Distribución de {caracteristicas_seleccionadas}")
                st.plotly_chart(fig_pie)
            
            elif tipo_grafico == "Scatter Plot":
                st.write("Selecciona las variables para el eje X y Y:")
                x_axis = st.selectbox(label="Variable Eje X", options=caracteristicas)
                y_axis = st.selectbox(label="Variable Eje Y", options=caracteristicas)
                scatter_plot = px.scatter(df, x=x_axis, y=y_axis, title=f"{x_axis} vs {y_axis}")
                st.plotly_chart(scatter_plot)
            
            elif tipo_grafico == "Line Chart":
                line_chart = px.line(df1, x=caracteristicas_seleccionadas, y="name", title=f"{caracteristicas_seleccionadas} a lo largo del tiempo")
                st.plotly_chart(line_chart)

        # Llamar a la función para crear botones y gráficos
        crear_botones_graficas()




        def subir_modelo():
            model = joblib.load('streamlit_proyecto/best_gbm.pkl')
            st.title("Predicción con Modelo de Machine Learning")

            #entrada de datos
            input_1 = st.number_input("Ingrese el valor de la característica 1:")
            input_2 = st.number_input("Ingrese el valor de la característica 2:")
            input_3 = st.number_input("Ingrese el valor de la característica 3:")

            # Botón 
            if st.button("Predecir"):
                prediccion = model.predict([[input_1, input_2, input_3]])
                st.write(f"La predicción del modelo es: {prediccion}")

        subir_modelo()
