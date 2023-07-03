import zeep
from environs import Env

from config.config_data import ROSSKO_CONF, ENV_PATH


def rossko(product_list: list, brandname: str) -> dict:
    """Запрос к API Rossko"""

    result_dict = {}

    client = zeep.client.Client(ROSSKO_CONF['url'])
    env = Env()
    Env().read_env()

    for article in product_list:
        result = client.service.GetSearch(
            env('ROSSKO_KEY_1'),
            env('ROSSKO_KEY_2'),
            article,
            ROSSKO_CONF['warehouse'])

        if result['success']:
            products_offer = result['PartsList']['Part']
            if len(products_offer) > 0:
                for item in products_offer:
                    if item['brand'] == brandname and item['stocks'] is not None:
                        stock = item['stocks']['stock']
                        if len(stock) > 0:
                            prices = []
                            for item in stock:
                                prices.append(float(item['price']))
                            print(f"Цена {article} - {float(min(prices))} - Rossko")
                            result_dict[article] = float(min(prices))
                        else:
                            print(f"Цена {article} - {stock[0]['price']} - Rossko")
                            result_dict[article] = stock[0]['price']
                    else:
                        print(f"Цена {article} - Нет товара - Rossko")
                        result_dict[article] = "Нет товара"
                        break
            else:
                stock = products_offer[0]['stocks']['stock']
                if len(stock) > 0:
                    prices = []
                    for item in stock:
                        prices.append(float(item['price']))
                    print(f"Цена {article} - {float(min(prices))} - Rossko")
                    result_dict[article] = float(min(prices))
                else:
                    print(f"Цена {article} - {stock[0]['price']} - Rossko")
                    result_dict[article] = stock[0]['price']
        else:
            print(f"Цена {article} - Нет товара - Rossko")
            result_dict[article] = "Нет товара"

    return result_dict


if __name__ == '__main__':
    rossko(['MH 67'], 'Mann')
