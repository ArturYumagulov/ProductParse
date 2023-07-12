import httpx
import asyncio
from environs import Env


from config.config_data import BRANDS, AutoEURO_CONF


async def autoeuro(products_list: list, brand_name: str):

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

        async with httpx.AsyncClient() as client:
            try:
                r = await client.get(AutoEURO_CONF['url'] + env('AUTOEURO_KEY'), params=params)
                if r.status_code == 200:
                    print(r, article)
                    print(r.json())
                    if r.json()['META']['result'] == 'DATA':
                        response = r.json()['DATA']
                        if len(response) > 0:
                            prices = [item['price'] for item in response]
                            min_price = min(prices)
                            print(f"Цена {article} - {min_price} - Autoeuro")
                            result_data[article] = min_price
                    else:
                        print(f"Цена {article} - Нет товара - Autoeuro")
                        result_data[article] = "Нет товара"
                else:
                    print(f"Цена {article} - Нет товара - Autoeuro")
                    result_data[article] = "Нет товара"
            except httpx.TimeoutException:
                print(f"Цена {article} - Нет товара - Autoeuro")
                result_data[article] = "Нет товара"

    return result_data


if __name__ == '__main__':
    asyncio.run(autoeuro(['C 28 011'], BRANDS["AutoEURO"]['MANN-FILTER']))
