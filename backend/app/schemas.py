# backend/app/schemas.py
from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional

# This Pydantic model defines the structure for a trade when interacting via the API.
# It helps with data validation, serialization, and documentation.
class TradeSchema(BaseModel):
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

    class Config:
        orm_mode = True  # Allows the model to be created from an ORM object
        allow_population_by_field_name = True