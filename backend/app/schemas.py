# backend/app/schemas.py
from pydantic import BaseModel, Field, HttpUrl, ConfigDict
from datetime import datetime, date
from typing import Optional, List

# --- Base Schemas ---
class TradeSchema(BaseModel):
    model_config = ConfigDict(
        from_attributes=True,
        populate_by_name=True,
    )
    id: int
    asset_category: str = Field(..., alias='Asset Category')
    currency: str = Field(..., alias='Currency')
    symbol: str = Field(..., alias='Symbol')
    datetime: datetime = Field(..., alias='Date/Time') # type: ignore
    quantity: float = Field(..., alias='Quantity')
    t_price: float = Field(..., alias='T. Price')
    c_price: Optional[float] = Field(None, alias='C. Price')
    proceeds: Optional[float] = Field(None, alias='Proceeds')
    comm_fee: Optional[float] = Field(None, alias='Comm/Fee')
    basis: Optional[float] = Field(None, alias='Basis')
    realized_pl: Optional[float] = Field(None, alias='Realized P/L')
    mtm_pl: Optional[float] = Field(None, alias='MTM P/L')
    code: Optional[str] = Field(None, alias='Code')


# --- Schemas for Analytics ---
class DailyValue(BaseModel):
    Date: date
    PortfolioValue: float

class HoldingXIRR(BaseModel):
    symbol: str
    xirr_percent: Optional[float] = None
    message: Optional[str] = None

class Holding(BaseModel):
    symbol: str
    quantity: float
    market_value: float
    xirr_percent: Optional[float]

# --- Schema for News ---
class NewsArticle(BaseModel):
    model_config = ConfigDict(from_attributes=True, populate_by_name=True)
    uuid: str
    title: str
    publisher: str
    link: HttpUrl
    provider_publish_time: datetime
    # FIX: Renamed 'type' to 'article_type' and added an alias.
    article_type: str = Field(..., alias='type')