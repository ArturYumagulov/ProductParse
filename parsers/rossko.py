import zeep
from environs import Env

from config.config_data import ROSSKO_CONF


def rossko(article: str, brandname: str) -> float | list:

    client = zeep.client.Client(ROSSKO_CONF['url'])
    env = Env()
    Env().read_env()
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
                        return float(min(prices))
                    else:
                        return stock[0]['price']
        else:
            stock = products_offer[0]['stocks']['stock']
            if len(stock) > 0:
                prices = []
                for item in stock:
                    prices.append(float(item['price']))
                return float(min(prices))
            else:
                return stock[0]['price']
    else:
        return ["товара нет"]
