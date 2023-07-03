import requests
from environs import Env


from config.config_data import BRANDS, AutoEURO_CONF


def autoeuro(products_list: list, brand_name: str):

    result_data = {}

    env = Env()
    Env().read_env()

    for article in products_list:

        params = {
            'delivery_key': env('AUTOEURO_DELIVERY_KEY'),
            'brand': brand_name,
            'code': article,
            'with_crosses': 0,
            'with_offers': 0
        }

        r = requests.get(AutoEURO_CONF['url'] + env('AUTOEURO_KEY'), params=params)
        if r.status_code != 400:
            response = r.json()['DATA']
            if len(response) > 0:
                prices = [item['price'] for item in response]
                min_price = min(prices)
                print(f"Цена {article} - {min_price} - Autoeuro")
                result_data[article] = min_price
        else:
            print(f"Цена {article} - Нет товара - Autoeuro")
            result_data[article] = "Нет товара"

    return result_data


if __name__ == '__main__':
    autoeuro(['w81180'], BRANDS["AUTOEURO"]['Mann'])
