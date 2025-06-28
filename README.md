# Stock Trading API

A robust FastAPI-based stock trading application with JWT authentication, database persistence, and circuit breaker pattern for reliability.

## Features

- **User Authentication**: JWT-based authentication with access and refresh tokens
- **Stock Management**: Track holdings, positions, and orders
- **Database Integration**: MySQL database with SQLAlchemy ORM
- **Security**: Password hashing with bcrypt and secure token management
- **Reliability**: Circuit breaker pattern for service fault tolerance
- **Data Seeding**: Automatic database seeding for development

## Tech Stack

- **Backend**: FastAPI
- **Database**: MySQL with PyMySQL driver
- **ORM**: SQLAlchemy
- **Authentication**: JWT tokens with PyJWT
- **Password Hashing**: Passlib with bcrypt
- **Configuration**: Pydantic Settings
- **Reliability**: PyBreaker for circuit breaker pattern

## Project Structure

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

## Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd stock-trading-api
   ```

2. **Create virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install fastapi uvicorn sqlalchemy pymysql passlib[bcrypt] python-jose[cryptography] pydantic-settings pybreaker python-multipart
   ```

4. **Environment Configuration**
   Create a `.env` file in the root directory:
   ```env
   DB_USERNAME=your_db_username
   DB_PASSWORD=your_db_password
   DB_HOST=localhost
   DB_PORT=3306
   DB_DATABASE_NAME=stock_trading_db
   
   JWT_SECRET_KEY=your-super-secret-jwt-key-here
   JWT_ALGORITHM=HS256
   JWT_ACCESS_TOKEN_EXPIRES_MINUTES=10
   JWT_REFRESH_TOKEN_EXPIRES_DAYS=7
   ```

5. **Database Setup**
   - Create a MySQL database named `stock_trading_db`
   - Ensure your MySQL server is running
   - The application will automatically create tables on startup

## Running the Application

1. **Start the development server**
   ```bash
   uvicorn app.main:app --reload
   ```

2. **Access the API**
   - API: http://localhost:8000
   - Interactive docs: http://localhost:8000/docs
   - Alternative docs: http://localhost:8000/redoc

## API Endpoints

### Authentication

- `POST /auth/register` - Register a new user
- `POST /auth/login` - Login and get tokens
- `GET /auth/refresh` - Refresh access token
- `POST /auth/logout` - Logout and revoke refresh token

### Stock Management

- `GET /stock/holdings` - Get user's stock holdings
- `GET /stock/positions` - Get user's positions
- `GET /stock/orders` - Get user's orders

### Health Check

- `GET /health` - API health status

## Database Models

### User
- `id`: Primary key
- `username`: Unique username
- `email`: Unique email address
- `hashed_password`: Bcrypt hashed password
- `created_at`, `updated_at`: Timestamps

### Holding
- `id`: Primary key
- `user_id`: Reference to user
- `symbol`: Stock symbol
- `quantity`: Number of shares
- `avg_price`: Average purchase price
- `current_price`: Current market price

### Order
- `id`: Primary key
- `user_id`: Reference to user
- `symbol`: Stock symbol
- `order_type`: BUY or SELL
- `quantity`: Number of shares
- `price`: Order price
- `status`: PENDING, EXECUTING, or CANCELED
- `timestamp`: Order timestamp
- `realized_pnl`: Realized profit/loss

### Position
- `id`: Primary key
- `user_id`: Reference to user
- `symbol`: Stock symbol
- `quantity`: Number of shares
- `entry_price`: Entry price
- `current_price`: Current market price
- `unrealized_pnl`: Unrealized profit/loss

## Authentication Flow

1. **Register**: Create account with username, email, and password
2. **Login**: Receive access token (10 min) and refresh token (7 days)
3. **Access Protected Routes**: Include access token in Authorization header
4. **Token Refresh**: Use refresh token to get new access token
5. **Logout**: Revoke refresh token

### Example Usage

```bash
# Register
curl -X POST "http://localhost:8000/auth/register" \
  -H "Content-Type: application/json" \
  -d '{"username": "testuser", "email": "test@example.com", "password": "password123"}'

# Login
curl -X POST "http://localhost:8000/auth/login" \
  -H "Content-Type: application/json" \
  -d '{"email": "test@example.com", "password": "password123"}'

# Get holdings (with authorization)
curl -X GET "http://localhost:8000/stock/holdings" \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN"
```

## Circuit Breaker

The application implements circuit breaker pattern in the stock service to handle database failures gracefully:

- **Failure Threshold**: 3 consecutive failures
- **Reset Timeout**: 10 seconds
- **Response**: HTTP 503 when circuit is open

## Development Features

### Database Seeding

The application automatically seeds the database with sample data on startup:
- Sample holdings for users
- Sample orders in executing status
- Sample positions with P&L data

### Configuration

All configuration is managed through environment variables using Pydantic Settings:
- Database connection parameters
- JWT configuration
- Application settings

## Security Features

- **Password Hashing**: Bcrypt with automatic salt generation
- **JWT Tokens**: Secure token-based authentication
- **Token Expiration**: Configurable token lifetimes
- **Token Revocation**: Refresh token blacklisting
- **Input Validation**: Pydantic schema validation
