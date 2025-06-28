from pydantic import BaseModel, ConfigDict
from datetime import datetime


class HoldingDTO(BaseModel):
    id: int
    user_id: int
    symbol: str
    quantity: int
    avg_price: float
    current_price: float

    model_config = ConfigDict(from_attributes=True)

class OrderDTO(BaseModel):
    id: int
    user_id: int
    symbol: str
    order_type: str
    quantity: int
    price: float
    status: str
    timestamp: datetime
    realized_pnl: float

    model_config = ConfigDict(from_attributes=True)


class PositionDTO(BaseModel):
    id: int
    user_id: int
    symbol: str
    quantity: int
    entry_price: float
    current_price: float
    unrealized_pnl: float

    model_config = ConfigDict(from_attributes=True)
