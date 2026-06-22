import { useState } from "react";
import StrategyFrom from "../components/StrategyForm.jsx";
import PortfolioSummary from "../components/PortfolioSummary.jsx";
import PortfolioTable from "../components/PortfolioTable.jsx";


const DashboardPage = () => {

    const [portfolioData, setPortfolioData] = useState(null);

    return (
        <div className="min-h-screen bg-slate-100 p-6">
            <div className="max-w-7xl mx-auto">

                <h1 className="text-4xl font-bold text-center mb-8">
                    Stock Backtesting Platform
                </h1>

                <StrategyFrom
                    setPortfolioData={setPortfolioData}
                />

                {
                    portfolioData && (
                        <>
                            <PortfolioSummary
                                portfolio={portfolioData.portfolio}
                            />

                            <PortfolioTable
                                stocks={portfolioData.portfolio.stocks}
                            />
                        </>
                    )
                }

            </div>
        </div>
    )
}

export default DashboardPage;