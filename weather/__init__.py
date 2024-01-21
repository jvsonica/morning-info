import requests
import datetime
from weather.icons import icons

URL = 'https://wttr.in'
CITY = 'Oporto'


def safe_get(object, keys, default=None):
    current_dict = object.copy()
    try:
        for key in keys:
            current_dict = current_dict[key]
    except (KeyError, TypeError):
        return default
    return current_dict if current_dict is not None else default


def fetch_weather():
    res = requests.get(f'{URL}/{CITY}', params={
        'format': 'j1'
    })
    content = res.json()

    current_hour = int(f'{datetime.datetime.now().hour}00')
    current_date = str(datetime.date.today())

    previsions = []
    for day in content['weather']:
        for hour in day['hourly']:
            if len(previsions) > 6:
                break

            if day['date'] == current_date and current_hour > int(hour['time']):
                continue

            previsions.append({
                'date': day['date'],
                'day': day['date'][-2:],
                'hour': hour['time'].zfill(4)[:-2],
                'temperature': hour['tempC'],
                'feelslike': hour['FeelsLikeC'],
                'humidity': hour['humidity'],
                'precipMM': hour['precipMM'],
                'description': hour['weatherDesc'][0]['value'],
                'code': hour['weatherCode'],
                'icon': icons[hour['weatherCode']],
            })

    return previsions
