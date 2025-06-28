from datetime import datetime, timedelta
from urllib import response

from app.schemas.user import UserRegister, UserLogin
from app.core.security import AuthHelper
from app.models.User import RefreshToken


def test_register_user(client):
    response = client.post('/auth/register', json={
        "username": "sanjay",
        "email": "sanjay@gmail.com",
        "password": "TestPassword@123"
    })

    assert response.status_code == 200
    data = response.json()
    assert data.get("email") == "sanjay@gmail.com"
    assert data.get("username") == "sanjay"
    assert "id" in data
    assert "created_at" in data


def test_register_duplicate_user(client):
    payload = {
        "username": "sanjay",
        "email": "sanjay@gmail.com",
        "password": "TestPassword@123"
    }

    client.post('/auth/register', json=payload)
    response = client.post('/auth/register', json=payload)
    assert response.status_code == 400
    assert response.json()["detail"] == "Email already registered"


def test_login_success(client):
    client.post("/auth/register", json={
        "username": "sanjay",
        "email": "sanjay@gmail.com",
        "password": "TestPassword@123"
    })

    response = client.post('/auth/login', json={
        "email": "sanjay@gmail.com",
        "password": "TestPassword@123"
    })
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert "refresh_token" in data
    assert data['token_type'] == "bearer"


def test_login_non_existing_user(client):
    response = client.post('/auth/login', json={
        "email": "nonexisting@gmail.com",
        "password": "TestPassword@123"
    })

    assert response.status_code == 404
    assert response.json()["detail"] == "User not found"


def test_token_refresh(client):
    client.post('/auth/register', json={
        "username": "sanjay",
        "email": "sanjay@gmail.com",
        "password": "TestPassword@123"
    })

    login_response = client.post('/auth/login', json={
        "email": "sanjay@gmail.com",
        "password": "TestPassword@123"
    })

    refresh_token = login_response.json()["refresh_token"]

    response = client.get('/auth/refresh', headers={
        "Authorization": f"Bearer {refresh_token}"
    })

    assert response.status_code == 200
    assert "access_token" in response.json()


def test_refresh_token_revoked(client, db):
    client.post('/auth/register', json= {
        "username": "sanjay",
        "email": "sanjay@gmail.com",
        "password": "TestPassword@123"
    })

    login_response = client.post('/auth/login', json= {
        "email": "sanjay@gmail.com",
        "password": "TestPassword@123"
    })

    refresh_token = login_response.json()["refresh_token"]

    db_token = db.query(RefreshToken).filter(RefreshToken.token==refresh_token).first()
    db_token.revoked = True
    db.commit()

    response = client.get('/auth/refresh', headers={
        "Authorization": f"Bearer {refresh_token}"
    })

    assert response.status_code == 401
    assert response.json()["detail"] == "Refresh token revoked"


def test_logout(client):
    client.post('/auth/register', json= {
        "username": "sanjay",
        "email": "sanjay@gmail.com",
        "password": "TestPassword@123"
    })

    login_response = client.post('/auth/login', json={
        "email": "sanjay@gmail.com",
        "password": "TestPassword@123"
    })

    refresh_token = login_response.json()["refresh_token"]

    response = client.post('/auth/logout', headers={
        "Authorization": f"Bearer {refresh_token}"
    })

    assert response.status_code == 200
    assert response.json()["message"] == "logged out successfully"


def test_refresh_logged_out(client):
    client.post('/auth/register', json= {
        "username": "sanjay",
        "email": "sanjay@gmail.com",
        "password": "TestPassword@123"
    })

    login_response = client.post('/auth/login', json={
        "email": "sanjay@gmail.com",
        "password": "TestPassword@123"
    })

    refresh_token = login_response.json()["refresh_token"]

    response = client.post('/auth/logout', headers={
        "Authorization": f"Bearer {refresh_token}"
    })

    refresh_response = client.get('/auth/refresh', headers={
        "Authorization": f"Bearer {refresh_token}"
    })

    assert refresh_response.status_code == 401
    assert refresh_response.json()["detail"] == "Refresh token revoked"