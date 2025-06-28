from typing import List
from sqlalchemy.orm import Session
from typing import Type
import pybreaker

from app.models.stock import Holding, Order, Position

circuit_breaker = pybreaker.CircuitBreaker(
    fail_max=3,
    reset_timeout=10
)

class StockService:
    def __init__(self, db: Session):
        self.db: Session = db

    @circuit_breaker
    def get_holdings(self, user_id: int) -> List[Type[Holding]]:
        return self.db.query(Holding).filter(Holding.user_id == user_id).all()

    @circuit_breaker
    def get_positions(self, user_id: int) -> List[Type[Position]]:
        return self.db.query(Position).filter(Position.user_id == user_id).all()

    @circuit_breaker
    def get_orders(self, user_id: int) -> List[Type[Order]]:
        return self.db.query(Order).filter(Order.user_id == user_id).all()


