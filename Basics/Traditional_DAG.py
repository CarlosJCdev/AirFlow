# Traditional Methods
from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime

 with DAG(
	 dag_id="my_dag_name",
	 start_date=datetime.datetime(2021, 1, 1),
	 schedule="@daily",
	 catchup=True, 
	 max_active_runs=1,
	 render_template_as_native_obj=True 
	 ) as DAG:
	 # Tasks..

#--------------------------------------------------
#Using Operators
from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime

 my_dag = DAG(
	 dag_id="my_dag_name",
	 start_date=datetime.datetime(2021, 1, 1),
	 schedule="@daily",
	 catchup=True, 
	 max_active_runs=1,
	 render_template_as_native_obj=True 
	 ) as DAG:

#--------------------------------------------------
#Complete example
from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime
import time

# Argumentos por defecto para todas las tareas del DAG
default_args = {
    'owner': 'airflow',            # Dueño del DAG (para trazabilidad)
    'depends_on_past': False,      # No depende del éxito de ejecuciones previas
    'retries': 1,                  # Intentar una vez más si falla
}

# Función de ejemplo que representa una tarea
def my_task_1_func():
    # Simula un trabajo pesado o una espera de recurso externo
    time.sleep(5)
    print("Tarea 1 ejecutada: valor 1")

# Definición del DAG utilizando un context manager
with DAG(
    dag_id='mi_dag_ejemplo',
    default_args=default_args,
    description='Un DAG simple de ejemplo con dos tareas secuenciales',
    schedule='@daily',                          # Ejecutar una vez al día
    start_date=datetime(2024, 11, 1),           # Fecha inicial de ejecución
    catchup=False,                              # No ejecutar días perdidos si el DAG estuvo detenido
    max_active_runs=1,                          # Solo una instancia activa a la vez
    render_template_as_native_obj=True,         # Renderiza valores como objetos nativos de Python
    tags=['ejemplo'],                           # Clasificación para UI
) as dag:

    # Primera tarea: llama a una función Python definida arriba
    my_task_1 = PythonOperator(
        task_id="my_task_1",                    # Identificador único de la tarea
        python_callable=my_task_1_func,         # Función a ejecutar
    )

    # Segunda tarea: usa una función anónima para imprimir
    my_task_2 = PythonOperator(
        task_id="my_task_2",
        python_callable=lambda: print("Tarea 2 ejecutada: valor 2"),
    )

    # Define orden de ejecución: my_task_1 se ejecuta antes que my_task_2
    my_task_1 >> my_task_2


