import json
import logging

from airflow.models import Variable
from airflow.providers.amazon.aws.operators.s3 import S3CreateObjectOperator


def save_json(**context):
    countries_codes = json.loads(Variable.get("countries_codes"))

    for country_code in countries_codes:
        country_data = context["task_instance"].xcom_pull(key=country_code)

        execution_data = str(context["data_interval_start"])

        year = execution_data[:4]
        month = execution_data[5:7]
        day = execution_data[8:10]

        saving_task = S3CreateObjectOperator(
            task_id="saving_data_to_landing_bucket",
            s3_bucket="md-youtube-de-landing",
            s3_key=f"data/year={year}/month={month}/day={day}/{country_code}.json",
            data=json.dumps(country_data , ensure_ascii=False),
            aws_conn_id="aws_default"
        )
        saving_task.execute(context=context)
        logging.info(f"saving: {country_code}.json")
