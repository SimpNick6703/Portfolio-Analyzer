# backend/main.py
from fastapi import FastAPI
from .app.config import logger, TRADE_FILES
from .app.data_loader import load_and_clean_trades

# --- Application Setup ---
app = FastAPI(title="Portfolio Analyzer API")

# --- Global State (use with caution, for demonstration here) ---
# In a real app, this would be managed by a database connection pool.
master_trade_data = None

@app.on_event("startup")
def startup_event():
    """Actions to perform on application startup."""
    global master_trade_data
    logger.info("Application startup: Loading and cleaning trade data...")
    master_trade_data = load_and_clean_trades(TRADE_FILES)
    if master_trade_data is not None and not master_trade_data.empty:
        logger.info("Trade data loaded successfully into memory.")
        # Log the first 5 rows for verification
        logger.info("Sample of loaded data:\n" + master_trade_data.head().to_string())
    else:
        logger.error("Failed to load trade data. The application might not function correctly.")

@app.get("/")
def read_root():
    """Root endpoint for the API."""
    return {
        "message": "Welcome to the Portfolio Analyzer API",
        "status": "ok",
        "loaded_trades": len(master_trade_data) if master_trade_data is not None else 0
    }