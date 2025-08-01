import React, { useState, useEffect } from 'react';
import './App.css';

function App() {
  // State to manage the theme. 'dark' is the default.
  const [theme, setTheme] = useState('dark');

  // Effect to apply the theme class to the html element
  useEffect(() => {
    const root = window.document.documentElement;
    root.classList.remove(theme === 'dark' ? 'light' : 'dark');
    root.classList.add(theme);
  }, [theme]);
  
  const toggleTheme = () => {
    setTheme(theme === 'dark' ? 'light' : 'dark');
  };

  return (
    // Main container with theme-based background and text colors
    <div className="min-h-screen bg-light-base text-light-text dark:bg-dark-base dark:text-dark-text">
      <header className="bg-light-content dark:bg-dark-content shadow-md">
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
        <h2 className="text-2xl font-semibold text-light-text-strong dark:text-dark-text-strong">
          Dashboard
        </h2>
        <p className="mt-4">
          Welcome to your portfolio dashboard. Components with data will be added here soon.
        </p>
      </main>
    </div>
  );
}

export default App;