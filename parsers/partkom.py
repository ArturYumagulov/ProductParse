import requests
from environs import Env
from requests.auth import HTTPBasicAuth

from config.config_data import PARTKOM_CONF, ENV_PATH


def partkom(product_list: list, brand_name: str) -> dict:
    """Запрос к API Part-kom"""

    result_data = {}

    env = Env()
    Env().read_env()

    url = PARTKOM_CONF['url']

    headers = {
        "Accept": "application/json",
        "Content-type": "application/json"
    }

    for product in product_list:

        data = {"number": f"{product}"}

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
                    print(f"Цена {product} - Нет товара - PartKom")
                    result_data[product] = "Нет товара"

            if len(avr) > 0:
                print(f"Цена {product} - {float(min(avr))} - PartKom")
                result_data[product] = float(min(avr))

            else:
                print(f"Цена {product} - Нет товара - PartKom")
                result_data[product] = "Нет товара"
    # print(result_data)
    return result_data


if __name__ == '__main__':
    partkom(['w914/2', 'w811/80'], brand_name="MANN")
