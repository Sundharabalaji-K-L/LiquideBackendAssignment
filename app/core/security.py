from passlib.context import CryptContext
from fastapi import HTTPException, status
from datetime import datetime, timedelta, timezone
import jwt

from app.config import settings
from app.schemas.token import TokenData


class AuthHelper:
    hasher = CryptContext(schemes=['bcrypt'], deprecated='auto')
    secret_key = settings.JWT_SECRET_KEY
    algorithm = settings.JWT_ALGORITHM
    access_token_expires_minutes = settings.JWT_ACCESS_TOKEN_EXPIRES_MINUTES
    refresh_token_expires_days = settings.JWT_REFRESH_TOKEN_EXPIRES_DAYS

    def get_password_hash(self, password: str) -> str:
        return self.hasher.hash(password)

    def verify_password(self, password: str, hashed_password: str) -> bool:
        return self.hasher.verify(password, hashed_password)

    def encode_token(self, userData: dict) -> str:
        payload = userData.copy()

        expires = datetime.now(timezone.utc) + timedelta(minutes=self.access_token_expires_minutes)
        iat = datetime.now(timezone.utc)

        payload.update({'iat': iat, 'exp': expires})

        return jwt.encode(payload, self.secret_key, algorithm=self.algorithm)

    def decode_token(self, token: str) -> TokenData:
        try:
            payload = jwt.decode(token, self.secret_key, algorithms=[self.algorithm])

            if payload:
                return TokenData(
                    id=payload.get('sub'),
                    email=payload.get('email'),
                    username=payload.get('username'),
                )

            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Invalid Token')

        except jwt.ExpiredSignatureError:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Token Expired')

        except jwt.InvalidTokenError:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Invalid Token')

    def encode_refresh_token(self, userData: dict) -> str:
        payload = userData.copy()
        expires = datetime.now(timezone.utc) + timedelta(days=self.refresh_token_expires_days)
        iat = datetime.now(timezone.utc)

        payload.update({'iat': iat, 'exp': expires})
        return jwt.encode(payload, self.secret_key, algorithm=self.algorithm)

    def refresh_token(self, refresh_token: str) -> str:
        try:
            payload = jwt.decode(refresh_token, self.secret_key, algorithms=[self.algorithm])

            if payload:
                to_encode = {
                    'sub': payload.get('sub'),
                    'username': payload.get('username'),
                    'email': payload.get('email'),
                }

                return self.encode_token(to_encode)

            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Invalid Token')

        except jwt.ExpiredSignatureError:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Token Expired')

        except jwt.InvalidTokenError:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Invalid Token')
