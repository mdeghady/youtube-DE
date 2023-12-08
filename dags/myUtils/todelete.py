import json
import os
import pandas as pd
import requests
from pathlib import Path
from io import StringIO

f = open("data.json" , encoding="utf-8")

data = json.load(f)

normalized_df = pd.json_normalize(data["items"])
cleaned_columns = ['id', 'snippet.title', 'snippet.publishedAt',
                       'snippet.channelTitle', 'snippet.categoryId',
                       'contentDetails.duration', 'statistics.viewCount'
                        , 'statistics.likeCount']
df_cleaned = normalized_df[cleaned_columns].copy()
#Adding duration in seconds column
df_cleaned["duration"] = pd.to_timedelta(df_cleaned['contentDetails.duration']).dt.total_seconds().astype('int64')
df_cleaned.drop('contentDetails.duration' , inplace=True , axis=1)

#Rename the columns to more clear name e.g. snippet.title -> title

for col in df_cleaned.columns:
    split_name = col.split(".")

    df_cleaned.rename({col : split_name[-1]} , inplace=True , axis=1)

df_cleaned["publishedAt"] = df_cleaned["publishedAt"].str[:10]
df_cleaned["publishedAt"] = pd.to_datetime(df_cleaned["publishedAt"])
print(df_cleaned["publishedAt"])

df_cleaned.to_parquet("small.parquet")

