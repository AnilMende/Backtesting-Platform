import sys
import os

sys.path.append(
    os.path.abspath(
        os.path.join(os.path.dirname(__file__), "..")
    )
)

from app.database.db import SessionLocal
from app.models.company import Company
from app.data.nifty100 import NIFTY_100_STOCKS

db = SessionLocal()

inserted = 0

for symbol in NIFTY_100_STOCKS:

    existing = (
        db.query(Company)
        .filter(Company.symbol == symbol)
        .first()
    )

    if existing:
        continue

    company = Company(
    symbol=symbol,
    company_name=symbol.replace(".NS", ""),
    sector="Unknown",
    market_cap=0
)

    db.add(company)
    inserted += 1

db.commit()

print(f"Inserted {inserted} companies")