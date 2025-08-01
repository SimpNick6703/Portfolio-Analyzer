# Portfolio Analysis and Visualization Tool

This project is a full-stack application designed to analyze and visualize stock trading data. It processes trade history from CSV files, enriches it with real-world market data, calculates key performance metrics, and presents them through a modern web interface.

## Tech Stack

-   **Backend:** Python, FastAPI, SQLAlchemy, `yfinance`
-   **Database:** SQLite
-   **Frontend:** React 18, Tailwind CSS, Recharts
-   **Containerization:** Docker, Docker Compose
-   **Data Validation:** Pydantic

## Features

-   **Data Ingestion:** Loads and cleans trade data from multiple CSV files.
-   **Data Enrichment:** Fetches historical prices, currency rates (USD, INR, SGD), and stock split data from Yahoo Finance.
-   **Split Adjustment:** Automatically adjusts historical trades for stock splits to ensure data accuracy.
-   **Financial Calculations:**
    -   Calculates the daily portfolio value over time.
    -   Computes the XIRR (Extended Internal Rate of Return) for each individual holding.
-   **Dynamic UI:**
    -   A responsive dashboard with key performance indicators.
    -   An interactive chart to visualize portfolio growth.
    -   A detailed table of current holdings.
    -   A news feed that updates based on the selected holding.
    -   Switchable dark (default) and light themes.

## How to Run the Application

This project is fully containerized, so you only need to have **Docker** and **Docker Compose** installed on your system.

### Steps

1.  **Clone the repository (or ensure all files are in place):**
   ```bash
   git clone https://github.com/SimpNick6703/Portfolio-Analyzer.git
   cd Portfolio-Analyzer
   ```

2.  **Place Data Files:**
    Ensure your `Stock_trading_*.csv` files are located in the `backend/data/` directory.

3.  **Run Docker Compose:**
    Open a terminal in the root directory of the project (`portfolio-analyzer/`) and run the following command:

    ```bash
    docker-compose up --build
    ```

4.  **Access the Application:**
    -   Once the build is complete and the containers are running, open your web browser and navigate to:
        **`http://localhost:3000`**
    -   The backend API will be accessible at `http://localhost:8000`, and you can view the auto-generated documentation at `http://localhost:8000/docs`.

5.  **Stopping the Application:**
    -   To stop the containers, press `Ctrl + C` in the terminal where Docker Compose is running.
    -   To stop and remove the containers, you can run `docker-compose down`.