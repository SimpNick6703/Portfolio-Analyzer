You are given 3 CSV files containing dummy stock trade data. 
Overall objective is to compute portfolio returns and portfolio value (individual holdings + portfolio). Steps, to help you, are as under. 

To do:
1. Create a simple data structure to append and store the files.
2. Create a master list of holdings
3. Get stock split details, if available. If a stock has split 1:2, it means price has become half and quantity has doubled.
4. Transform input files to reflect split adjusted price and quantity. It needs to be done iteratively basis the split date. Adjust trading cashflow as adjusted price * adjusted quantity.
5. Get historical daily currency pairing for each date (USD, INR, SGD) 
6. Compute transaction price in each currency
7. Get split adjusted historical prices / NAVs of the stocks / mutual funds through yahoo finance / amfi
8. Compute daily portfolio value across currencies. Portfolio value = Quantity * price, summed for all holdings
9. Compute XIRR for each holding
10. Represent through a simple UI

Create a plan then prompt me if it is okay to proceed for code. Project should have robust logging with proper flags like INFO, ERROR, WARN, etc (flags are up to you to create/innovate).
Tech Stack: Python fastapi, tailwindcss, react18, sqlite/postgresql (consider performance and the code clarity to decide SQLite vs PostgreSQL), dockerization, sqlalchemy for ORM and pydantic for data validation. Limit use the use of tech stacks to these only and ask me first before using any other tech stack. Code should be modular, maintainable, reviewable and preferably shouldn't have more than 5 indents such that it is readable. Keep the comments to a minimum, only include when necessary. Frontend should have both dark and light themes with appropriate gradient shades used throughout the UI, while Dark theme should be default with a toggle on top right corner. 

Amends and Tips:
1. For frontend, do not use Vite since I have no knowledge of it. And use #fdf6e3 color scheme. as base for light theme. It is not a white shade will put less strain on eyes. Pick right shade for font later based on this too.
2. Keep use of `yfinance`, `python-multipart` and `numpy-finance` somewhat elemental and explanatory since today I learnt they exist.
3. Through APIs, bring latest news of the holdings.
4. Respect yfinance rate limits since too many requests to yahoo finance may block the IP.