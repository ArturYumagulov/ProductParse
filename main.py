import pandas as pd
from environs import Env
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from datetime import datetime

from parsers.moskvorechie import moskvorechie
from parsers.rossko import rossko
from parsers.partkom import partkom
from parsers.tts import tts

from db.products_db import Products
from db.product_schema_1C import products_table

from config.config_data import BRANDS


def create_or_update(data: dict, platform: str, brand: str):
    """Функция записи данных в БД"""

    sqlite = create_engine("sqlite:///data/db_files/products.db")
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


def run(brand_name: str):

    date = datetime.now().date()
    env = Env()
    Env().read_env('parsers/.env')

    tranzit_db = create_engine(
        f"mssql+pymssql://{env('MSSQL_LOGIN')}:{env('MSSQL_PASSWORD')}@{env('MSSQL_HOST')}/Marketing")

    session = sessionmaker(bind=tranzit_db)

    tranzit_db_session = session()

    products = tranzit_db_session.query(products_table).filter_by(brand=brand_name).all()  # Данные с 1С

    article = [str(product.vendor_code).strip() for product in products]

    # products = excel_reader(filename, pagename=page_name, column=column)  # Данные с 1С (Артикула-Файл)

    partkom_data = partkom(article, BRANDS['PARTKOM'][brand_name])
    create_or_update(partkom_data, platform="Partkom", brand=BRANDS['PARTKOM'][brand_name])

    rossko_data = rossko(article, BRANDS['ROSSKO'][brand_name])
    create_or_update(rossko_data, platform="Rossko", brand=BRANDS['ROSSKO'][brand_name])

    moskvorechie_data = moskvorechie(article, BRANDS['MOSKVORECHIE'][brand_name])
    create_or_update(moskvorechie_data, platform="Moskvorechie", brand=BRANDS['MOSKVORECHIE'][brand_name])

    tts_data = tts(article, BRANDS['TTS'][brand_name])
    create_or_update(tts_data, platform="TTS", brand=BRANDS['TTS'][brand_name])

    def sort_func(products_list, result_dict):
        result_list = []
        for item in products_list:
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
        'Part-kom': sort_func(article, partkom_data),
        'Moskvorechie': sort_func(article, moskvorechie_data),
        'Rossko': sort_func(article, rossko_data),
        'ТТС': sort_func(article, tts_data),
        'Дата_мониторинга': [f"{date.day}-{date.month}-{date.year}" for _ in range(len(products))]
    }
    df = pd.DataFrame(data)
    df.to_excel(f"data\\price_min_{brand_name}_{date}.xlsx")
    print("Данные сохранены")


if __name__ == '__main__':
    run('BIG FILTER')
