import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from types import SimpleNamespace
from datetime import datetime, timezone

from app.dependencies import get_current_user, get_stock_service
from app.main import app
from app.models.User import User, RefreshToken
from app.core.database import Base, get_db

SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


class MockStockService:
    def get_holdings(self, user_id: int):
        return [
            SimpleNamespace(
                id=1,
                user_id=user_id,
                symbol="AAPL",
                quantity=15,
                avg_price=145.20,
                current_price=150.75,
                invested_amount=2178.00,
                market_value=2261.25,
                profit=83.25,
                pnl_percent=3.82,
                created_at=datetime.utcnow(),
            ),
            SimpleNamespace(
                id=2,
                user_id=user_id,
                symbol="GOOGL",
                quantity=5,
                avg_price=2800.00,
                current_price=2900.00,
                invested_amount=14000.00,
                market_value=14500.00,
                profit=500.00,
                pnl_percent=3.57,
                created_at=datetime.now(timezone.utc),
            ),
        ]

    def get_positions(self, user_id: int):
        return [
            SimpleNamespace(
                id=1,
                user_id=user_id,
                symbol="TSLA",
                quantity=10,
                entry_price=320.50,
                current_price=330.00,
                unrealized_pnl=95.0
            )
        ]

    def get_orders(self, user_id: int):
        return [
            SimpleNamespace(
                id=1,
                user_id=user_id,
                symbol="MSFT",
                order_type="buy",
                quantity=100,
                price=305.50,
                status="executed",
                timestamp=datetime.now(timezone.utc),
                realized_pnl=150.0,
            )
        ]


@pytest.fixture(scope="session", autouse=True)
def create_test_db():
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)


@pytest.fixture
def db():
    session = TestingSessionLocal()
    try:
        yield session
    finally:
        session.close()


@pytest.fixture
def client(db):
    def override_get_db():
        yield db

    app.dependency_overrides[get_db] = override_get_db
    return TestClient(app)

@pytest.fixture
def test_user():
    return User(id=1, username="sanjay", email="sanjay@gmail.com")


@pytest.fixture(autouse=True)
def clear_refresh_tokens(db):
    db.query(RefreshToken).delete()
    db.commit()


@pytest.fixture
def authorized_client(client, test_user):
    app.dependency_overrides[get_current_user] = lambda : test_user
    app.dependency_overrides[get_stock_service] = lambda : MockStockService()

    yield client

    app.dependency_overrides.clear()