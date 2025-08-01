// frontend/src/components/Chart.js
import React from 'react';
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer, AreaChart, Area } from 'recharts';
import { format } from 'date-fns';

function PortfolioChart({ data, currency }) {
  if (!data || data.length === 0) {
    return (
      <div className="bg-light-content dark:bg-dark-content p-4 rounded-lg shadow-md h-96 flex items-center justify-center">
        <p>Loading chart data...</p>
      </div>
    );
  }

  // Formatter for the Y-axis (portfolio value)
  const valueFormatter = (value) => {
    if (value >= 1_000_000) return `${(value / 1_000_000).toFixed(1)}M`;
    if (value >= 1_000) return `${(value / 1_000).toFixed(1)}K`;
    return value.toFixed(0);
  };
  
  // Formatter for the tooltip
  const tooltipFormatter = (value, name, props) => {
      return [`${new Intl.NumberFormat('en-US', { style: 'currency', currency: currency }).format(value)}`, "Value"];
  }

  return (
    <div className="bg-light-content dark:bg-dark-content p-4 rounded-lg shadow-md h-96">
      <ResponsiveContainer width="100%" height="100%">
        <AreaChart
          data={data}
          margin={{ top: 5, right: 30, left: 20, bottom: 5 }}
        >
          <defs>
            <linearGradient id="colorValue" x1="0" y1="0" x2="0" y2="1">
              <stop offset="5%" stopColor="#268bd2" stopOpacity={0.8}/>
              <stop offset="95%" stopColor="#268bd2" stopOpacity={0}/>
            </linearGradient>
          </defs>
          <CartesianGrid strokeDasharray="3 3" strokeOpacity={0.2} />
          <XAxis 
            dataKey="Date" 
            tickFormatter={(dateStr) => format(new Date(dateStr), 'MMM yy')}
            tick={{ fill: 'currentColor', fontSize: 12 }} 
            stroke="currentColor"
          />
          <YAxis 
            tickFormatter={valueFormatter} 
            tick={{ fill: 'currentColor', fontSize: 12 }}
            stroke="currentColor"
          />
          <Tooltip 
            formatter={tooltipFormatter}
            contentStyle={{
                backgroundColor: 'rgba(0, 43, 54, 0.8)', // dark-base with opacity
                borderColor: '#268bd2',
                color: '#fdf6e3'
            }}
            labelStyle={{ color: '#fdf6e3' }}
          />
          <Legend />
          <Area type="monotone" dataKey="PortfolioValue" stroke="#268bd2" fillOpacity={1} fill="url(#colorValue)" name={`Portfolio Value (${currency})`} />
        </AreaChart>
      </ResponsiveContainer>
    </div>
  );
}

export default PortfolioChart;