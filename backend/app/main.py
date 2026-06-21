from fastapi import FastAPI
from fastapi import FastAPI, Query, HTTPException
from datetime import datetime

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
    min_roce: float = Query(15, ge=0),
    min_roe: float = Query(15, ge=0),
    max_pe: float = Query(25, gt=0),
    portfolio_size: int = Query(10, ge=1, le=50),
    ranking_metric: str = Query("roe"),
    min_market_cap: float = Query(0, ge=0),
    max_market_cap: float = Query(
        999999999999999999,
        ge=0
    ),
    min_pat: float = Query(0, ge=0)
):
    allowed_metrics = [
        "roe",
        "roce",
        "pe",
        "composite"
    ]
    
    if ranking_metric.lower() not in allowed_metrics:
        raise HTTPException(
            status_code=400,
            detail=(
                "ranking_metric must be one of: "
                "roe, roce, pe, composite"
            )
        )
    
    db = SessionLocal()

    try:
        result = run_strategy(
            db,
            min_roce,
            min_roe,
            max_pe,
            portfolio_size,
            ranking_metric,
            min_market_cap,
            max_market_cap,
            min_pat
        )

        return {
            "selected_stocks": result
        }

    finally:
        db.close()

# Portfolio
@app.get("/portfolio")
def portfolio(
    min_roce: float = Query(15, ge=0),
    min_roe: float = Query(15, ge=0),
    max_pe: float = Query(25, gt=0),

    start_date: str = "2020-01-01",
    end_date: str = "2025-12-31",

    capital: float = Query(
        100000,
        gt=0
    ),

    portfolio_size: int = Query(
        10,
        ge=1,
        le=50
    ),

    ranking_metric: str = "roe",

    rebalance_frequency: str = "yearly",

    position_sizing: str = "equal"
):

    db = SessionLocal()
    
    try:
        start = datetime.strptime(
            start_date,
            "%Y-%m-%d"
        )
        
        end = datetime.strptime(
            end_date,
            "%Y-%m-%d"
        )
        
    except ValueError:
        raise HTTPException(
            status_code=400,
            detail=(
                "Dates must be in "
                "YYYY-MM-DD format"
            )
        )
    
    if start >= end:
        raise HTTPException(
            status_code=400,
            detail=(
                "end_date must be after "
                "start_date"
            )
        )
    
    allowed_frequencies = [
        "monthly",
        "quarterly",
        "yearly"
    ]
    
    if (
        rebalance_frequency.lower()
        not in allowed_frequencies
    ):
        raise HTTPException(
            status_code=400,
            detail=(
                "rebalance_frequency must be "
                "monthly, quarterly or yearly"
            )
        )
    
    allowed_position_sizing = [
        "equal",
        "market_cap",
        "roce"
    ]
    
    if (
        position_sizing.lower()
        not in allowed_position_sizing
    ):
        raise HTTPException(
            status_code=400,
            detail=(
                "position_sizing must be "
                "equal, market_cap or roce"
            )
        )

    try:

        results = calculate_returns(
            db,
            min_roce,
            min_roe,
            max_pe,
            start_date,
            end_date,
            capital,
            portfolio_size,
            ranking_metric,
            rebalance_frequency,
            position_sizing
        )

        return {
            "portfolio": results
        }
    
    except Exception as e:
        
        raise HTTPException(
            status_code=500,
            detail=str(e)
        )

    finally:
        db.close()