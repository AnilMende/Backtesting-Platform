import {
    LineChart,
    Line,
    XAxis,
    YAxis,
    CartesianGrid,
    Tooltip,
    ResponsiveContainer
} from "recharts";

const PortfolioChart = ({ history }) => {

    if (!history || history.length === 0) {
        return null;
    }

    const chartData = history.map(item => ({
        date: item.rebalance_date,
        value: item.portfolio_value
    }));

    return (
        <div className="bg-white rounded-lg shadow mt-8 p-6">

            <h2 className="text-xl font-semibold mb-4">
                Portfolio Growth
            </h2>

            <div className="h-96">

                <ResponsiveContainer
                    width="100%"
                    height="100%"
                >

                    <LineChart data={chartData}>

                        <CartesianGrid strokeDasharray="3 3" />

                        <XAxis dataKey="date" />

                        <YAxis
                            tickFormatter={(value) =>
                                `₹${(value / 1000).toFixed(0)}K`
                            }
                        />

                        <Tooltip
                            formatter={(value) =>
                                `₹${Number(value).toLocaleString()}`
                            }
                        />

                        <Line
                            type="monotone"
                            dataKey="value"
                            strokeWidth={3}
                        />

                    </LineChart>

                </ResponsiveContainer>

            </div>

        </div>
    );
};

export default PortfolioChart;