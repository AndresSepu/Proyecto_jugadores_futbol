# Dashboard de Análisis de Datos de Fútbol ⚽

Este proyecto es un **dashboard interactivo** desarrollado en Streamlit para visualizar y analizar datos de fútbol en profundidad. Diseñado para facilitar el análisis de equipos, ligas y jugadores, permite a los usuarios obtener información detallada y realizar predicciones a través de un modelo de Machine Learning.

## Características Principales 🛠️

1. **Conexión a Base de Datos MySQL**
   - El dashboard se conecta a una base de datos MySQL (`football_data`), extrayendo datos de varias tablas, como `clubs`, `players`, y `player_valuations`.
   - La función `conexion()` establece y gestiona la conexión con la base de datos, asegurando un acceso seguro y eficiente a los datos.

2. **Análisis de Equipos**
   - **Búsqueda de Equipos**: Permite buscar un club por su nombre para mostrar información detallada como tamaño de la plantilla, antigüedad promedio de los jugadores, nombre y capacidad del estadio.
   - **Visualizaciones**: Usa gráficos de barras, diagramas de caja y gráficos de dispersión para mostrar detalles del equipo, incluidas las edades y el valor de mercado de los jugadores.
   - **Interactividad**: Muestra etiquetas descriptivas y métricas clave, permitiendo a los usuarios ver detalles específicos del equipo en tiempo real.

3. **Exploración de Ligas**
   - **Selección de Liga**: Ofrece una lista desplegable con competiciones, permitiendo seleccionar una liga y ver una comparativa del número de jugadores por equipo.
   - **Comparación Visual**: Genera un gráfico de barras que representa la cantidad de jugadores por equipo dentro de la liga seleccionada, facilitando la comparación entre ellos.

4. **Análisis de Jugadores**
   - **Búsqueda de Jugador**: Permite encontrar un jugador específico y muestra su información completa en una tabla.
   - **Gráficos Personalizados**: Los usuarios pueden seleccionar características como posición, pie dominante, altura, etc., y visualizar gráficos de barras, pastel, dispersión y violin para explorar estas características.
   - **Distribución de Edad y Altura**: Visualiza la distribución de edades y alturas de los jugadores a través de gráficos de violín e histogramas, ofreciendo un análisis demográfico detallado.

5. **Predicción con Machine Learning**
   - **Modelo GBM**: El dashboard incluye un modelo de Gradient Boosting Machine (GBM) previamente entrenado (cargado desde `best_gbm.pkl`).
   - **Predicción Interactiva**: Permite ingresar valores específicos para realizar predicciones en tiempo real basadas en tres características de entrada.

## Tecnologías Utilizadas 💻

- **Python**: Base del desarrollo de la aplicación.
- **Streamlit**: Framework para crear aplicaciones web de datos de manera rápida y sencilla.
- **MySQL**: Base de datos para almacenar y gestionar información de fútbol.
- **Plotly**: Biblioteca de visualización para gráficos interactivos.
- **Sklearn & Joblib**: Para cargar y utilizar el modelo de Machine Learning.
- **Pandas & Numpy**: Procesamiento y manipulación de datos.

