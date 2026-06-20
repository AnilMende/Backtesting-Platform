import sys
import os
import pandas as pd

sys.path.append(
    os.path.abspath(
        os.path.join(os.path.dirname(__file__), "..")
    )
)

import yfinance as yf

from app.database.db import SessionLocal
from app.models.company import Company
from app.models.stock_price import StockPrice
from app.data.nifty100 import NIFTY_100_STOCKS


db = SessionLocal()

stocks = NIFTY_100_STOCKS

for symbol in stocks:

    print(f"Processing {symbol}")

    company = (
        db.query(Company)
        .filter(Company.symbol == symbol)
        .first()
    )

    if not company:
        continue

    data = yf.download(
    symbol,
    start="2020-01-01",
    end="2025-12-31",
    auto_adjust=True,
    group_by="column"
)

    data.reset_index(inplace=True)

    if isinstance(data.columns, pd.MultiIndex):
        data.columns = [col[0] for col in data.columns]
    

    count = 0
    
    existing_dates = {
    row[0]
    for row in db.query(StockPrice.trade_date)
    .filter(StockPrice.company_id == company.id)
    .all()
    }
    
    new_records = []
    
    for _, row in data.iterrows():
        
        trade_date = pd.to_datetime(row["Date"]).date()
        
        if trade_date in existing_dates:
            continue
        
        new_records.append(
            StockPrice(
                company_id=company.id,
                trade_date=trade_date,
                open_price=float(row["Open"]),
                high_price=float(row["High"]),
                low_price=float(row["Low"]),
                close_price=float(row["Close"]),
                volume=float(row["Volume"])
                )   
                )
        
        count += 1
        
    db.add_all(new_records)
    
    db.commit()
        
    print(f"Inserted {count} rows")

print("Historical Data Loaded Successfully")