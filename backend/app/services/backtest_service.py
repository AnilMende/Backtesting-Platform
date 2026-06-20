from datetime import datetime
from sqlalchemy.orm import Session

from app.models.company import Company
from app.models.fundamental import Fundamental
from app.models.stock_price import StockPrice


def run_strategy(
    db: Session,
    min_roce: float,
    min_roe: float,
    max_pe: float,
    portfolio_size : int,
    ranking_metric: str
):
    results = (
        db.query(
            Company.symbol,
            Fundamental.roce,
            Fundamental.roe,
            Fundamental.pe
        )
        .join(
            Fundamental,
            Company.id == Fundamental.company_id
        )
        .filter(
            Fundamental.roce >= min_roce,
            Fundamental.roe >= min_roe,
            Fundamental.pe <= max_pe
        )
        .all()
    )

    return [
        {
            "symbol": row.symbol,
            "roce": row.roce,
            "roe": row.roe,
            "pe": row.pe
        }
        for row in results
    ]


def calculate_returns(
    db: Session,
    min_roce: float,
    min_roe: float,
    max_pe: float,
    start_date : str,
    end_date : str,
    capital : float
):
    start_date = datetime.strptime(
        start_date,
        "%Y-%m-%d").date()
    
    end_date = datetime.strptime(
        end_date,
        "%Y-%m-%d").date()
    
    selected = (
        db.query(
            Company.id,
            Company.symbol
        )
        .join(
            Fundamental,
            Company.id == Fundamental.company_id
        )
        .filter(
            Fundamental.roce >= min_roce,
            Fundamental.roe >= min_roe,
            Fundamental.pe <= max_pe
        )
        .all()
    )

    results = []

    for stock in selected:

        first_price = (
            db.query(StockPrice)
            .filter(
                StockPrice.company_id == stock.id,
                StockPrice.trade_date >= start_date
            )
            .order_by(StockPrice.trade_date.asc())
            .first()
        )

        last_price = (
            db.query(StockPrice)
            .filter(
                StockPrice.company_id == stock.id,
                StockPrice.trade_date <= end_date
            )
            .order_by(StockPrice.trade_date.desc())
            .first()
        )

        if not first_price or not last_price:
            continue

        return_pct = (
            (
                last_price.close_price
                - first_price.close_price
            )
            / first_price.close_price
        ) * 100

        final_value = capital * (
            1 + (return_pct / 100)
        )

        results.append({
            "symbol": stock.symbol,
            "start_price": round(first_price.close_price, 2),
            "end_price": round(last_price.close_price, 2),
            "return_pct": round(return_pct, 2),
            "capital": capital,
            "final_value": round(final_value, 2)
        })

    return results