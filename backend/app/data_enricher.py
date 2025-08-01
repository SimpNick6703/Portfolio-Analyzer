# backend/app/data_enricher.py
import yfinance as yf
import time
from sqlalchemy.orm import Session
from datetime import date, timedelta
from . import crud, models
from .config import logger

# Fetches stock splits and stores them in the database.
def fetch_and_store_splits(db: Session, symbol: str):
    if crud.get_split_count_for_symbol(db, symbol) > 0:
        logger.info(f"Split data for {symbol} already exists. Skipping fetch.")
        return

    logger.info(f"Fetching split data for {symbol}...")
    try:
        ticker = yf.Ticker(symbol)
        splits = ticker.splits
        if not splits.empty:
            splits_to_add = []
            for split_date, ratio in splits.items():
                splits_to_add.append({
                    "symbol": symbol,
                    "date": split_date.date(),
                    "ratio": ratio
                })
            crud.create_splits(db, splits_to_add)
            logger.info(f"Stored {len(splits_to_add)} split events for {symbol}.")
        else:
            logger.info(f"No split history found for {symbol}.")
    except Exception as e:
        logger.error(f"Could not fetch splits for {symbol}: {e}")

# Adjusts historical trades based on stored split data.
def adjust_trades_for_splits(db: Session):
    logger.info("Starting split adjustment process for all trades...")
    all_splits = db.query(models.StockSplit).order_by(models.StockSplit.date).all()

    if not all_splits:
        logger.info("No split data in database. No adjustments to make.")
        return

    for split in all_splits:
        trades_to_adjust = crud.get_trades_to_adjust(db, split.symbol, split.date)
        if not trades_to_adjust:
            continue

        logger.info(f"Applying {split.ratio}:1 split on {split.date} to {len(trades_to_adjust)} trades for {split.symbol}.")
        for trade in trades_to_adjust:
            trade.quantity *= split.ratio
            trade.t_price /= split.ratio
            trade.is_split_adjusted = True # Mark as adjusted
        
        db.commit()
    logger.info("Split adjustment process completed.")
    
# Generic fetcher for historical prices and currency rates.  
def _fetch_yf_data(db: Session, name: str, is_currency: bool):
    fetch_type = "currency rates" if is_currency else "historical prices"
    get_latest_date_func = crud.get_latest_rate_date if is_currency else crud.get_latest_price_date
    create_func = crud.create_currency_rates if is_currency else crud.create_historical_prices
    
    start_date = get_latest_date_func(db, name)
    if start_date:
        start_date += timedelta(days=1) # Start from the day after the last entry
    else:
        start_date = date(2022, 1, 1) # Fallback start date
        
    end_date = date.today()

    if start_date > end_date:
        logger.info(f"{fetch_type.capitalize()} for {name} are up to date. Skipping.")
        return

    logger.info(f"Fetching {fetch_type} for {name} from {start_date} to {end_date}...")
    try:
        data = yf.download(name, start=start_date, end=end_date, progress=False)
        if data.empty:
            logger.warning(f"No {fetch_type} data found for {name} in the specified period.")
            return

        data_to_store = []
        for index, row in data.iterrows():
            record = {
                "date": index.date(),
                "close_price": row['Close']
            }
            if is_currency:
                record["pair"] = name
                record["rate"] = row['Close']
                del record["close_price"]
            else:
                record["symbol"] = name
            
            data_to_store.append(record)

        if data_to_store:
            create_func(db, data_to_store)
            logger.info(f"Stored {len(data_to_store)} new {fetch_type} entries for {name}.")
            
    except Exception as e:
        logger.error(f"Could not fetch {fetch_type} for {name}: {e}")

# Orchestrates the entire data enrichment process.
def run_full_enrichment(db: Session):
    unique_symbols = crud.get_unique_symbols(db)
    currency_pairs = ["USDSGD=X", "USDINR=X", "INRSGD=X"]

    # 1. Fetch splits and adjust trades
    for symbol in unique_symbols:
        fetch_and_store_splits(db, symbol)
        time.sleep(1) # Respect rate limits
    
    adjust_trades_for_splits(db)

    # 2. Fetch historical prices
    for symbol in unique_symbols:
        _fetch_yf_data(db, symbol, is_currency=False)
        time.sleep(1) # Respect rate limits
        
    # 3. Fetch currency rates
    for pair in currency_pairs:
        _fetch_yf_data(db, pair, is_currency=True)
        time.sleep(1) # Respect rate limits