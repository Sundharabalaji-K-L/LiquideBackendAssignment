# 📈 Liquide Backend Assessment

This project is a FastAPI-based backend service for handling authentication and stock data (holdings, positions, and orders). It uses MySQL as the database and is containerized using Docker and Docker Compose.

---

## 🐳 Running the Application (Docker Compose)

### 1. 🧾 Prerequisites

- Docker 🐳
- Docker Compose

---

### 2. 🏗️ Build and Start the Application

```bash
docker-compose up --build
```

### 3. 🛑 Stop the Application

```bash
docker-compose down
```

---

## 🌐 Endpoints

The following endpoints are available in the application:

- **/auth/register**  
  Register a new user account.

- **/auth/login**  
  Authenticate a user and return a token.

- **/auth/logout**  
  Log out a user and invalidate the token.

- **/stock/positions**  
  Retrieve the user's current stock positions.

- **/stock/orders**  
  Retrieve user's stock orders.

- **/stock/holdings**  
  Retrieve the user's stock holdings.

