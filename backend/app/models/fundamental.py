from sqlalchemy import (
    Column,
    Integer,
    Float,
    BigInteger,
    ForeignKey
)

from app.database.base import Base


class Fundamental(Base):
    __tablename__ = "fundamentals"

    id = Column(Integer, primary_key=True)

    company_id = Column(
        Integer,
        ForeignKey("companies.id")
    )

    fiscal_year = Column(Integer)

    roce = Column(Float)

    roe = Column(Float)

    pe = Column(Float)

    pat = Column(BigInteger)

    revenue = Column(BigInteger)