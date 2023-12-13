import datetime

from myUtils import YoutubeRequest
from myUtils import upload_data_to_s3

from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from airflow.providers.amazon.aws.operators.glue_crawler import GlueCrawlerOperator


dag = DAG(
    dag_id = "youtube_DE_project",
    start_date=datetime.datetime(2023 , 12 , 8),
    schedule="@daily",
    catchup=False
)

retrieve_data = PythonOperator(
    task_id="retrieve_data",
    python_callable=YoutubeRequest.get_request,
    dag=dag
)

save_json_data_to_s3 = PythonOperator(
    task_id="save_json_data_to_s3",
    python_callable=upload_data_to_s3.push_to_s3,
    op_kwargs={
        "convert_data_to_parquet" : False,
        "s3_bucket_name" : "md-youtube-de-landing"
    },
    dag=dag
)

save_parquet_data_to_s3 = PythonOperator(
    task_id="save_parquet_data_to_s3",
    python_callable=upload_data_to_s3.push_to_s3,
    op_kwargs={
        "convert_data_to_parquet" : True,
        "s3_bucket_name" : "md-youtube-de-cleaned-data"
    },
    dag=dag
)

trigger_glue_crawler = GlueCrawlerOperator(
    task_id="trigger_glue_crawler",
    dag=dag,
    region_name = "us-east-1",
    config={
        "Name" : "youtube-de-crawler"}
)

retrieve_data >> save_json_data_to_s3 >> save_parquet_data_to_s3 >> trigger_glue_crawler

