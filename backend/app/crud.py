# backend/app/crud.py
from sqlalchemy.orm import Session
import pandas as pd
from . import models
from .config import logger

def get_trade_count(db: Session) -> int:
    """Returns the total number of trades in the database."""
    return db.query(models.Trade).count()

def populate_database(db: Session, trades_df: pd.DataFrame):
    """
    Populates the database with trade data from a DataFrame.
    This function is idempotent; it won't insert data if the table is not empty.
    """
    # Check if the database is already populated
    if get_trade_count(db) > 0:
        logger.info("Database already contains trade data. Skipping population.")
        return

    logger.info("Database is empty. Populating with new trade data...")
    
    # Convert DataFrame to a list of dictionaries for easier processing
    # The columns in the DataFrame must match the keys expected by the Trade model
    # We rename the DataFrame columns to match the model's attribute names
    
    df_renamed = trades_df.rename(columns={
        "Asset Category": "asset_category",
        "Currency": "currency",
        "Symbol": "symbol",
        "Date/Time": "datetime",
        "Quantity": "quantity",
        "T. Price": "t_price",
        "C. Price": "c_price",
        "Proceeds": "proceeds",
        "Comm/Fee": "comm_fee",
        "Basis": "basis",
        "Realized P/L": "realized_pl",
        "MTM P/L": "mtm_pl",
        "Code": "code"
    })
    
    # Convert to list of dicts and handle NaN values which SQL doesn't like
    trades_to_insert = df_renamed.where(pd.notnull(df_renamed), None).to_dict(orient='records')
    
    try:
        # Create Trade model objects and add them to the session
        db.add_all([models.Trade(**trade) for trade in trades_to_insert])
        db.commit()
        logger.info(f"Successfully inserted {len(trades_to_insert)} trades into the database.")
    except Exception as e:
        logger.error(f"Failed to populate database: {e}")
        db.rollback()