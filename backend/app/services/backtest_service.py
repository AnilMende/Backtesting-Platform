from datetime import datetime, date, timedelta
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
    ranking_metric: str,
    min_market_cap: float = 0,
    max_market_cap: float = 999999999999999999,
    min_pat: float = 0
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
            Fundamental.pe <= max_pe,
            Fundamental.pat >= min_pat,
            Company.market_cap >= min_market_cap,
            Company.market_cap <= max_market_cap
        )
    )

    if ranking_metric.lower() == "composite":
        
        stocks = results.all()
        
        stocks = apply_composite_ranking(
            stocks
        )
        
        stocks = stocks[:portfolio_size]
        
        return [
            {
                "symbol": stock.symbol,
                "roce": stock.roce,
                "roe": stock.roe,
                "pe": stock.pe
            }
            for stock in stocks
        ]
    
    if ranking_metric.lower() == "roe":
        results = results.order_by(
            Fundamental.roe.desc()
        )
        
    elif ranking_metric.lower() == "roce":
        results = results.order_by(
            Fundamental.roce.desc()
        )
        
    elif ranking_metric.lower() == "pe":
        results = results.order_by(
            Fundamental.pe.asc()
        )
        
    else:
        results = results.order_by(
            Fundamental.roe.desc()
        )
        
    results = results.limit(portfolio_size)
    
    results = results.all()

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
    start_date: str,
    end_date: str,
    capital: float,
    portfolio_size: int,
    ranking_metric: str,
    rebalance_frequency: str = "yearly",
    position_sizing: str = "equal"
):

    start_date = datetime.strptime(
        start_date,
        "%Y-%m-%d"
    ).date()

    end_date = datetime.strptime(
        end_date,
        "%Y-%m-%d"
    ).date()

    # Generate rebalance dates

    rebalance_dates = []

    current_date = start_date

    if rebalance_frequency.lower() == "monthly":
        
        while current_date < end_date:
            
            rebalance_dates.append(current_date)
            
            if current_date.month == 12:
                
                current_date = date(
                    current_date.year + 1,
                    1,
                    1
                )
                
            else:
                
                current_date = date(
                    current_date.year,
                    current_date.month + 1,
                    1
                )
                
    elif rebalance_frequency.lower() == "quarterly":
        
        while current_date < end_date:
            
            rebalance_dates.append(current_date)
            
            next_month = current_date.month + 3
            
            year = current_date.year
            
            if next_month > 12:
                
                next_month -= 12
                year += 1
                
            current_date = date(
                year,
                next_month,
                1
            )

    else:
        
        while current_date < end_date:
            
            rebalance_dates.append(current_date)
            current_date = date(
                current_date.year + 1,
                1,
                1
            )

    

    if rebalance_dates[-1] != end_date:
        rebalance_dates.append(end_date)

    rebalance_history = []

    all_results = []

    current_capital = capital

    # Rebalance loop

    for i in range(len(rebalance_dates) - 1):

        period_start = rebalance_dates[i]

        period_end = rebalance_dates[i + 1]

        yearly_results = []

        selected = (
            db.query(
                Company.id,
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
        )

        # Ranking

        if ranking_metric.lower() == "roe":

            selected = selected.order_by(
                Fundamental.roe.desc()
            )

        elif ranking_metric.lower() == "roce":

            selected = selected.order_by(
                Fundamental.roce.desc()
            )

        elif ranking_metric.lower() == "pe":

            selected = selected.order_by(
                Fundamental.pe.asc()
            )

        else:

            selected = selected.order_by(
                Fundamental.roe.desc()
            )

        selected = selected.limit(
            portfolio_size
        )

        selected = selected.all()

        allocations = {}

        if position_sizing.lower() == "equal":
            allocation_per_stock = (
                current_capital / len(selected)
            )
            
            for stock in selected:
                
                allocations[stock.symbol] = (
                    allocation_per_stock
                )
        
        elif position_sizing.lower() == "market_cap":
            
            total_market_cap = sum(
                db.query(Company)
                .filter(Company.id == stock.id)
                .first()
                .market_cap
                for stock in selected
            )
            
            for stock in selected:
                
                company = (
                    db.query(Company)
                    .filter(
                        Company.id == stock.id
                    )
                    .first()
                )
                
                weight = (
                    company.market_cap
                    / total_market_cap
                )
                
                allocations[stock.symbol] = (
                    current_capital * weight
                )

        elif position_sizing.lower() == "roce":
            
            total_roce = sum(
                stock.roce
                for stock in selected
            )
            
            for stock in selected:
                
                weight = (
                    stock.roce
                    / total_roce
                )
                
                allocations[stock.symbol] = (
                    current_capital * weight
                )

        if len(selected) == 0:
            continue


        for stock in selected:

            first_price = (
                db.query(StockPrice)
                .filter(
                    StockPrice.company_id == stock.id,
                    StockPrice.trade_date >= period_start
                )
                .order_by(
                    StockPrice.trade_date.asc()
                )
                .first()
            )

            last_price = (
                db.query(StockPrice)
                .filter(
                    StockPrice.company_id == stock.id,
                    StockPrice.trade_date <= period_end
                )
                .order_by(
                    StockPrice.trade_date.desc()
                )
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

            allocated_capital = (
                allocations[stock.symbol]
            )
            
            final_value = allocated_capital * (
                1 + (return_pct / 100)
            )

            yearly_results.append({
                "symbol": stock.symbol,
                "period_start": str(period_start),
                "period_end": str(period_end),
                "start_price": round(
                    first_price.close_price,
                    2
                ),
                "end_price": round(
                    last_price.close_price,
                    2
                ),
                "return_pct": round(
                    return_pct,
                    2
                ),
                "allocated_capital": round(
                    allocated_capital,
                    2
                )
                ,
                "final_value": round(
                    final_value,
                    2
                )
            })

        period_value = sum(
            stock["final_value"]
            for stock in yearly_results
        )

        current_capital = period_value

        rebalance_history.append({
            "rebalance_date": str(period_start),
            "portfolio_value": round(
                current_capital,
                2
            ),
            "selected_stocks": [
                stock["symbol"]
                for stock in yearly_results
            ]
        })

        all_results.extend(
            yearly_results
        )

    total_final_value = current_capital

    portfolio_return_pct = (
        (
            total_final_value - capital
        )
        / capital
    ) * 100

    years = (
        end_date - start_date
    ).days / 365.25

    cagr = (
        (
            total_final_value / capital
        ) ** (1 / years)
        - 1
    ) * 100

    return {
        "portfolio_size": portfolio_size,
        "initial_capital": capital,
        "final_portfolio_value": round(
            total_final_value,
            2
        ),
        "portfolio_return_pct": round(
            portfolio_return_pct,
            2
        ),
        "cagr": round(
            cagr,
            2
        ),
        "rebalance_history": rebalance_history,
        "stocks": all_results
    }


def apply_composite_ranking(stocks):
    
    roe_sorted = sorted(
        stocks,
        key=lambda x: x.roe,
        reverse=True
    )

    roce_sorted = sorted(
        stocks,
        key=lambda x: x.roce,
        reverse=True
    )

    pe_sorted = sorted(
        stocks,
        key=lambda x: x.pe
    )

    roe_rank = {
        stock.symbol: rank + 1
        for rank, stock in enumerate(roe_sorted)
    }

    roce_rank = {
        stock.symbol: rank + 1
        for rank, stock in enumerate(roce_sorted)
    }

    pe_rank = {
        stock.symbol: rank + 1
        for rank, stock in enumerate(pe_sorted)
    }

    ranked_stocks = []

    for stock in stocks:

        composite_score = (
            roe_rank[stock.symbol]
            + roce_rank[stock.symbol]
            + pe_rank[stock.symbol]
        ) / 3

        ranked_stocks.append({
            "stock": stock,
            "score": composite_score
        })

    ranked_stocks.sort(
        key=lambda x: x["score"]
    )

    return [
        item["stock"]
        for item in ranked_stocks
    ]