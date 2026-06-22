import { useState } from "react";
import StrategyFrom from "../components/StrategyForm.jsx";
import PortfolioSummary from "../components/PortfolioSummary.jsx";
import PortfolioTable from "../components/PortfolioTable.jsx";
import RebalanceHistory from "../components/RebalanceHistory.jsx";
import PortfolioChart from "../components/PortfolioChart.jsx";
import WinnersLosers from "../components/WinnersLosers.jsx";
import DrawdownChart from "../components/DrawDownChart.jsx";
import ExportButtons from "../components/ExportButtons.jsx";


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

                            <PortfolioChart
                                history={
                                    portfolioData.portfolio.rebalance_history
                                }
                            />

                            <DrawdownChart
                                history={
                                    portfolioData.portfolio.drawdown_history
                                }
                            />

                            <WinnersLosers
                                winners={
                                    portfolioData.portfolio.top_winners
                                }
                                losers={
                                    portfolioData.portfolio.top_losers
                                }
                            />

                            <ExportButtons
                                stocks={
                                    portfolioData.portfolio.stocks
                                }
                            />

                            <PortfolioTable
                                stocks={portfolioData.portfolio.stocks}
                            />

                            <RebalanceHistory
                                history={portfolioData.portfolio.rebalance_history}
                            />
                        </>
                    )
                }

            </div>
        </div>
    )
}

export default DashboardPage;