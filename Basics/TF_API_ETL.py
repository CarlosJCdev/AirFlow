from airflow.decorators import dag, task
# Módulo para definir fecha de inicio del DAG
from datetime import datetime
# Pandas se usará para estructurar la salida como DataFrame (ETL realista)
import pandas as pd

# Logging nativo de Airflow para trazabilidad en los logs de tareas
from airflow.utils.log.logging_mixin import LoggingMixin
log = LoggingMixin().log  # Instancia de logger

# Definición del DAG usando TaskFlow API con decorador @dag
@dag(
    dag_id="weather_etl_taskflow",              # Identificador único del DAG (visible en la UI)
    start_date=datetime(2023, 1, 1, 9, 0),      # Fecha y hora de inicio de ejecución
    schedule="@daily",                          # Frecuencia de ejecución: diario
    catchup=True,                               # Permite ejecutar días pendientes si el DAG estuvo inactivo
    max_active_runs=1,                          # Solo una instancia activa a la vez para evitar solapamientos
    render_template_as_native_obj=True,         # Permite pasar tipos de datos nativos entre tareas (Jinja compatible)
    tags=["ETL", "weather", "taskflow"]         # Clasificación para UI y búsqueda
)
def weather_etl():
    # Tarea de extracción: simula obtención de datos desde una API meteorológica
    @task()
    def extract_data() -> dict:
        log.info("Extracting data from a weather API")
        return {
            "date": "2023-01-01",               # Fecha de observación
            "location": "NYC",                  # Ciudad
            "weather": {
                "temp": 33,                     # Temperatura en °F
                "conditions": "Light snow and wind"  # Condiciones climáticas
            }
        }

    # Tarea de transformación: convierte los datos crudos en una estructura tabular simple
    @task()
    def transform_data(raw_data: dict) -> list:
        log.info("Transforming raw weather data")
        return [[
            raw_data["date"],
            raw_data["location"],
            raw_data["weather"]["temp"],
            raw_data["weather"]["conditions"]
        ]]

    # Tarea de carga: convierte los datos transformados en un DataFrame (como paso previo a cargar en un sistema externo)
    @task()
    def load_data(transformed_data: list):
        # Construye un DataFrame con columnas nombradas
        df = pd.DataFrame(transformed_data, columns=[
            "date", "location", "weather_temp", "weather_conditions"
        ])
        # Muestra el DataFrame en los logs para trazabilidad
        log.info("Loaded DataFrame:\n%s", df.to_string(index=False))

    # Encadenamiento de tareas: orden lógico del ETL
    raw = extract_data()                # Etapa 1: Extracción
    transformed = transform_data(raw)  # Etapa 2: Transformación (usa output anterior)
    load_data(transformed)             # Etapa 3: Carga final (usa output anterior)

# Instanciación del DAG para que Airflow lo registre automáticamente
dag = weather_etl()
