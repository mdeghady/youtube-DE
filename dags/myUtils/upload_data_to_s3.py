import json
import logging
import pandas as pd
from io import StringIO

from airflow.models import Variable
from airflow.providers.amazon.aws.operators.s3 import S3CreateObjectOperator


def push_to_s3(convert_data_to_parquet : bool , s3_bucket_name : str , **context):
    """
    pushing data to se buckets according to the bucket name and data format [json or parquet]
    :param convert_data_to_parquet: boolean value to notify if I want to convert json to parquet or not
    :param s3_bucket_name:
    :param context: airflow context

    """

    #Decide which data format to use
    data_format = "parquet" if convert_data_to_parquet else "json"

    # extract year, month, day to act as partition keys on S3
    execution_date = str(context["data_interval_start"])
    year = execution_date[:4]
    month = execution_date[5:7]
    day = execution_date[8:10]

    #Get the countries_codes from airflow variables
    countries_codes = json.loads(Variable.get("countries_codes"))

    for country_code in countries_codes:

        #pull the json file according to the country code
        data = context["task_instance"].xcom_pull(key=country_code + "_json")

        #Decide to convert json to parquet or not
        if convert_data_to_parquet:
            data = convert_to_parquet(data)
        else:
            data = json.dumps(data , ensure_ascii=False)#to allow non ascii characters

        #pushing data to S3 buckets
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
    """
    convert json file to parquet format with some processing

    :param json_file: json_file which would be converted

    """
    #flattent the json file to make it easy to be processed
    normalized_df = pd.json_normalize(json_file['items'])

    #useful columns to save & drop the others
    cleaned_columns = ['id', 'snippet.title', 'snippet.publishedAt',
                       'snippet.channelTitle', 'snippet.categoryId',
                       'contentDetails.duration', 'statistics.viewCount'
                        , 'statistics.likeCount']

    df_cleaned = normalized_df[cleaned_columns].copy()#keeping the useful columns

    #Adding duration in seconds column
    df_cleaned["duration"] = pd.to_timedelta(df_cleaned['contentDetails.duration']).dt.total_seconds().astype('Int64')
    df_cleaned.drop('contentDetails.duration' , inplace=True , axis=1)#remove the old duration column

    #convert these columns from string type to float type to make it easy to ingest to data base
    df_cleaned["statistics.viewCount"] = pd.to_numeric(df_cleaned["statistics.viewCount"], errors="coerce",
                                                       downcast="float")
    df_cleaned["statistics.likeCount"] = pd.to_numeric(df_cleaned["statistics.likeCount"], errors="coerce",
                                                       downcast="float")

    # to extract only the date from the datetime object
    df_cleaned["snippet.publishedAt"] = df_cleaned["snippet.publishedAt"].str[:10]
    df_cleaned["snippet.publishedAt"] = pd.to_datetime(df_cleaned["snippet.publishedAt"])

    #Rename the columns to more clear names e.g. snippet.title -> title
    for col in df_cleaned.columns:
        split_name = col.split(".")

        df_cleaned.rename({col: split_name[-1]}, inplace=True, axis=1)

    #retuen data in apache parquet format
    return df_cleaned.to_parquet()










