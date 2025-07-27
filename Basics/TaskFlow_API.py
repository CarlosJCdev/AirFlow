from airflow.decorators import dag, task  # Decoradores modernos de DAG y tareas
from datetime import datetime
import time

# Decorador del DAG principal, define metadatos y comportamiento
@dag(
    dag_id="taskflow_api_dag",            # Identificador único del DAG
    schedule="@daily",                    # Frecuencia diaria
    start_date=datetime(2025, 4, 1),      # Fecha desde la cual se activa
    catchup=False,                        # No hacer catchup de fechas pasadas
    tags=["ejemplo", "taskflow"],         # Tags visibles en la UI de Airflow
)
def my_etl_dag():
    
    # Definición de la primera tarea con decorador @task
    @task()
    def my_task_1():
        time.sleep(5)                     # Simula procesamiento pesado
        print("Tarea 1 ejecutada: 1")     # Mensaje en logs de Airflow

    # Segunda tarea, también como función decorada
    @task()
    def my_task_2():
        print("Tarea 2 ejecutada: 2")

    # Orquestación: se ejecutan en orden
    my_task_2(my_task_1())                # my_task_1 >> my_task_2

# Airflow necesita que se instancie el DAG
dag = my_etl_dag()
