
# 📈 Liquide Backend Assignment

A FastAPI-based backend that supports user authentication and stock tracking — including holdings, orders, and positions. Fully containerized using Docker.

---

## 🚀 Features

- 🧑 User registration & login (JWT-based)
- 📊 View holdings, orders, and positions by user
- ✅ Protected routes with token authentication
- 🐳 Dockerized for easy deployment

---

## 📁 Project Structure

```
app/
├── core/
│   ├── database.py      # Database configuration and connection
│   └── security.py      # Authentication and password hashing
├── models/
│   ├── User.py          # User and RefreshToken models
│   └── stock.py         # Stock-related models (Holding, Order, Position)
├── schemas/
│   ├── user.py          # User Pydantic schemas
│   ├── stock.py         # Stock Pydantic schemas
│   └── token.py         # Token schemas
├── services/
│   ├── user.py          # User business logic
│   └── stock.py         # Stock business logic with circuit breaker
├── routers/
│   ├── auth.py          # Authentication endpoints
│   └── stock.py         # Stock-related endpoints
├── config.py            # Application configuration
├── dependencies.py      # FastAPI dependencies
├── main.py             # Application entry point
└── seeds.py            # Database seeding
```

---

## ⚙️ Environment Setup

### 1. Clone the Repository
```bash
git clone https://github.com/your-org/LiquideBackendAssignment.git
cd LiquideBackendAssignment
```

### 2. Environment Variables

Please rename example.env to .env and use it as environment file

---

## 🐳 Docker Usage

### 🔨 Build & Run Containers

```bash
docker-compose up --build
```

### ❌ Stop the app

```bash
docker-compose down
```

---

## 🔐 Auth Endpoints

### 📥 Register - `POST /auth/register`
```json
{
  "username": "john_doe",
  "email": "john@example.com",
  "password": "securePass123"
}
```

### 🔑 Login - `POST /auth/login`
```json
{
  "username": "john_doe",
  "password": "securePass123"
}
```

✅ Response:
```json
{
  "access_token": "your.jwt.token",
  "token_type": "bearer"
}
```

> 🔒 Use this token for all stock API requests in the `Authorization` header.

---

## 📊 Stock Endpoints

All these endpoints require:

```
Authorization: Bearer <access_token>
```

### 🧾 Holdings - `GET /stock/holdings?user_id=1`

Example Response:
```json
[
  {
    "symbol": "AAPL",
    "quantity": 10,
    "average_price": 150.0,
    "current_price": 155.5
  }
]
```

---

### 📈 Positions - `GET /stock/positions?user_id=1`

Example Response:
```json
[
  {
    "symbol": "TSLA",
    "quantity": 5,
    "buy_price": 600.0,
    "current_price": 720.0
  }
]
```

---

### 📋 Orders - `GET /stock/orders?user_id=1`

Example Response:
```json
[
  {
    "symbol": "MSFT",
    "order_type": "buy",
    "status": "filled",
    "price": 280.0,
    "quantity": 3
  }
]
```

---

## 🧪 Running Tests

```if needed to execute from docker container```

```bash
docker exec -it app bash

then run:
pytest
```

