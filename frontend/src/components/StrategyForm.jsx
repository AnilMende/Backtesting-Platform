import { useState } from "react";
import { runBacktest } from "../api/portfolioApi.js";


const StrategyFrom = ({ setPortfolioData }) => {

    const [loading, setLoading] = useState(false);

    const [formData, setFormData] = useState({
        min_roce: 15,
        min_roe: 15,
        max_pe: 25,
        min_pat: 0,
        min_market_cap: 0,

        portfolio_size: 10,
        capital: 100000,

        ranking_metric: "roe",
        position_sizing: "equal",
        rebalance_frequency: "yearly",

        start_date: "2020-01-01",
        end_date: "2025-01-01",
    })

    const handleChange = (e) => {
        setFormData({
            ...formData,
            [e.target.name]: e.target.value
        }
        );
    }

    const handleSubmit = async (e) => {
        e.preventDefault();

        try {

            setLoading(true);

            const data = await runBacktest(formData);

            console.log(data);

            setPortfolioData(data);

        } catch (error) {

            // console.error(error);

            // setLoading(false);

            return (
                <div className="bg-red-100 text-red-700 p-4 rounded">
                    Failed to run backtest
                </div>
            )
            
        } finally {
            setLoading(false);
        }
    }

    return (
        <form
            onSubmit={handleSubmit}
            className="bg-white rounded-xl shadow-lg p-8"
        >
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">

                {/* ROCE */}
                <div>
                    <label className="block mb-2 font-medium">
                        Minimum ROCE
                    </label>

                    <input
                        type="number"
                        name="min_roce"
                        value={formData.min_roce}
                        onChange={handleChange}
                        className="w-full border rounded-lg px-3 py-2"
                    />
                </div>

                {/* ROE */}
                <div>
                    <label className="block mb-2 font-medium">
                        Minimum ROE
                    </label>

                    <input
                        type="number"
                        name="min_roe"
                        value={formData.min_roe}
                        onChange={handleChange}
                        className="w-full border rounded-lg px-3 py-2"
                    />
                </div>

                {/* PE */}
                <div>
                    <label className="block mb-2 font-medium">
                        Maximum PE
                    </label>

                    <input
                        type="number"
                        name="max_pe"
                        value={formData.max_pe}
                        onChange={handleChange}
                        className="w-full border rounded-lg px-3 py-2"
                    />
                </div>

                {/* PAT */}
                <div>
                    <label className="block mb-2 font-medium">
                        Minimum PAT
                    </label>

                    <input
                        type="number"
                        name="min_pat"
                        value={formData.min_pat}
                        onChange={handleChange}
                        className="w-full border rounded-lg px-3 py-2"
                    />
                </div>

                {/* Market Cap */}
                <div>
                    <label className="block mb-2 font-medium">
                        Minimum Market Cap
                    </label>

                    <input
                        type="number"
                        name="min_market_cap"
                        value={formData.min_market_cap}
                        onChange={handleChange}
                        className="w-full border rounded-lg px-3 py-2"
                    />
                </div>

                {/* Portfolio Size */}
                <div>
                    <label className="block mb-2 font-medium">
                        Portfolio Size
                    </label>

                    <input
                        type="number"
                        name="portfolio_size"
                        value={formData.portfolio_size}
                        onChange={handleChange}
                        className="w-full border rounded-lg px-3 py-2"
                    />
                </div>

                {/* Capital */}
                <div>
                    <label className="block mb-2 font-medium">
                        Initial Capital
                    </label>

                    <input
                        type="number"
                        name="capital"
                        value={formData.capital}
                        onChange={handleChange}
                        className="w-full border rounded-lg px-3 py-2"
                    />
                </div>

                {/* Ranking */}
                <div>
                    <label className="block mb-2 font-medium">
                        Ranking Metric
                    </label>

                    <select
                        name="ranking_metric"
                        value={formData.ranking_metric}
                        onChange={handleChange}
                        className="w-full border rounded-lg px-3 py-2"
                    >
                        <option value="roe">ROE</option>
                        <option value="roce">ROCE</option>
                        <option value="pe">PE</option>
                        <option value="composite">Composite</option>
                    </select>
                </div>

                {/* Position Sizing */}
                <div>
                    <label className="block mb-2 font-medium">
                        Position Sizing
                    </label>

                    <select
                        name="position_sizing"
                        value={formData.position_sizing}
                        onChange={handleChange}
                        className="w-full border rounded-lg px-3 py-2"
                    >
                        <option value="equal">Equal Weight</option>
                        <option value="market_cap">Market Cap</option>
                        <option value="roce">ROCE Weight</option>
                    </select>
                </div>

                {/* Rebalance */}
                <div>
                    <label className="block mb-2 font-medium">
                        Rebalance Frequency
                    </label>

                    <select
                        name="rebalance_frequency"
                        value={formData.rebalance_frequency}
                        onChange={handleChange}
                        className="w-full border rounded-lg px-3 py-2"
                    >
                        <option value="yearly">Yearly</option>
                        <option value="quarterly">Quarterly</option>
                        <option value="monthly">Monthly</option>
                    </select>
                </div>

                {/* Start Date */}
                <div>
                    <label className="block mb-2 font-medium">
                        Start Date
                    </label>

                    <input
                        type="date"
                        name="start_date"
                        value={formData.start_date}
                        onChange={handleChange}
                        className="w-full border rounded-lg px-3 py-2"
                    />
                </div>

                {/* End Date */}
                <div>
                    <label className="block mb-2 font-medium">
                        End Date
                    </label>

                    <input
                        type="date"
                        name="end_date"
                        value={formData.end_date}
                        onChange={handleChange}
                        className="w-full border rounded-lg px-3 py-2"
                    />
                </div>

            </div>

            <div className="mt-8 flex justify-center">
                <button
                    type="submit"
                    className="bg-blue-600 text-white px-8 py-3 rounded-lg hover:bg-blue-700"
                    disabled={loading}
                >
                    {loading ? "Running" : "Run Backtest"}

                </button>
            </div>
        </form>
    )
}

export default StrategyFrom;