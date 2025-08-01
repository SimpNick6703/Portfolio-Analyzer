# backend/main.py
from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List, AsyncGenerator
from contextlib import asynccontextmanager
import yfinance as yf

from .app import crud, models, schemas
from .app.database import engine, get_db, SessionLocal
from .app.config import logger, TRADE_FILES
from .app.data_loader import load_and_clean_trades
from .app.data_enricher import run_full_enrichment
from .app.financial_calculator import get_daily_portfolio_value, calculate_xirr_for_holding, get_current_holdings

models.Base.metadata.create_all(bind=engine)

@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    logger.info("Application startup: Initializing...")
    db = SessionLocal()
    try:
        if crud.get_trade_count(db) == 0:
            trades_df = load_and_clean_trades(TRADE_FILES)
            if trades_df is not None and not trades_df.empty:
                crud.populate_database(db, trades_df)
        else:
            logger.info("Trade data already exists in DB.")

        logger.info("Starting data enrichment process...")
        run_full_enrichment(db)
        logger.info("Data enrichment process complete.")
    finally:
        db.close()
    
    logger.info("Startup process complete.")
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
    trades = db.query(models.Trade).order_by(models.Trade.datetime).offset(skip).limit(limit).all()
    return trades

@app.get("/data/splits/{symbol}")
def get_splits(symbol: str, db: Session = Depends(get_db)):
    splits = db.query(models.StockSplit).filter(models.StockSplit.symbol == symbol.upper()).all()
    return splits

@app.get("/analytics/portfolio-value", response_model=List[schemas.DailyValue])
def get_portfolio_value(currency: str = "USD", db: Session = Depends(get_db)):
    if currency.upper() not in ["USD", "INR", "SGD"]:
        raise HTTPException(status_code=400, detail="Invalid currency. Use USD, INR, or SGD.")
    value_df = get_daily_portfolio_value(db, target_currency=currency.upper())
    return value_df.to_dict(orient='records')

@app.get("/analytics/xirr/{symbol}", response_model=schemas.HoldingXIRR)
def get_xirr(symbol: str, db: Session = Depends(get_db)):
    xirr = calculate_xirr_for_holding(db, symbol.upper())
    if xirr is None:
        return {"symbol": symbol.upper(), "xirr_percent": None, "message": "Could not calculate XIRR."}
    return {"symbol": symbol.upper(), "xirr_percent": xirr}

@app.get("/analytics/holdings", response_model=List[schemas.Holding])
def get_holdings_list(db: Session = Depends(get_db)):
    """
    Returns a list of all current holdings with their market value and XIRR.
    """
    return get_current_holdings(db)

# --- NEW NEWS ENDPOINT ---
@app.get("/news/{symbol}", response_model=List[schemas.NewsArticle])
def get_news_for_holding(symbol: str):
    """
    Fetches the latest news articles for a given stock symbol.
    """
    logger.info(f"Fetching news for symbol: {symbol.upper()}")
    try:
        ticker = yf.Ticker(symbol)
        # .news returns a list of dictionaries
        news_list = ticker.news
        if not news_list:
            logger.warning(f"No news found for {symbol.upper()}")
            return []
        
        # Pydantic will automatically validate the structure of each article
        return news_list
        
    except Exception as e:
        logger.error(f"Failed to fetch news for {symbol.upper()}: {e}")
        raise HTTPException(status_code=500, detail="Failed to fetch news from provider.")