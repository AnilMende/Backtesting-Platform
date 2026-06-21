import sys
import os
import random

sys.path.append(
    os.path.abspath(
        os.path.join(os.path.dirname(__file__), "..")
    )
)

from app.database.db import SessionLocal
from app.models.company import Company
from app.models.fundamental import Fundamental

db = SessionLocal()

companies = db.query(Company).all()

inserted = 0

for company in companies:

    existing = (
        db.query(Fundamental)
        .filter(
            Fundamental.company_id == company.id
        )
        .first()
    )

    if existing:
        continue

    fundamental = Fundamental(
        company_id=company.id,
        fiscal_year=2025,
        roce=random.randint(10, 50),
        roe=random.randint(10, 40),
        pe=random.randint(10, 40),
        pat=random.randint(5000, 100000),
        revenue=random.randint(50000, 1000000)
    )

    db.add(fundamental)

    inserted += 1

db.commit()

print(f"Inserted {inserted} fundamentals")