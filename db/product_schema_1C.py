from sqlalchemy import String, Date, Float, Integer, Table, Column
from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):
    pass


products_table = Table(
    "t_ost",
    Base.metadata,
    Column("brand", String(100)),
    Column("date", Date),
    Column("quantity", Integer),
    Column("price", Float),
    Column("price_sc", Float),
    Column("price_retail", Float),
    Column("vendor_code", String(100)),
)
