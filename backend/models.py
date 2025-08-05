# backend/models.py
from sqlalchemy import Column, Integer, String, Float, DateTime, Date, Boolean
from database import Base

class Trade(Base):
    __tablename__ = "trades"

    trade_id = Column(Integer, primary_key=True, index=True)
    asset_category = Column(String, name="Asset Category")
    currency = Column(String, name="Currency")
    symbol = Column(String, name="Symbol", index=True)
    datetime = Column(DateTime, name="Date/Time", index=True)
    quantity = Column(Float, name="Quantity")
    t_price = Column(Float, name="T. Price")
    c_price = Column(Float, name="C. Price")
    proceeds = Column(Float, name="Proceeds")
    comm_fee = Column(Float, name="Comm/Fee")
    cost_basis = Column(Float, name="Basis")
    realized_pl = Column(Float, name="Realized P/L")
    mtm_pl = Column(Float, name="MTM P/L")
    trade_code = Column(String, name="Code")
    is_split_adjusted = Column(Boolean, default=False, nullable=False)

class StockSplit(Base):
    __tablename__ = "stock_splits"
    id = Column(Integer, primary_key=True, index=True)
    symbol = Column(String, index=True)
    date = Column(Date, index=True)
    ratio = Column(Float)

class HistoricalPrice(Base):
    __tablename__ = "historical_prices"
    id = Column(Integer, primary_key=True, index=True)
    symbol = Column(String, index=True)
    date = Column(Date, index=True)
    close_price = Column(Float)

class CurrencyRate(Base):
    __tablename__ = "currency_rates"
    id = Column(Integer, primary_key=True, index=True)
    pair = Column(String, index=True)
    date = Column(Date, index=True)
    rate = Column(Float)