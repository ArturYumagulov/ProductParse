import httpx
import asyncio

from environs import Env

from config.config_data import TTS_CONF


async def tts(products_list: list, brand_name: str):
    """Запрос к API TTS"""

    result_dict = {}

    env = Env()
    Env().read_env()

    headers = {
        "Accept": "application/json",
        "Content-type": "application/json"
    }
    for article in products_list:

        url = f"{TTS_CONF['url']}/search/articles/?" \
              f"userlogin={env('TTS_LOGIN')}&" \
              f"userpsw={env('TTS_PASSWORD')}&" \
              f"number={article}&" \
              f"brand={brand_name}"

        async with httpx.AsyncClient() as requests:
            r = await requests.get(url, headers=headers)

        response = r.json()

        if isinstance(response, list):
            for item in response:
                if item['brand'] == brand_name:
                    print(f"Цена {article} - {item['price']} - TTS")
                    result_dict[article] = item['price']
                    break
        else:
            print(f"Цена {article} - Нет товара - TTS")
            result_dict[article] = "Нет товара"
    return result_dict


if __name__ == '__main__':
    # products = excel_reader('../data/sakura.xlsx', pagename='list', column='A')  # Данные с 1С (Артикула)
    asyncio.run(tts(['w914/2'], brand_name="Sakura"))
