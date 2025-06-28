from sqlalchemy.orm import Session
from app.models.stock import Holding, Order, Position, OrderType, OrderStatus
from app.core.database import sessionLocal
from sqlalchemy import delete

def seed_db():
    db: Session = sessionLocal()
    try:
        # Clear existing data
        db.execute(delete(Position))
        db.execute(delete(Order))
        db.execute(delete(Holding))
        db.commit()

        # Add holdings
        holdings = [
            Holding(user_id=1, symbol="AAPL", quantity=10, avg_price=150.0, current_price=160.0),
            Holding(user_id=1, symbol="TSLA", quantity=5, avg_price=700.0, current_price=650.0),
            Holding(user_id=2, symbol="GOOG", quantity=8, avg_price=2800.0, current_price=2900.0),
        ]
        db.add_all(holdings)

        # Add orders
        orders = [
            Order(user_id=1, symbol="AAPL", order_type=OrderType.BUY, quantity=10, price=150.0,
                  status=OrderStatus.EXECUTING, realized_pnl=0.0),
            Order(user_id=1, symbol="TSLA", order_type=OrderType.SELL, quantity=5, price=680.0,
                  status=OrderStatus.EXECUTING, realized_pnl=-100.0),
            Order(user_id=2, symbol="GOOG", order_type=OrderType.BUY, quantity=8, price=2800.0,
                  status=OrderStatus.EXECUTING, realized_pnl=0.0),
        ]
        db.add_all(orders)

        # Add positions
        positions = [
            Position(user_id=1, symbol="INFY", quantity=20, entry_price=1400.0, current_price=1450.0, unrealized_pnl=1000.0),
            Position(user_id=1, symbol="WIPRO", quantity=15, entry_price=410.0, current_price=390.0, unrealized_pnl=-300.0),
            Position(user_id=2, symbol="TCS", quantity=12, entry_price=3200.0, current_price=3300.0, unrealized_pnl=1200.0),
        ]
        db.add_all(positions)

        db.commit()
        print("Seed data inserted successfully.")
    except Exception as e:
        db.rollback()
        print(f"Error during seeding: {e}")
    finally:
        db.close()
