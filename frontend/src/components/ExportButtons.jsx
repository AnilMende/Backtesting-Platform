import { saveAs } from "file-saver";
import * as XLSX from "xlsx";

const ExportButtons = ({ stocks }) => {

  const exportCSV = () => {

    const csvRows = [
      [
        "Symbol",
        "Return %",
        "Allocated Capital",
        "Final Value"
      ],

      ...stocks.map(stock => [
        stock.symbol,
        stock.return_pct,
        stock.allocated_capital,
        stock.final_value
      ])
    ];

    const csvContent = csvRows
      .map(row => row.join(","))
      .join("\n");

    const blob = new Blob(
      [csvContent],
      {
        type: "text/csv;charset=utf-8;"
      }
    );

    saveAs(
      blob,
      "portfolio_results.csv"
    );
  };

  const exportExcel = () => {

    const worksheet =
      XLSX.utils.json_to_sheet(
        stocks
      );

    const workbook =
      XLSX.utils.book_new();

    XLSX.utils.book_append_sheet(
      workbook,
      worksheet,
      "Portfolio"
    );

    XLSX.writeFile(
      workbook,
      "portfolio_results.xlsx"
    );
  };

  return (
    <div className="flex gap-4 mt-6">

      <button
        onClick={exportCSV}
        className="
          px-4 py-2
          bg-green-600
          text-white
          rounded-lg
          hover:bg-green-700
          cursor-pointer
        "
      >
        Export CSV
      </button>

      <button
        onClick={exportExcel}
        className="
          px-4 py-2
          bg-blue-600
          text-white
          rounded-lg
          hover:bg-blue-700
          cursor-pointer
        "
      >
        Export Excel
      </button>

    </div>
  );
};

export default ExportButtons;