from datetime import datetime
from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.core.security import AuthHelper
from app.models.User import User, RefreshToken
from app.schemas.user import UserRegister


class UserService:
    def __init__(self, db: Session):
        self.db: Session = db
        self.auth_helper: AuthHelper = AuthHelper()

    def get_user_by_email(self, email: str) -> User | None:
        return self.db.query(User).filter(User.email == email).first()


    def get_user_by_username(self, username: str) -> User | None:
        return self.db.query(User).filter(User.username == username).first()


    def get_user_by_id(self, user_id: int) -> User | None:
        return self.db.query(User).filter(User.id == user_id).first()


    def create_user(self, userData: UserRegister) -> User:
        hashed_password = self.auth_helper.get_password_hash(userData.password)
        new_user = User(
            username=userData.username,
            email=str(userData.email),
            hashed_password=hashed_password,
        )

        self.db.add(new_user)
        self.db.commit()
        self.db.refresh(new_user)

        return new_user


    def store_refresh_token(self, token: str, user_id: int, expired_at: datetime):
        db_token = RefreshToken(token=token, user_id=user_id, expired_at=expired_at)
        self.db.add(db_token)
        self.db.commit()
        self.db.refresh(db_token)

        return db_token

    def is_token_revoked(self, token: str) -> bool:
        db_token = self.db.query(RefreshToken).filter_by(token=token).first()
        if not db_token:

            raise HTTPException(status_code=404, detail="Refresh token not found")
        return bool(db_token.revoked)

    def revoke_refresh_token(self, token: str) -> bool:
        db_token = self.db.query(RefreshToken).filter_by(token=token).first()

        if not db_token:
            raise HTTPException(status_code=404, detail="Invalid token")

        db_token.revoked = True
        self.db.commit()
        self.db.refresh(db_token)
        return bool(db_token.revoked)


