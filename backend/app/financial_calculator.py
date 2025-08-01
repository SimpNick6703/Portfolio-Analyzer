# backend/app/financial_calculator.py
import pandas as pd
import numpy_financial as npf
from sqlalchemy.orm import Session
from datetime import date, timedelta
from . import models
from .config import logger

def get_daily_portfolio_value(db: Session, target_currency: str = 'USD') -> pd.DataFrame:
    """
    Calculates the daily portfolio value over time in the specified currency.

    Args:
        db: The database session.
        target_currency: The currency to report the value in ('USD', 'INR', 'SGD').

    Returns:
        A pandas DataFrame with 'Date' and 'PortfolioValue' columns.
    """
    logger.info(f"Calculating daily portfolio value in {target_currency}...")
    
    # 1. Fetch all necessary data into pandas DataFrames for efficient processing
    trades = pd.read_sql(db.query(models.Trade).statement, db.bind)
    prices = pd.read_sql(db.query(models.HistoricalPrice).statement, db.bind)
    rates = pd.read_sql(db.query(models.CurrencyRate).statement, db.bind)

    if trades.empty:
        logger.warning("No trades found, cannot calculate portfolio value.")
        return pd.DataFrame(columns=['Date', 'PortfolioValue'])

    # 2. Prepare data for merging
    trades['date'] = pd.to_datetime(trades['Date/Time']).dt.date
    prices['date'] = pd.to_datetime(prices['date']).dt.date
    rates['date'] = pd.to_datetime(rates['date']).dt.date
    
    # Pivot rates for easy lookup
    rates_pivot = rates.pivot(index='date', columns='pair', values='rate').ffill()

    # 3. Determine the full date range for the portfolio history
    start_date = trades['date'].min()
    end_date = date.today()
    date_range = pd.to_datetime(pd.date_range(start=start_date, end=end_date)).date
    
    portfolio_values = []
    
    # 4. Iterate through each day in the portfolio's history
    for current_date in date_range:
        # Get all trades that happened up to and including the current day
        past_trades = trades[trades['date'] <= current_date]
        
        # Calculate current holdings by summing quantities for each symbol
        holdings = past_trades.groupby('Symbol')['Quantity'].sum()
        holdings = holdings[holdings > 0] # Filter out stocks that have been sold off

        daily_value = 0.0
        
        # 5. Calculate the value of each holding
        for symbol, quantity in holdings.items():
            # Get the latest price for the symbol on or before the current date
            latest_price_series = prices[(prices['Symbol'] == symbol) & (prices['date'] <= current_date)]
            if latest_price_series.empty:
                continue # No price data available for this date yet
                
            latest_price = latest_price_series.sort_values(by='date', ascending=False).iloc[0]
            
            # Find the currency of the first trade for this symbol to determine its native currency
            asset_currency = trades[trades['Symbol'] == symbol].iloc[0]['Currency']
            
            value_in_asset_currency = quantity * latest_price['close_price']
            
            # 6. Convert the holding's value to the target currency
            value_in_target_currency = _convert_currency(
                value_in_asset_currency,
                asset_currency,
                target_currency,
                current_date,
                rates_pivot
            )
            daily_value += value_in_target_currency
            
        portfolio_values.append({'Date': current_date, 'PortfolioValue': daily_value})

    logger.info("Finished calculating daily portfolio value.")
    return pd.DataFrame(portfolio_values)


def _convert_currency(amount: float, from_currency: str, to_currency: str, conv_date: date, rates_df: pd.DataFrame) -> float:
    """Helper function to convert an amount between currencies on a specific date."""
    if from_currency == to_currency:
        return amount

    try:
        if from_currency == 'USD':
            # USD to SGD or INR
            pair = f"USD{to_currency}=X"
            rate = rates_df.loc[rates_df.index <= pd.to_datetime(conv_date), pair].iloc[-1]
            return amount * rate
        elif to_currency == 'USD':
            # SGD or INR to USD
            pair = f"USD{from_currency}=X"
            rate = rates_df.loc[rates_df.index <= pd.to_datetime(conv_date), pair].iloc[-1]
            return amount / rate
        else: # e.g., SGD to INR
            pair_sgd_usd = "USDSGD=X"
            pair_usd_inr = "USDINR=X"
            rate_sgd = rates_df.loc[rates_df.index <= pd.to_datetime(conv_date), pair_sgd_usd].iloc[-1]
            rate_inr = rates_df.loc[rates_df.index <= pd.to_datetime(conv_date), pair_usd_inr].iloc[-1]
            if from_currency == 'SGD' and to_currency == 'INR':
                return (amount / rate_sgd) * rate_inr # Convert SGD to USD, then USD to INR
            # Add other non-USD conversions if necessary
    except (IndexError, KeyError):
        # Handle cases where conversion rate is not available for the date
        return amount # Fallback to no conversion

    return amount # Default fallback

