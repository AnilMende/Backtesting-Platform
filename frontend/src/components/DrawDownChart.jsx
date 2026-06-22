
import {
  LineChart,
  Line,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  ResponsiveContainer
} from "recharts";

const DrawdownChart = ({ history }) => {

  if (!history || history.length === 0) {
    return null;
  }

  return (
    <div className="bg-white rounded-lg shadow mt-8 p-6">

      <h2 className="text-xl font-semibold mb-4">
        Drawdown Chart
      </h2>

      <div className="h-96">

        <ResponsiveContainer
          width="100%"
          height="100%"
        >

          <LineChart data={history}>

            <CartesianGrid
              strokeDasharray="3 3"
            />

            <XAxis dataKey="date" />

            <YAxis
              tickFormatter={
                (value) => `${value}%`
              }
            />

            <Tooltip
              formatter={
                (value) => `${value}%`
              }
            />

            <Line
              type="monotone"
              dataKey="drawdown"
              stroke="#ef4444"
              strokeWidth={3}
              dot={false}
            />

          </LineChart>

        </ResponsiveContainer>

      </div>

    </div>
  );
};

export default DrawdownChart;