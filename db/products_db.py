from sqlalchemy.ext.automap import automap_base
from sqlalchemy import Column, Integer, String, create_engine, Float, DateTime
from sqlalchemy.orm import declarative_base

Base = declarative_base()


class Products(Base):
    __tablename__ = 'products'

    aid = Column(Integer, primary_key=True, autoincrement=True)
    brand = Column(String(255))
    article = Column(String(255))
    price = Column(Float())
    date = Column(DateTime)
    platform = Column(String(255))

    def __init__(self, brand, article, price, date, platform):
        self.brand = brand
        self.article = article
        self.price = price
        self.date = date
        self.platform = platform


