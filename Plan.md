### **Project Plan: Portfolio Analysis and Visualization Tool (Revised)**

The development will be structured in three main phases:

1.  **Phase 1: Backend Development & Data Processing**
2.  **Phase 2: Frontend Development & UI Implementation**
3.  **Phase 3: Containerization & Final Touches**

---

### **Phase 1: Backend Development & Data Processing (FastAPI)**

This phase focuses on building the core engine of the application.

- **Step 1.1: Project Setup and Data Loading**
  - **Action:** Initialize a FastAPI project structure.
  - **Data Ingestion:** Create a data loading module to read the three provided CSV files.
  - **Cleaning:** This module will automatically handle data inconsistencies, such as removing empty trailing rows and converting columns with commas (e.g., `"2,500"`) into proper numeric types.
  - **Consolidation:** The cleaned data from all files will be merged into a single, master list of transactions.
  - **Logging:** A robust logging system using Python's `logging` module will be configured to track key events (INFO, ERROR, WARN) throughout the application.

- **Step 1.2: Database and ORM Setup**
  - **Technology:** We will use **SQLite** for its simplicity and performance in this context, coupled with **SQLAlchemy** for the ORM. This avoids the overhead of setting up a separate database server while providing the full power of an ORM.
  - **Models:** Define Pydantic and SQLAlchemy models for `Trades`, `Holdings`, and `Currencies` to ensure data integrity and validation.
  - **Action:** A script will be created to populate the SQLite database with the consolidated trade data from Step 1.1.
- **Step 1.3: Data Enrichment with `yfinance`**
  - **Stock Splits:** For each unique stock symbol, we will query `yfinance` to fetch its split history. A function will be implemented to adjust all historical trades (quantity, price, and proceeds) chronologically based on the split dates.
  - **Historical Prices:** We will fetch daily historical price data (NAVs) for all holdings. To respect rate limits, data for each ticker will be fetched once and stored.
  -  **Currency Data:** We will fetch historical daily exchange rates for **USD-INR**, **USD-SGD** and **INR-SGD** pairs to allow for currency conversion.

- **Step 1.4: Core Financial Calculations**
  - **Daily Portfolio Value:** Implement logic to compute the total portfolio value for each day by iterating through the timeline of trades and applying the corresponding daily historical prices. This will be calculated for USD, INR, and SGD.
  - **XIRR per Holding:** Using the `numpy_financial` library, we will create a function to calculate the XIRR. This function will take the cash flows (proceeds from trades) and their dates for a specific holding, providing a powerful measure of its performance.

- **Step 1.5: API Endpoints**
  - **Holdings API:** Create endpoints like `/api/holdings` to return a list of current holdings, their quantities, and market values.
  - **Portfolio API:** An endpoint like `/api/portfolio/value` will serve the time-series data for the daily portfolio value.
  - **Analytics API:** Endpoints like `/api/holdings/{symbol}/xirr` will provide the calculated XIRR for a given stock.
  - **News API:** An endpoint `/api/holdings/{symbol}/news` will use `yfinance` to fetch and deliver the latest news for the selected holding.

### **Phase 2: Frontend Development (React & Tailwind CSS)**

This phase focuses on creating an intuitive and visually appealing user interface.

- **Step 2.1: Project Setup**
  - **Action:** Initialize a React 18 project using `create-react-app`.
  - **Styling:** Configure Tailwind CSS for modern, utility-first styling.

- **Step 2.2: UI/UX Design and Components**
  - **Theme:**
    - **Default (Dark):** The UI will feature a default dark theme with a clean, professional look using gradient shades.
    - **Light:** The light theme will use **`#fdf6e3`** as its base background color. We will select a suitable dark, high-contrast font color (e.g., a dark sepia or charcoal) to ensure excellent readability against this base.
    - **Toggle:** A theme toggle will be placed in the top-right corner for easy switching.
  - **Dashboard:** A main dashboard view will present a summary of the total portfolio value, overall return, and key metrics.
  - **Holdings Table:** A detailed table will display all individual holdings, their current value, quantity, and the calculated XIRR.
  - **Charts:** We will integrate a charting library (like Recharts) to visualize the portfolio's value over time.
  - **News Display:** A component to neatly display the latest news for each holding.

- **Step 2.3: API Integration**
  - **Action:** Connect the React components to the FastAPI backend endpoints to fetch and display all the necessary data dynamically.

### **Phase 3: Containerization & Finalization**

This phase ensures the application is easy to deploy and run.

- **Step 3.1: Dockerization**
  - **Backend:** Create a `Dockerfile` for the FastAPI application.
  - **Frontend:** Create a multi-stage `Dockerfile` for the React application to build and serve the static files efficiently.

- **Step 3.2: Docker Compose**
  - **Action:** A `docker-compose.yml` file will be created to define and link the backend and frontend services, allowing you to launch the entire application with a single command (`docker-compose up`).

- **Step 3.3: Final Review**
  - **Action:** A thorough review of the codebase will be conducted to ensure it is modular, readable (adhering to the <5 indent rule), and maintainable. All features will be tested to ensure they meet the requirements.