
const WinnersLosers = ({
  winners,
  losers
}) => {

  return (
    <div className="grid md:grid-cols-2 gap-6 mt-8">

      {/* Winners */}

      <div className="bg-white rounded-lg shadow p-6">

        <h2 className="text-xl font-semibold text-green-600 mb-4">
          Top Winners
        </h2>

        <div className="space-y-3">

          {winners.map(
            (stock, index) => (
              <div
                key={index}
                className="
                  flex
                  justify-between
                  border-b
                  pb-2
                "
              >
                <span>
                  {stock.symbol}
                </span>

                <span
                  className="
                    text-green-600
                    font-medium
                  "
                >
                  +{stock.return_pct}%
                </span>
              </div>
            )
          )}

        </div>

      </div>

      {/* Losers */}

      <div className="bg-white rounded-lg shadow p-6">

        <h2 className="text-xl font-semibold text-red-600 mb-4">
          Top Losers
        </h2>

        <div className="space-y-3">

          {losers.map(
            (stock, index) => (
              <div
                key={index}
                className="
                  flex
                  justify-between
                  border-b
                  pb-2
                "
              >
                <span>
                  {stock.symbol}
                </span>

                <span
                  className="
                    text-red-600
                    font-medium
                  "
                >
                  {stock.return_pct}%
                </span>
              </div>
            )
          )}

        </div>

      </div>

    </div>
  );
};

export default WinnersLosers;