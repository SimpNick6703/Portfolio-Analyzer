# backend/main.py
from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from typing import List, AsyncGenerator
from contextlib import asynccontextmanager

# Import our modules
from .app import crud, models, schemas
from .app.database import engine, get_db, SessionLocal
from .app.config import logger, TRADE_FILES
from .app.data_loader import load_and_clean_trades

# Create all database tables defined in models.py
models.Base.metadata.create_all(bind=engine)

# --- Lifespan Management (The new way for startup/shutdown events) ---
@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    """
    Manages the application's lifespan. Code before 'yield' runs on startup.
    Code after 'yield' runs on shutdown.
    """
    logger.info("Application startup: Initializing...")
    
    # Use a standard synchronous session for the one-off startup task
    db = SessionLocal()
    try:
        # 1. Load data from files into a DataFrame
        trades_df = load_and_clean_trades(TRADE_FILES)
        
        # 2. Populate the database with the DataFrame
        if trades_df is not None and not trades_df.empty:
            crud.populate_database(db, trades_df)
        else:
            logger.error("No trade data was loaded, so the database could not be populated.")
    finally:
        db.close()
        
    logger.info("Startup process complete. The application is now ready.")
    
    yield  # The application is now running
    
    # --- Shutdown logic (if any) would go here ---
    logger.info("Application shutdown.")

# --- Application Setup ---
app = FastAPI(title="Portfolio Analyzer API", lifespan=lifespan)

# --- API Endpoints ---
@app.get("/")
def read_root(db: Session = Depends(get_db)):
    """Root endpoint providing basic API status and DB stats."""
    trade_count = crud.get_trade_count(db)
    return {
        "message": "Welcome to the Portfolio Analyzer API",
        "status": "ok",
        "database_status": "connected",
        "total_trades_in_db": trade_count
    }

@app.get("/trades", response_model=List[schemas.TradeSchema])
def get_all_trades(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """
    Retrieves a list of all trades from the database with pagination.
    """
    trades = db.query(models.Trade).offset(skip).limit(limit).all()
    return trades