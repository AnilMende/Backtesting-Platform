from sqlalchemy import Column, Integer, String, BigInteger

from app.database.base import Base

class Company(Base):
    __tablename__ = "companies"

    id = Column(Integer, primary_key=True, index=True)

    symbol = Column(
        String(50),
        unique=True,
        nullable=False
    )

    company_name = Column(
        String(255)
    )

    sector = Column(
        String(255)
    )

    market_cap = Column(
        BigInteger
    )