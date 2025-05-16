import requests
import os
import json
from matplotlib import pyplot as plt
from datetime import datetime, timedelta
from io import BytesIO
from PyQt5.QtGui import QPixmap

#do dodania:
#   - więcej walut
#   - przy uruchomieniu programu domyślnie ma być wykres euro

#get currency data from start date to end date
#https://api.nbp.pl/api/exchangerates/rates/{table}/{code}/{startDate}/{endDate}/
#get data from today
#https://api.nbp.pl/api/exchangerates/rates/{tabe}/{code}/today/
CACHE_FILE = "resources/cache/rates.json"
CURRENCIES = ["EUR", "USD", "AUD", "GBP","JPY"]

def get_api_data(curr_code):
    api_url = f"https://api.nbp.pl/api/exchangerates/rates/A/{curr_code}/today/?format=json"    
    try:
        response = requests.get(api_url, timeout=5)
        response.raise_for_status()
        response_data = response.json()

        if('rates' in response_data and response_data['rates']):
            exchange_data = response_data['rates'][0]['mid']
            return exchange_data
        else:
            return None
    except requests.exceptions.HTTPError as http_error:
        print(f"HTTP Error: {http_error}")
    except Exception as e:
        print(f"Error: {e}")

def get_currency_chart(curr_code):
    #poprawić wyświetlanie, poprawić wygląd wykresu

    #get data from 10 days back
    today = datetime.today().date()
    ten_days_ago = today - timedelta(days=10)

    api_url = f"https://api.nbp.pl/api/exchangerates/rates/A/{curr_code}/{ten_days_ago}/{today}/?format=json"
    try:
        response = requests.get(api_url, timeout=5)
        response.raise_for_status()
        response_data = response.json()

        if ('rates' in response_data and response_data['rates']):
            exchange_period_data = response_data['rates']
        else:
            print("No API data.")
            return None
    except requests.exceptions.HTTPError as http_error:
        print(f"HTTP Error: {http_error}")
        return None
    except Exception as e:
        print(f"Error: {e}")
        return None

    #Currency chart
    #x values are dates, y values are currency values
    x_values = []
    y_values = []

    plt.style.available
    plt.style.use('fivethirtyeight')

    if not exchange_period_data:
        return None
    for day in exchange_period_data:
        date = day['effectiveDate']
        date_obj = datetime.strptime(date, "%Y-%m-%d")  
        date_str = date_obj.strftime("%m-%d")  
        exchange_day = int(day['mid'] * 100)

        x_values.append(date_str)
        y_values.append(exchange_day / 100)
    
    plt.figure(figsize=(10,5), dpi=100)
    plt.plot(x_values, y_values, label=f"Kurs {curr_code}", marker='.')
    
    buf = BytesIO()
    plt.savefig(buf, format='png')
    plt.close()
    buf.seek(0)

    pixmap = QPixmap()
    pixmap.loadFromData(buf.read())
    return pixmap

def save_offline_data():
    today = datetime.now().strftime("%Y-%m-%d")
    data = {}
    
    for code in CURRENCIES:
        rate = get_api_data(code)
        if rate is not None:
            data[code] = {
                "date" : today,
                "rate" : rate
            }
    if data:
        with open(CACHE_FILE, "w") as file:
            json.dump(data, file)

def load_offline_data():
    if os.path.exists(CACHE_FILE):
        with open(CACHE_FILE, "r") as file:
            try:
                return json.load(file)
            except json.JSONDecodeError:
                return {}
    return {}

def get_cached_live_data(curr_code):
    today = datetime.now().strftime("%Y-%m-%d")
    data = load_offline_data()

    if (curr_code in data and data[curr_code]["date"] == today):
        return data[curr_code]['rate']
    
    rate = get_api_data(curr_code)
    if rate:
        data[curr_code] = {
            'date' : today,
            'rate' : rate
        }
        return data[curr_code]['rate']
    
    with open(CACHE_FILE, 'w') as file:
        json.dump(data, file)
        return rate

    if curr_code in data:
        return data[curr_code]["rate"]
    
    return None