def calculate_xirr_for_holding(db: Session, symbol: str) -> float | None:
    """
    Calculates the XIRR (Internal Rate of Return) for a specific holding.

    Args:
        db: The database session.
        symbol: The stock symbol to calculate XIRR for.

    Returns:
        The calculated XIRR as a percentage, or None if calculation is not possible.
    """
    # 1. Get all trades for the symbol, ordered by date
    trades = db.query(models.Trade).filter(models.Trade.symbol == symbol).order_by(models.Trade.datetime).all()
    if not trades:
        return None

    cash_flows = []
    dates = []

    # 2. Generate cash flow events from trades
    for trade in trades:
        # Proceeds are negative for buys and positive for sells
        cash_flows.append(trade.Proceeds)
        dates.append(trade.datetime.date())

    # 3. Add the final market value of current holdings as the last cash flow event
    current_quantity = sum(t.Quantity for t in trades)
    if current_quantity > 0:
        latest_price_entry = db.query(models.HistoricalPrice)\
            .filter(models.HistoricalPrice.symbol == symbol)\
            .order_by(models.HistoricalPrice.date.desc())\
            .first()
        
        if latest_price_entry:
            current_value = current_quantity * latest_price_entry.close_price
            cash_flows.append(current_value) # Positive cash flow as if sold today
            dates.append(date.today())
        else:
            logger.warning(f"No price data for {symbol}, cannot add final value to XIRR calc.")
    
    # 4. Ensure there are at least one positive and one negative cash flow
    if not any(cf > 0 for cf in cash_flows) or not any(cf < 0 for cf in cash_flows):
        logger.warning(f"XIRR for {symbol} requires both positive and negative cash flows.")
        return None

    try:
        # Use numpy_financial to calculate XIRR
        xirr_value = npf.xirr(cash_flows, dates)
        return xirr_value * 100 # Return as percentage
    except (ValueError, TypeError) as e:
        logger.error(f"Could not calculate XIRR for {symbol}: {e}")
        return None

def get_current_holdings(db: Session) -> list:
    """
    Calculates the current quantity and market value for all holdings.

    Returns:
        A list of dictionaries, each representing a holding.
    """
    logger.info("Calculating current holdings...")
    
    # Using pandas for efficient calculation
    trades_df = pd.read_sql(db.query(models.Trade).statement, db.bind)
    prices_df = pd.read_sql(db.query(models.HistoricalPrice).statement, db.bind)

    if trades_df.empty:
        return []

    # Get the latest price for each symbol
    latest_prices = prices_df.loc[prices_df.groupby('Symbol')['date'].idxmax()]
    latest_prices = latest_prices.set_index('Symbol')['close_price']
    
    # Calculate current quantities
    current_quantities = trades_df.groupby('Symbol')['Quantity'].sum()
    
    # Filter for holdings we still own
    holdings = current_quantities[current_quantities > 0].reset_index()
    holdings.rename(columns={'Quantity': 'quantity'}, inplace=True)
    
    # Map the latest price to each holding
    holdings['market_value'] = holdings['Symbol'].map(latest_prices) * holdings['quantity']
    holdings.fillna({'market_value': 0}, inplace=True) # Handle case where price might be missing
    
    # Fetch XIRR for each holding
    def get_xirr(symbol):
        xirr = calculate_xirr_for_holding(db, symbol)
        # Ensure we return a JSON-serializable float or None
        return float(xirr) if xirr is not None else None

    holdings['xirr_percent'] = holdings['Symbol'].apply(get_xirr)

    # Rename for consistency with schema
    holdings.rename(columns={'Symbol': 'symbol'}, inplace=True)
    
    return holdings.to_dict(orient='records')