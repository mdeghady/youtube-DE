import datetime
import myUtils
from myUtils import YoutubeRequest
from myUtils import SaveInitialData

from airflow import DAG
from airflow.operators.python_operator import PythonOperator


dag = DAG(
    dag_id = "youtube_DE_project",
    start_date=datetime.datetime(2023 , 11 , 29),
    schedule="@daily",
    catchup=True
)

retrieve_data = PythonOperator(
    task_id="retrieve_data",
    python_callable=YoutubeRequest.getRequest,
    dag=dag
)

save_data = PythonOperator(
    task_id="save_data",
    python_callable=SaveInitialData.save_json,
    dag=dag
)

retrieve_data >> save_data