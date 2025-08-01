# backend/app/models.py
from sqlalchemy import Column, Integer, String, Float, DateTime
from .database import Base

class Trade(Base):
    __tablename__ = "trades"

    # Define the columns for the 'trades' table
    id = Column(Integer, primary_key=True, index=True)
    asset_category = Column(String, name="Asset Category")
    currency = Column(String, name="Currency")
    symbol = Column(String, name="Symbol", index=True)
    datetime = Column(DateTime, name="Date/Time", index=True)
    quantity = Column(Float, name="Quantity")
    t_price = Column(Float, name="T. Price")
    c_price = Column(Float, name="C. Price")
    proceeds = Column(Float, name="Proceeds")
    comm_fee = Column(Float, name="Comm/Fee")
    basis = Column(Float, name="Basis")
    realized_pl = Column(Float, name="Realized P/L")
    mtm_pl = Column(Float, name="MTM P/L")
    code = Column(String, name="Code")