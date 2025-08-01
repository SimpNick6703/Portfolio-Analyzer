// frontend/src/components/StatCard.js
import React from 'react';

function StatCard({ title, value, subtext }) {
  return (
    <div className="bg-light-content dark:bg-dark-content p-4 rounded-lg shadow-md flex-1">
      <h3 className="text-sm font-medium text-light-text dark:text-dark-text">{title}</h3>
      <p className="text-2xl font-bold text-light-text-strong dark:text-dark-text-strong mt-1">{value}</p>
      {subtext && <p className="text-xs text-gray-500 dark:text-gray-400 mt-1">{subtext}</p>}
    </div>
  );
}

export default StatCard;