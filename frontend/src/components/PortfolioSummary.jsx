
const PortfolioSummary = ({ portfolio }) => {

    if (!portfolio) return null;

    return (
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-5 gap-4 mt-8">

            <div className="bg-white p-4 rounded-lg shadow">
                <h3 className="font-semibold">Portfolio Size</h3>
                <p>{portfolio.portfolio_size}</p>
            </div>

            <div className="bg-white p-4 rounded-lg shadow">
                <h3 className="font-semibold">Initial Capital</h3>
                <p>₹{portfolio.initial_capital}</p>
            </div>

            <div className="bg-white p-4 rounded-lg shadow">
                <h3 className="font-semibold">Final Value</h3>
                <p>₹{portfolio.final_portfolio_value}</p>
            </div>

            <div className="bg-white p-4 rounded-lg shadow">
                <h3 className="font-semibold">Return %</h3>
                <p>{portfolio.portfolio_return_pct}%</p>
            </div>

            <div className="bg-white p-4 rounded-lg shadow">
                <h3 className="font-semibold">CAGR</h3>
                <p>{portfolio.cagr}%</p>
            </div>

            <div className="bg-white p-4 rounded-lg shadow">
                <h3 className="font-semibold">Sharpe Ratio</h3>
                <p>{portfolio.sharpe_ratio}</p>
            </div>

            <div className="bg-white p-4 rounded-lg shadow">
                <h3 className="font-semibold">Max DrawDown</h3>
                <p>{portfolio.max_drawdown}</p>
            </div>

        </div>
    );
};

export default PortfolioSummary;