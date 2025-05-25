import requests
from dotenv import load_dotenv
import os

#load api key
load_dotenv()
API_KEY = os.getenv("NEWS_API_KEY")
lang_env = os.environ.get("LANG")
lang_code = lang_env.split(".")[0].split("_")[0]
param_country = 'pl'


def get_parameters(category):
    return {
        'apiKey' : API_KEY,
        'country' : param_country,
        'language' : 'pl',
        'category' : category
    }

def get_news(category):
    parameters = get_parameters(category)
    api_url = 'https://newsdata.io/api/1/news?'

    try:
        response = requests.get(api_url, params=parameters, timeout=5)
        response.raise_for_status()
        response_data = response.json()

        if response_data['totalResults'] == 0:
            return None
        else:
            return response_data['results']

    except requests.exceptions.HTTPError as http_error:
        print(f"HTTP Error: {http_error}")
    except Exception as e:
        print(f"Error: {e}")
    








