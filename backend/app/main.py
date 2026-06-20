from fastapi import FastAPI

from app.database.db import SessionLocal

from app.services.backtest_service import (
    run_strategy,
    calculate_returns
)

app = FastAPI()


@app.get("/")
def home():
    return {
        "message": "Backtesting Platform API Running"
    }

# Backtest
@app.get("/backtest")
def backtest(
    min_roce: float = 15,
    min_roe: float = 15,
    max_pe: float = 25
):
    db = SessionLocal()

    try:
        result = run_strategy(
            db,
            min_roce,
            min_roe,
            max_pe
        )

        return {
            "selected_stocks": result
        }

    finally:
        db.close()

# Portfolio
@app.get("/portfolio")
def portfolio(
    start_date: str = "2020-01-01",
    end_date: str = "2025-01-01",
    capital: float = 100000,
    min_roce: float = 15,
    min_roe: float = 15,
    max_pe: float = 25
):

    db = SessionLocal()

    try:

        results = calculate_returns(
            db,
            min_roce,
            min_roe,
            max_pe,
            start_date,
            end_date,
            capital
        )

        return {
            "portfolio": results
        }

    finally:
        db.close()