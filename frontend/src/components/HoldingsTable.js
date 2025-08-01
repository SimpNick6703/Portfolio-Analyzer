// frontend/src/components/HoldingsTable.js
import React from 'react';

function HoldingsTable({ holdings, onRowClick }) {
  if (!holdings || holdings.length === 0) {
    return (
      <div className="bg-light-content dark:bg-dark-content p-4 rounded-lg shadow-md mt-6">
        <p>Loading holdings...</p>
      </div>
    );
  }

  // Helper to format numbers with commas
  const formatNumber = (num) => {
    if (num === null || num === undefined) return 'N/A';
    return num.toLocaleString(undefined, { minimumFractionDigits: 2, maximumFractionDigits: 2 });
  }

  return (
    <div className="bg-light-content dark:bg-dark-content rounded-lg shadow-md mt-6 overflow-x-auto">
      <table className="w-full text-sm text-left">
        <thead className="text-xs uppercase bg-light-base dark:bg-dark-base">
          <tr>
            <th scope="col" className="px-6 py-3">Symbol</th>
            <th scope="col" className="px-6 py-3 text-right">Quantity</th>
            <th scope="col" className="px-6 py-3 text-right">Market Value (USD)</th>
            <th scope="col" className="px-6 py-3 text-right">XIRR (%)</th>
          </tr>
        </thead>
        <tbody>
          {holdings.map((h, index) => (
            <tr
              key={index}
              className="border-b border-light-base dark:border-dark-base hover:bg-light-base dark:hover:bg-dark-base cursor-pointer"
              onClick={() => onRowClick(h.symbol)}
            >
              <td className="px-6 py-4 font-bold text-light-text-strong dark:text-dark-text-strong">{h.symbol}</td>
              <td className="px-6 py-4 text-right">{formatNumber(h.quantity)}</td>
              <td className="px-6 py-4 text-right">${formatNumber(h.market_value)}</td>
              <td className={`px-6 py-4 text-right font-semibold ${h.xirr_percent > 0 ? 'text-green-500' : 'text-red-500'}`}>
                {h.xirr_percent !== null ? `${formatNumber(h.xirr_percent)}%` : 'N/A'}
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}

export default HoldingsTable;