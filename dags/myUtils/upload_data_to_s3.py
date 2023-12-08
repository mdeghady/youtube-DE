import json
import logging
import pandas as pd
from io import StringIO

from airflow.models import Variable
from airflow.providers.amazon.aws.operators.s3 import S3CreateObjectOperator


def push_to_s3(convert_data_to_parquet : bool , s3_bucket_name : str , **context):
    """

    :param convert_data_to_parquet:
    :param s3_bucket_name:
    :param context:
    :return:
    """

    data_format = "parquet" if convert_data_to_parquet else "json"

    # extract year, month, day to act as partition keys on S3
    execution_date = str(context["data_interval_start"])
    year = execution_date[:4]
    month = execution_date[5:7]
    day = execution_date[8:10]

    countries_codes = json.loads(Variable.get("countries_codes"))

    for country_code in countries_codes:

        data = context["task_instance"].xcom_pull(key=country_code + "_json")

        if convert_data_to_parquet:

            data = convert_to_parquet(data)
        else:
            data = json.dumps(data , ensure_ascii=False)



        saving_data_task = S3CreateObjectOperator(
            task_id="saving_data",
            s3_bucket=s3_bucket_name,
            s3_key=f"raw_statistics/year={year}/month={month}/day={day}/region={country_code}/data.{data_format}",
            data=data,
            aws_conn_id="aws_default"
        )


        saving_data_task.execute(context=context)
        logging.info(f"saving: {country_code}.{data_format} to {s3_bucket_name}")


def convert_to_parquet(json_file):

    #json_file = json.loads(json_file)

    normalized_df = pd.json_normalize(json_file['items'])

    #useful columns to save & drop the others

    cleaned_columns = ['id', 'snippet.title', 'snippet.publishedAt',
                       'snippet.channelTitle', 'snippet.categoryId',
                       'contentDetails.duration', 'statistics.viewCount'
                        , 'statistics.likeCount']

    df_cleaned = normalized_df[cleaned_columns].copy()
    #Adding duration in seconds column
    df_cleaned["duration"] = pd.to_timedelta(df_cleaned['contentDetails.duration']).dt.total_seconds().astype('int64')
    df_cleaned.drop('contentDetails.duration' , inplace=True , axis=1)

    df_cleaned["statistics.viewCount"] = df_cleaned["statistics.viewCount"].astype('int64')
    df_cleaned["statistics.likeCount"] = df_cleaned["statistics.likeCount"].astype('int64')

    df_cleaned["snippet.publishedAt"] = df_cleaned["snippet.publishedAt"].str[:10]#to extract only the date from the datetime object
    df_cleaned["snippet.publishedAt"] = pd.to_datetime(df_cleaned["snippet.publishedAt"])

    #Rename the columns to more clear name e.g. snippet.title -> title

    for col in df_cleaned.columns:
        split_name = col.split(".")

        df_cleaned.rename({col: split_name[-1]}, inplace=True, axis=1)

    #retuen data in apache parquet format
    return df_cleaned.to_parquet()










