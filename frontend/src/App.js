// frontend/src/App.js
import React, { useState, useEffect } from 'react';
import axios from 'axios';
import './App.css';

import StatCard from './components/StatCard';
import PortfolioChart from './components/Chart';
import HoldingsTable from './components/HoldingsTable';
import NewsFeed from './components/NewsFeed';

// The base URL for our backend API.
const API_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000';

function App() {
  const [theme, setTheme] = useState('dark');
  const [portfolioValueData, setPortfolioValueData] = useState([]);
  const [holdings, setHoldings] = useState([]);
  const [selectedSymbol, setSelectedSymbol] = useState(null);
  const [news, setNews] = useState(null);
  const [currency] = useState('USD'); // For future implementation of currency switching

  useEffect(() => {
    // Apply theme
    const root = window.document.documentElement;
    root.classList.remove(theme === 'dark' ? 'light' : 'dark');
    root.classList.add(theme);
  }, [theme]);

  // Fetch portfolio value data
  useEffect(() => {
    // Fetch portfolio value
    axios.get(`${API_URL}/analytics/portfolio-value?currency=${currency}`)
      .then(response => {
        setPortfolioValueData(response.data);
      })
      .catch(error => console.error("Error fetching portfolio value:", error));

    // Fetch holdings data
    axios.get(`${API_URL}/analytics/holdings`)
        .then(response => {
            setHoldings(response.data);
        })
        .catch(error => console.error("Error fetching holdings:", error));

  }, [currency]);
  
  // Fetch news when a symbol is selected
  useEffect(() => {
    if (selectedSymbol) {
      setNews(null); // Set to loading state
      axios.get(`${API_URL}/news/${selectedSymbol}`)
        .then(response => {
          setNews(response.data);
        })
        .catch(error => {
          console.error(`Error fetching news for ${selectedSymbol}:`, error);
          setNews([]); // Set to empty to show "not found" message
        });
    }
  }, [selectedSymbol]);

  const toggleTheme = () => {
    setTheme(theme === 'dark' ? 'light' : 'dark');
  };

  const handleHoldingClick = (symbol) => {
    setSelectedSymbol(symbol);
  };
  
  const totalValue = portfolioValueData.length > 0 ? portfolioValueData[portfolioValueData.length - 1].PortfolioValue : 0;

  return (
    <div className="min-h-screen bg-light-base text-light-text dark:bg-dark-base dark:text-dark-text transition-colors duration-300">
      <header className="bg-light-content dark:bg-dark-content shadow-md sticky top-0 z-10">
        <nav className="container mx-auto px-6 py-3 flex justify-between items-center">
          <h1 className="text-xl font-bold text-light-text-strong dark:text-dark-text-strong">
            Portfolio Analyzer
          </h1>
          <button 
            onClick={toggleTheme}
            className="p-2 rounded-full text-light-text-strong dark:text-dark-text-strong focus:outline-none"
          >
            {theme === 'dark' ? '☀️' : '🌙'}
          </button>
        </nav>
      </header>
      
      <main className="container mx-auto p-6">
        <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
            <StatCard 
                title="Total Portfolio Value" 
                value={new Intl.NumberFormat('en-US', { style: 'currency', currency: currency }).format(totalValue)} 
            />
            <StatCard title="Holdings" value={holdings.length} />
            <StatCard title="Performance (24h)" value="+1.25%" subtext="Placeholder" />
        </div>

        <div className="mt-6">
            <PortfolioChart data={portfolioValueData} currency={currency} />
        </div>
        
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-6 mt-6">
            <div className="lg:col-span-2">
                <HoldingsTable holdings={holdings} onRowClick={handleHoldingClick} />
            </div>
            <div>
                <NewsFeed news={news} symbol={selectedSymbol} />
            </div>
        </div>
      </main>
    </div>
  );
}

export default App;