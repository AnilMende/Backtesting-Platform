

const RebalanceHistory = ({ history }) => {

    if(!history || history.length === 0){
        return null;
    }

    return (
        <div className="bg-white rounded-lg shadow mt-8">

            <div className="p-4 border-b">
                <h2 className="text-xl font-semibold">
                    Rebalance History
                </h2>
            </div>

            <div className="overflow-x-auto">

                <table className="w-full">

                    <thead className="bg-slate-100">

                        <tr>
                            <th className="p-3 text-left">
                                Rebalance Date
                            </th>

                            <th className="p-3 text-left">
                                Portfolio Value
                            </th>

                            <th className="p-3 text-left">
                                Selected Stocks
                            </th>
                        </tr>

                    </thead>

                    <tbody>

                        {history.map((item, index) => (
                            <tr
                                key={index}
                                className="border-t"
                            >
                                <td className="p-3">
                                    {item.rebalance_date}
                                </td>

                                <td className="p-3">
                                    ₹
                                    {Number(
                                        item.portfolio_value
                                    ).toLocaleString()}
                                </td>

                                <td className="p-3">

                                    <div className="flex flex-wrap gap-2">

                                        {item.selected_stocks?.map(
                                            (stock) => (
                                                <span
                                                    key={stock}
                                                    className="
                            bg-blue-100
                            text-blue-700
                            px-2
                            py-1
                            rounded-md
                            text-sm
                          "
                                                >
                                                    {stock}
                                                </span>
                                            )
                                        )}

                                    </div>

                                </td>
                            </tr>
                        ))}

                    </tbody>

                </table>

            </div>

        </div>
    )
}

export default RebalanceHistory;