from sqlalchemy import create_engine
from products_db import Base


sqlite = create_engine("sqlite:///../data/products.db")
Base.metadata.create_all(sqlite)


# TODO подключить MYSQL_DB
