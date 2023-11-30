import requests
from airflow.models import Variable
import json
import logging

def getRequest(**context):
    api_key = Variable.get("api_key")
    # Variable returns countries_codes as a string so json.loads will return it to list
    countries_codes = json.loads(Variable.get("countries_codes"))
    for country_code in countries_codes:
        url = f"https://youtube.googleapis.com/youtube/v3/videos?part=contentDetails%2C%20snippet%2C%20statistics&chart=mostPopular&regionCode={country_code}&key={api_key}"
        response = requests.request(method="GET",url=url)

        context["task_instance"].xcom_push(key = country_code , value = response.json())

        logging.info(f"The Used url is: {url}")


