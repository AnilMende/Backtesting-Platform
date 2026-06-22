
const PortfolioTable = ({ stocks }) => {

    if (!stocks || stocks.length === 0) return null;

    return (
        <div className="bg-white rounded-lg shadow mt-8 overflow-x-auto">

            <table className="w-full">

                <thead className="bg-slate-200">

                    <tr>
                        <th className="p-3">Symbol</th>
                        <th className="p-3">Start Price</th>
                        <th className="p-3">End Price</th>
                        <th className="p-3">Return %</th>
                        <th className="p-3">Allocated Capital</th>
                        <th className="p-3">Final Value</th>
                    </tr>

                </thead>

                <tbody>

                    {stocks.map((stock, index) => (
                        <tr key={index} className="border-t">

                            <td className="p-3">{stock.symbol}</td>

                            <td className="p-3">
                                ₹{stock.start_price}
                            </td>

                            <td className="p-3">
                                ₹{stock.end_price}
                            </td>

                            <td className="p-3">
                                {stock.return_pct}%
                            </td>

                            <td className="p-3">
                                ₹{stock.allocated_capital}
                            </td>

                            <td className="p-3">
                                ₹{stock.final_value}
                            </td>

                        </tr>
                    ))}

                </tbody>

            </table>

        </div>
    );
};

export default PortfolioTable;