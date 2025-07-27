# AirFlow

# _Mejores practicas de AIRFLOW_

### Modularidad
Con las tareas, Airflow ayuda a que la modularidad sea más fácil de visualizar. No intentes hacer demasiado en una sola tarea. Aunque se puede construir todo un canal ETL en una sola tarea, esto dificultaría la resolución de problemas. También dificultaría la visualización del rendimiento de un DAG.
Al crear una tarea, es importante asegurarse de que sólo hará una cosa, como las funciones en Python.
Mira el siguiente ejemplo. Ambos DAG hacen lo mismo y fallan en el mismo punto del código. Sin embargo, en el DAG de la izquierda, está claro que la lógica `load` es la causante del fallo, mientras que esto no queda del todo claro en el DAG de la derecha.

### Determinismo
Un proceso determinista es aquel que produce el mismo resultado, dada la misma entrada. Cuando un DAG se ejecuta durante un intervalo determinado, debe generar siempre los mismos resultados. Aunque es una característica más compleja de los conductos de datos, el determinismo es importante para garantizar resultados coherentes.
Con Airflow, aprovecha Jinja-templating para pasar campos templados a los operadores Airflow en lugar de utilizar la función `datetime.now()` para crear datos temporales.
### ✳️ Ejemplo simple:
Supón que ejecutas tu DAG `weather_etl_taskflow` para el `2024-01-01`.
- **Determinista**: Si hoy y mañana corres el DAG para esa fecha (`2024-01-01`), el resultado (outputs, cargas, logs) es el mismo.
- **No determinista**: Si la tarea depende de `datetime.now()` o de datos en vivo, el resultado cambia cada vez que lo corres.
## 🔧 ¿Qué rompe el determinismo?

| Malas prácticas                                             | Consecuencia                                                              |
| ----------------------------------------------------------- | ------------------------------------------------------------------------- |
| Uso de `datetime.now()` o `date.today()`                    | Rompe la reproducibilidad: cambia en cada ejecución                       |
| Lecturas de APIs sin control de versión o filtros por fecha | Resultados impredecibles o inconsistentes                                 |
| Variables externas no versionadas                           | Dependencia en valores que pueden cambiar sin control                     |
| Falta de `execution_date` / `logical_date` en filtros       | No se asegura que los datos procesados coincidan con la ejecución del DAG |
## 📌 Variables útiles de Jinja templating

|Variable|Descripción|Ejemplo para `2024-01-15`|
|---|---|---|
|`{{ ds }}`|Fecha lógica en formato YYYY-MM-DD|`2024-01-15`|
|`{{ execution_date }}`|Fecha lógica completa con hora|`2024-01-15T00:00:00+00:00`|
|`{{ next_ds }}`|Fecha siguiente|`2024-01-16`|
|`{{ prev_ds }}`|Fecha anterior|`2024-01-14`|

Puedes usarlas en rutas de archivos, filtros SQL, nombres de logs, rutas de output, etc.

### Idempotencia
Cuando ejecutas un DAG varias veces para el mismo intervalo de tiempo (por ejemplo, el mismo `execution_date`), ¿Qué sucede con los datos?  
¿Se sobrescriben correctamente o terminas con registros duplicados en tu sistema de destino?

La **idempotencia** es la propiedad que garantiza que, **sin importar cuántas veces se ejecute un DAG para el mismo intervalo**, el resultado final sea **el mismo** que si se hubiera ejecutado una sola vez.
Esto es fundamental en pipelines de datos, ya que evita inconsistencias, duplicidades y errores al hacer reprocesos.
### ✅ Buenas prácticas para lograr idempotencia en Airflow
Para que tus DAGs sean idempotentes y deterministas, considera implementar las siguientes estrategias:
- **Sobrescritura controlada de archivos**  
    Cuando escribas archivos como salidas (CSV, Parquet, etc.), usa rutas basadas en `execution_date` o `{{ ds }}`. Así, si el DAG se ejecuta de nuevo para el mismo día, sobrescribirá el archivo anterior en lugar de generar uno nuevo con otro nombre o sufijo.
- **Patrón de "borrado y escritura" (`delete + insert`)**  
    En lugar de hacer `INSERT` directo en bases de datos o data warehouses, implementa una lógica que:
    1. Elimine previamente los registros del intervalo correspondiente (`WHERE date = '{{ ds }}'`); y
    2. Inserte los nuevos datos de manera limpia.
    Esto evita duplicados y mantiene la consistencia si se reejecuta el DAG.

### Orquestación no es Transformación
Airflow no está pensado para procesar grandes cantidades de datos. Si quieres ejecutar transformaciones en más de un par de gigabytes de datos, Airflow sigue siendo la herramienta adecuada para el trabajo; sin embargo, Airflow debería invocar otra herramienta, como dbt o Databricks, para ejecutar la transformación.

Normalmente, las tareas se ejecutan localmente en tu máquina o con nodos trabajadores en producción. De cualquier forma, sólo unos pocos gigabytes de memoria estarán disponibles para cualquier trabajo computacional que se necesite.

Céntrate en el uso de Airflow para transformaciones de datos muy ligeras y como herramienta de orquestación cuando manipules datos más grandes.
