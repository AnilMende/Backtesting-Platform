import sys
import os

sys.path.append(
    os.path.abspath(
        os.path.join(os.path.dirname(__file__), "..")
    )
)

from app.database.db import SessionLocal
from app.models.company import Company
from app.models.fundamental import Fundamental

db = SessionLocal()

sample_data = {
    "RELIANCE.NS": {
        "roce": 18,
        "roe": 16,
        "pe": 22,
        "pat": 79000,
        "revenue": 900000
    },
    "TCS.NS": {
        "roce": 48,
        "roe": 42,
        "pe": 28,
        "pat": 45000,
        "revenue": 230000
    },
    "INFY.NS": {
        "roce": 34,
        "roe": 29,
        "pe": 26,
        "pat": 25000,
        "revenue": 150000
    },
    "HDFCBANK.NS": {
        "roce": 14,
        "roe": 17,
        "pe": 19,
        "pat": 52000,
        "revenue": 280000
    }
}

for symbol, values in sample_data.items():

    company = (
        db.query(Company)
        .filter(Company.symbol == symbol)
        .first()
    )

    if not company:
        continue

    record = Fundamental(
        company_id=company.id,
        fiscal_year=2025,
        roce=values["roce"],
        roe=values["roe"],
        pe=values["pe"],
        pat=values["pat"],
        revenue=values["revenue"]
    )

    db.add(record)

db.commit()

print("Fundamentals Loaded Successfully")