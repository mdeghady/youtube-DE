import requests
from airflow.models import Variable
import json
import logging



def get_request(**context):
    """
    retrieve data from YouTube api
    :param context: airflow context

    """
    api_key = Variable.get("api_key")

    # Variable returns countries_codes as a string so json.loads will return it to list
    countries_codes = json.loads(Variable.get("countries_codes"))

    for country_code in countries_codes:
        #call the YouTube api
        url = f"https://youtube.googleapis.com/youtube/v3/videos?part=contentDetails%2C%20snippet%2C%20statistics&chart=mostPopular&regionCode={country_code}&key={api_key}"
        response = requests.request(method="GET",url=url)

        #retrieve the data from the body of the response as python dictionary
        response_data = response.json()

        #pushing data tpo xcom for further processing
        context["task_instance"].xcom_push(key=country_code + "_json",
                                           value=response_data)

        logging.info(f"{country_code}.json saved to local disk")


