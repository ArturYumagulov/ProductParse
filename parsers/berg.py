import httpx
import asyncio
from environs import Env

from config.config_data import BRANDS, BERG_CONF

env = Env()
Env().read_env()


async def get_brands(brand_name):
    async with httpx.AsyncClient() as client:
        try:
            r = await client.get(f"{BERG_CONF['url']}v1.0/references/{BERG_CONF['Brands']}?key={env('BERG_KEY')}")
            response = r.json()['brands']
            brand = [name for name in response if name['name'] == brand_name][0]
            return brand
        except httpx.TimeoutException:
            print('Нет id')


async def berg(product_list: list, brand_name: str) -> dict:

    result_data = {}

    for article in product_list:

        async with httpx.AsyncClient() as client:
            brand_id = await get_brands(brand_name)
            clean_article = article.strip().replace('/', '').replace(' ', '')
            try:
                r = await client.get(f"{BERG_CONF['url']}ordering/get_stock.json?items[0][resource_article]="
                                     f"{clean_article}&items[0][brand_id]={brand_id['id']}&key={env('BERG_KEY')}")
                response = r.json()['resources']

                if len(response) > 0:
                    offers = response[0]['offers']
                    prices = [x['price'] for x in offers]
                    min_price = min(prices)
                    print(f"Цена {article} - {min_price} - Berg")
                    result_data[article] = min_price
                else:
                    print(f"Цена {article} - Нет товара - Berg")
                    result_data[article] = "Нет товара"
            except httpx.TimeoutException:
                print(f"Цена {article} - Нет товара - Berg")
                result_data[article] = "Нет товара"

    return result_data

if __name__ == '__main__':
    pass
