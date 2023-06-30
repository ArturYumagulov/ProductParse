from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from datetime import datetime
import pandas as pd

from db.products_db import Products
from parsers.rossko import rossko
from parsers.partkom import partkom
from parsers.tts import tts
from services.utils.excel import excel_reader
from config.config_data import DATA_FILE, BRANDS


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


def run(filename: str, page_name: str, column: str, brand_name: str):
    date = datetime.now().date()
    products = excel_reader(filename, pagename=page_name, column=column)  # Данные с 1С (Артикула)

    partkom_data = partkom(products, BRANDS['PARTKOM'][brand_name])
    create_or_update(partkom_data, platform="Partkom", brand=BRANDS['PARTKOM'][brand_name])

    rossko_data = rossko(products, BRANDS['ROSSKO'][brand_name])
    create_or_update(rossko_data, platform="Rossko", brand=BRANDS['ROSSKO'][brand_name])

    tts_data = tts(products, BRANDS['TTS'][brand_name])
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
        'Артикул': [product for product in products],
        'Part-kom': sort_func(products, partkom_data),
        'Rossko': sort_func(products, rossko_data),
        'ТТС': sort_func(products, tts_data),
        'Дата_мониторинга': [f"{date.day}-{date.month}-{date.year}" for i in range(len(products))]
    }
    df = pd.DataFrame(data)
    df.to_excel(f"data\\price_min_{brand_name}_{date}.xlsx")
    print("Данные сохранены")


if __name__ == '__main__':
    run(DATA_FILE, page_name='list', column='A', brand_name='Sakura')
    pass
