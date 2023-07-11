import requests
from config.config_data import MOSKVORECHIE_CONF, BRANDS, ENV_PATH
from environs import Env


def moskvorechie(product_list: list, brand_name: str) -> dict:

    result_data = {}

    env = Env()
    Env().read_env()

    for article in product_list:

        params = {'l': env('MOSKVORECHIE_LOGIN'),
                  'p': env('MOSKVORECHIE_KEY'),
                  'act': 'price_by_nr_firm', 'nr': article, 'v': '1'}

        r = requests.get(MOSKVORECHIE_CONF['url'], params=params)

        if isinstance(r.json()['result'], list):
            response = r.json()['result']
            # print(response)

            if len(response) > 0:
                prices = [item['price'] for item in response if item['brand'] == brand_name]
                if len(prices) > 0:
                    min_price = min(prices)
                    print(f"Цена {article} - {min_price} - Moskvorechie")
                    result_data[article] = min_price
                else:
                    print(f"Цена {article} - Нет товара - Moskvorechie")
                    result_data[article] = "Нет товара"
            else:
                print(f"Цена {article} - Нет товара - Moskvorechie")
                result_data[article] = "Нет товара"
        else:
            print(f"Цена {article} - Неверный ключ - Moskvorechie")
            result_data[article] = "Неверный ключ"

    return result_data


if __name__ == '__main__':
    moskvorechie(['CA25050'], BRANDS['MOSKVORECHIE']['Sakura'])
