CREATE DATABASE backtesting_platform;

CREATE TABLE companies (
    id INT PRIMARY KEY AUTO_INCREMENT,
    symbol VARCHAR(20) UNIQUE NOT NULL,
    company_name VARCHAR(255),
    sector VARCHAR(100),
    market_cap BIGINT,

    INDEX idx_symbol(symbol)
);


CREATE TABLE stock_prices (
    id BIGINT PRIMARY KEY AUTO_INCREMENT,

    company_id INT NOT NULL,

    trade_date DATE NOT NULL,

    open_price DECIMAL(12,2),
    high_price DECIMAL(12,2),
    low_price DECIMAL(12,2),
    close_price DECIMAL(12,2),

    volume BIGINT,

    FOREIGN KEY (company_id)
        REFERENCES companies(id),

    INDEX idx_company_date(company_id, trade_date)
);

SELECT *
FROM stock_prices
WHERE company_id = ?
AND trade_date BETWEEN ? AND ?;

CREATE TABLE fundamentals (
    id BIGINT PRIMARY KEY AUTO_INCREMENT,

    company_id INT NOT NULL,

    fiscal_year YEAR NOT NULL,

    roce DECIMAL(10,2),
    roe DECIMAL(10,2),
    pe DECIMAL(10,2),

    pat BIGINT,
    revenue BIGINT,

    FOREIGN KEY(company_id)
        REFERENCES companies(id),

    INDEX idx_company_year(company_id, fiscal_year)
);
