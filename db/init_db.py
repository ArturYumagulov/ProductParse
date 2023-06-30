from sqlalchemy import create_engine
from products_db import Base


sqlite = create_engine("sqlite:///../data/db_files/products.db")
Base.metadata.create_all(sqlite)
