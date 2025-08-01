# backend/main.py
from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from typing import List, AsyncGenerator
from contextlib import asynccontextmanager

from .app import crud, models, schemas
from .app.database import engine, get_db, SessionLocal
from .app.config import logger, TRADE_FILES
from .app.data_loader import load_and_clean_trades
from .app.data_enricher import run_full_enrichment

models.Base.metadata.create_all(bind=engine)

@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    logger.info("Application startup: Initializing...")
    db = SessionLocal()
    try:
        # 1. Populate DB with raw trades if it's empty
        if crud.get_trade_count(db) == 0:
            trades_df = load_and_clean_trades(TRADE_FILES)
            if trades_df is not None and not trades_df.empty:
                crud.populate_database(db, trades_df)
            else:
                logger.error("No trade data loaded, cannot populate or enrich DB.")
        else:
            logger.info("Trade data already exists in DB.")

        # 2. Run the data enrichment process
        logger.info("Starting data enrichment process...")
        run_full_enrichment(db)
        logger.info("Data enrichment process complete.")

    finally:
        db.close()
    
    logger.info("Startup process complete. The application is now ready.")
    yield
    logger.info("Application shutdown.")

app = FastAPI(title="Portfolio Analyzer API", lifespan=lifespan)

# --- API Endpoints ---
@app.get("/")
def read_root(db: Session = Depends(get_db)):
    trade_count = crud.get_trade_count(db)
    return {
        "message": "Welcome to the Portfolio Analyzer API",
        "status": "ok",
        "total_trades_in_db": trade_count
    }

@app.get("/trades", response_model=List[schemas.TradeSchema])
def get_all_trades(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    """ Retrieves a paginated list of trades from the database. """
    trades = db.query(models.Trade).order_by(models.Trade.datetime).offset(skip).limit(limit).all()
    return trades

@app.get("/data/splits/{symbol}")
def get_splits(symbol: str, db: Session = Depends(get_db)):
    """ Retrieves stored split data for a given symbol. """
    splits = db.query(models.StockSplit).filter(models.StockSplit.symbol == symbol.upper()).all()
    return splits