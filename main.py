import asyncio
from datetime import datetime

import pandas as pd
from environs import Env
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from config.config_data import BRANDS
from db.product_schema_1C import products_table
from db.products_db import Products
from parsers.autoeuro import autoeuro
from parsers.moskvorechie import moskvorechie
from parsers.partkom import partkom
from parsers.rossko import rossko
from parsers.tts import tts
from parsers.berg import berg

sqlite = create_engine("sqlite:///data/products.db")


def create_or_update(data: dict, platform: str, brand: str):
    """Функция записи данных в БД"""

    session = sessionmaker(bind=sqlite)
    s = session()

    date = datetime.now().date()

    for article, price in data.items():
        product = s.get(Products, article)
        if price == "Нет товара":
            price = 0
        if product is None:
            new_product = Products(article=article, brand=brand, price=price, date=date, platform=platform)
            s.add(new_product)
            s.commit()
            print(f"В базу записаны данные {article}- {price}")
        else:
            product.price = price
            product.date = date
            s.add(product)
            s.commit()
            print(f"В базe обновлены данные {article}- {price}")


def reserve(platform_name):

    res = sessionmaker(bind=sqlite)
    reserve_session = res()

    reserve_data = reserve_session.query(Products).filter_by(platform=platform_name).all()

    result_data = {}
    for reserve_product in reserve_data:
        result_data[reserve_product.article] = reserve_product.price
    return result_data


async def run(brand_name: str):

    date = datetime.now().date()
    env = Env()
    Env().read_env('parsers/.env')

    tranzit_db = create_engine(
        f"mssql+pymssql://{env('MSSQL_LOGIN')}:{env('MSSQL_PASSWORD')}@{env('MSSQL_HOST')}/Marketing")

    session = sessionmaker(bind=tranzit_db)

    tranzit_db_session = session()

    products = tranzit_db_session.query(products_table).filter_by(brand=brand_name).all()  # Данные с 1С
    article = [str(product.vendor_code).strip() for product in products]

    rossko_brands = BRANDS['ROSSKO'][brand_name]
    rossko_data = rossko(article, rossko_brands)
    create_or_update(rossko_data, platform="Rossko", brand=rossko_brands)

    moskvorechie_brands = BRANDS['MOSKVORECHIE'][brand_name]
    moskvorechie_data = moskvorechie(article, moskvorechie_brands)
    create_or_update(moskvorechie_data, platform="Moskvorechie", brand=moskvorechie_brands)

    partkom_brands = BRANDS['PARTKOM'][brand_name]
    partkom_data = partkom(article, partkom_brands)
    create_or_update(partkom_data, platform="Partkom", brand=partkom_brands)

    autoeuro_brands = BRANDS['AutoEURO'][brand_name]
    autoeuro_data = autoeuro(article, autoeuro_brands)
    create_or_update(autoeuro_data, platform="AutoEuro", brand=autoeuro_brands)

    berg_brands = BRANDS['BERG'][brand_name]
    berg_data = await berg(article, berg_brands)
    create_or_update(berg_data, platform='Berg', brand=berg_brands)

    tts_brand = BRANDS['TTS'][brand_name]
    tts_data = tts(article, tts_brand)
    create_or_update(tts_data, platform="TTS", brand=tts_brand)

    def sort_func(result_dict):
        result_list = []
        for item in article:
            if item in result_dict.keys():
                result_list.append(result_dict[item])
            else:
                result_list.append('Нет товара')
        return result_list

    data = {
        'Артикул': [product for product in article],
        'Tranzit-Закуп': [product.price for product in products],
        'Tranzit-Розница': [product.price_sc for product in products],
        'Tranzit-Опт': [product.price_retail for product in products],
        'Part-kom': sort_func(partkom_data),
        'Moskvorechie': sort_func(moskvorechie_data),
        'AutoEuro': sort_func(autoeuro_data),
        'Rossko': sort_func(rossko_data),
        'BERG': sort_func(berg_data),
        'ТТС': sort_func(tts_data),
        'Дата_мониторинга': [f"{date.day}-{date.month}-{date.year}" for _ in range(len(products))]
    }

    df = pd.DataFrame(data)
    df.to_excel(f"data\\price_min_{brand_name}_{date}.xlsx")
    print("Данные сохранены")


if __name__ == '__main__':
    asyncio.run(run('Sakura'))
    # create_or_update({'w914/2': 499.0, 'w811/80': 470.0}, platform="Partkom", brand='MANN-FILTER')


# TODO переписать все на ассинхрон
# TODO написать тесты
