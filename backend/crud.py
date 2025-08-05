# backend/crud.py
from sqlalchemy.orm import Session
from sqlalchemy import func
import pandas as pd
import models
from config import logger
from datetime import date

def get_trade_count(db: Session) -> int:
    return db.query(models.Trade).count()

def get_unique_symbols(db: Session) -> list:
    return [s[0] for s in db.query(models.Trade.symbol).distinct().all()]

def get_trades_to_adjust(db: Session, symbol: str, split_date: date) -> list[models.Trade]:
    return db.query(models.Trade).filter(
        models.Trade.symbol == symbol,
        func.date(models.Trade.datetime) < split_date,
        models.Trade.is_split_adjusted == False
    ).all()

def populate_database(db: Session, trades_df: pd.DataFrame):
    if get_trade_count(db) > 0:
        logger.info("Database already contains trade data. Skipping population.")
        return
    logger.info("Database is empty. Populating with new trade data...")
    df_renamed = trades_df.rename(columns={
        "Asset Category": "asset_category", "Currency": "currency", "Symbol": "symbol",
        "Date/Time": "datetime", "Quantity": "quantity", "T. Price": "t_price",
        "C. Price": "c_price", "Proceeds": "proceeds", "Comm/Fee": "comm_fee",
        "Basis": "cost_basis", "Realized P/L": "realized_pl", "MTM P/L": "mtm_pl",
        "Code": "trade_code"
    })
    trades_to_insert = df_renamed.where(pd.notnull(df_renamed), None).to_dict(orient='records')
    try:
        db.add_all([models.Trade(**trade) for trade in trades_to_insert])
        db.commit()
        logger.info(f"Successfully inserted {len(trades_to_insert)} trades into the database.")
    except Exception as e:
        logger.error(f"Failed to populate database: {e}")
        db.rollback()

def get_split_count_for_symbol(db: Session, symbol: str) -> int:
    return db.query(models.StockSplit).filter(models.StockSplit.symbol == symbol).count()

def create_splits(db: Session, splits: list[dict]):
    db.add_all([models.StockSplit(**split) for split in splits])
    db.commit()

def get_latest_price_date(db: Session, symbol: str) -> date | None:
    return db.query(func.max(models.HistoricalPrice.date)).filter(models.HistoricalPrice.symbol == symbol).scalar()

def create_historical_prices(db: Session, prices: list[dict]):
    db.add_all([models.HistoricalPrice(**price) for price in prices])
    db.commit()

def get_latest_rate_date(db: Session, pair: str) -> date | None:
    return db.query(func.max(models.CurrencyRate.date)).filter(models.CurrencyRate.pair == pair).scalar()

def create_currency_rates(db: Session, rates: list[dict]):
    db.add_all([models.CurrencyRate(**rate) for rate in rates])
    db.commit()