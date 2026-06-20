from app.database.db import engine
from app.database.base import Base

from app.models.company import Company
from app.models.stock_price import StockPrice
from app.models.fundamental import Fundamental

Base.metadata.create_all(bind=engine)

print("Tables Created Successfully")