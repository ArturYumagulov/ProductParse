import requests
from environs import Env
from requests.auth import HTTPBasicAuth

from config.config_data import PARTKOM_CONF


def partkom(article: str, brand_name: str) -> str | float:

    url = PARTKOM_CONF['url']

    headers = {
        "Accept": "application/json",
        "Content-type": "application/json"
    }

    data = {"number": f"{article}"}
    env = Env()
    Env().read_env()
    r = requests.get(url,
                     headers=headers,
                     auth=HTTPBasicAuth(env('PARTKOM_LOGIN'), env('PARTKOM_PASSWORD')),
                     params=data)

    if r.status_code == 200:
        avr = []
        for item in r.json():
            try:
                if item['maker'] == brand_name.upper() and item['detailGroup'] == 'Original':
                    avr.append(float(item['price']))
            except TypeError:
                pass

        if len(avr) > 0:
            return float(min(avr))
        else:
            return "нет данных"
