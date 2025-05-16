import requests
from datetime import datetime, timedelta
from io import BytesIO
from PyQt5.QtGui import QPixmap
from dotenv import load_dotenv
import os

#get coordinates api
#http://api.openweathermap.org/geo/1.0/direct?q={city name},{state code},{country code}&limit={limit}&appid={API key}
#req: city_name, limit (1), api_key

#get weather info api for 5 days (3h refresh)
#http://api.openweathermap.org/data/2.5/forecast?lat={lat}&lon={lon}&appid={API key}
#req: lat, lon, api_key


load_dotenv()
API_KEY = os.getenv("API_KEY")

def get_weather(city_name):
    lat, lon = get_coordinates(city_name)
    today_date = datetime.now()
    tomorrow_date = today_date + timedelta(days=1)
    today_date_str = today_date.strftime("%Y-%m-%d")
    tomorrow_date_str = tomorrow_date.strftime("%Y-%m-%d")
    target_tomorrow_time = tomorrow_date_str + " 15:00:00"
    api_url = f"http://api.openweathermap.org/data/2.5/forecast?lat={lat}&lon={lon}&appid={API_KEY}&units=metric"
    
    try:
        response = requests.get(api_url, timeout=5)
        response.raise_for_status()
        response_data = response.json()
        
    except requests.exceptions.HTTPError as http_error:
        print(f"HTTP Error: {http_error}")
        return None
    except Exception as e:
        print(f"Error: {e}")
        return None
    
    if not response_data or 'list' not in response_data:
        return None
    
    #get forecast
    today_forecast = response_data['list'][0]
    tomorrow_forecast = None
    for forecast in response_data['list']:
        if forecast['dt_txt'] == target_tomorrow_time:
            tomorrow_forecast = forecast
            break
    return {
        "today":{
            "weather_desc" : today_forecast['weather'][0]['description'],
            "temperature" : str(today_forecast['main']['temp']),
            "wind" : str(today_forecast['wind']['speed']),
            "humidity" : str(today_forecast['main']['humidity']),
            "visibility" :  str(today_forecast['visibility']),
            "pressure" : str(today_forecast['main']['pressure']),
            "date" : str(today_forecast['dt_txt'])
        },
        "tomorrow": {
            "weather_desc" : tomorrow_forecast['weather'][0]['description'],
            "temperature" : str(tomorrow_forecast['main']['temp']),
            "date" : str(tomorrow_date)
        }
    }

def get_coordinates(city_name):
    api_url = f"http://api.openweathermap.org/geo/1.0/direct?q={city_name}&limit={1}&appid={API_KEY}"
    try:
        response = requests.get(api_url, timeout=5)
        response.raise_for_status()
        response_data = response.json()

        if (response_data and 'lat' in response_data[0] and 'lon' in response_data[0]):
            lat = response_data[0]['lat']
            lon = response_data[0]['lon']
        else:
            return None
    except requests.exceptions.HTTPError as http_error:
        print(f"HTTP Error: {http_error}")
    except Exception as e:
        print(f"Error: {e}")

    return lat, lon