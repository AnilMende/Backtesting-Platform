# Backtesting Platform

A full-stack stock portfolio backtesting platform that allows users to create rule-based investment strategies, simulate historical performance, analyze portfolio returns, and evaluate risk metrics through an interactive dashboard.

---

## Features

### Strategy Configuration

* Filter stocks using:

  * ROCE
  * ROE
  * PE Ratio
  * PAT
  * Market Capitalization
* Select portfolio size
* Choose ranking metric:

  * ROE
  * ROCE
  * PE
  * Composite Ranking

### Portfolio Construction

* Equal Weight Allocation
* Market Cap Weighted Allocation
* ROCE Weighted Allocation

### Backtesting Engine

* Historical stock price analysis
* Portfolio rebalancing:

  * Monthly
  * Quarterly
  * Yearly
* Configurable date ranges
* Capital allocation simulation

### Performance Analytics

* Portfolio Return %
* CAGR
* Sharpe Ratio
* Maximum Drawdown
* Equity Curve
* Drawdown Chart
* Top Winners and Losers

### Reporting

* Portfolio Holdings Table
* Rebalance History Table
* CSV Export
* Excel Export

---

## Tech Stack

### Frontend

* React.js
* Tailwind CSS
* Axios
* Recharts
* XLSX
* File Saver

### Backend

* FastAPI
* SQLAlchemy
* Pydantic

### Database

* MySQL

### Market Data

* Yahoo Finance (yfinance)

---

## Project Architecture

```text
Backtesting Platform
│
├── frontend
│   │
│   ├── components
│   │   ├── StrategyForm
│   │   ├── SummaryCards
│   │   ├── PortfolioTable
│   │   ├── RebalanceHistory
│   │   ├── PortfolioChart
│   │   ├── DrawdownChart
│   │   ├── WinnersLosers
│   │   └── ExportButtons
│   │
│   ├── pages
│   │   └── DashboardPage
│   │
│   └── services
│       └── portfolioApi
│
├── backend
│   │
│   ├── app
│   │   ├── models
│   │   ├── services
│   │   ├── database
│   │   └── main.py
│   │
│   └── scripts
│       ├── load_companies.py
│       ├── load_fundamentals.py
│       └── fetch_data.py
│
└── mysql
```

---

## Database Schema

### Companies

| Column       | Type       |
| ------------ | ---------- |
| id           | Integer    |
| symbol       | String     |
| company_name | String     |
| sector       | String     |
| market_cap   | BigInteger |

### Fundamentals

| Column      | Type    |
| ----------- | ------- |
| id          | Integer |
| company_id  | Integer |
| fiscal_year | Integer |
| roce        | Float   |
| roe         | Float   |
| pe          | Float   |
| pat         | Float   |
| revenue     | Float   |

### Stock Prices

| Column      | Type    |
| ----------- | ------- |
| id          | Integer |
| company_id  | Integer |
| trade_date  | Date    |
| open_price  | Float   |
| high_price  | Float   |
| low_price   | Float   |
| close_price | Float   |
| volume      | Float   |

---

# Backend Setup

## 1. Clone Repository

```bash
git clone https://github.com/AnilMende/Backtesting-Platform
cd backend
```

## 2. Create Virtual Environment

```bash
python -m venv venv
```

Activate:

### Windows

```bash
venv\Scripts\activate
```

### Linux / Mac

```bash
source venv/bin/activate
```

---

## 3. Install Dependencies

```bash
pip install -r requirements.txt
```

---

## 4. Configure Environment Variables

Create a `.env` file:

```env
DATABASE_URL=mysql+pymysql://username:password@localhost/backtesting_db
```

---

## 5. Create Database

```sql
CREATE DATABASE backtesting_db;
```

---

## 6. Create Tables

```bash
python
```

```python
from app.database.base import Base
from app.database.db import engine

Base.metadata.create_all(bind=engine)
```

---

## 7. Load Company Data

```bash
python scripts/load_companies.py
```

---

## 8. Load Fundamentals

```bash
python scripts/load_fundamentals.py
```

---

## 9. Load Historical Stock Prices

```bash
python scripts/fetch_data.py
```

---

## 10. Run Backend

```bash
uvicorn app.main:app --reload
```

Backend URL:

```text
http://127.0.0.1:8000
```

Swagger Docs:

```text
http://127.0.0.1:8000/docs
```

---

# Frontend Setup

## 1. Navigate to Frontend

```bash
cd frontend
```

---

## 2. Install Dependencies

```bash
npm install
```

---

## 3. Start Frontend

```bash
npm run dev
```

Frontend URL:

```text
http://localhost:5173
```

---

# API Example

## Run Backtest

```http
GET /portfolio
```

Example:

```http
/portfolio?
min_roce=15&
min_roe=15&
max_pe=25&
portfolio_size=10&
ranking_metric=roe&
position_sizing=equal&
rebalance_frequency=yearly&
start_date=2020-01-01&
end_date=2025-01-01
```

---

# Sample Output

```json
{
  "portfolio_size": 10,
  "initial_capital": 100000,
  "final_portfolio_value": 252485.84,
  "portfolio_return_pct": 152.49,
  "cagr": 20.35,
  "sharpe_ratio": 1.42,
  "max_drawdown": 0,
  "stocks": [...]
}
```

---

# Future Enhancements

* Real-time market data integration
* User authentication
* Portfolio persistence
* Benchmark comparison
* Transaction cost modelling
* Advanced factor ranking
* Cloud deployment

---

# Author

Anil Kumar

B.Tech Artificial Intelligence & Data Science

Full Stack & AI Developer
