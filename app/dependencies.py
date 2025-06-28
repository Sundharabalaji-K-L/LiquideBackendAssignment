import jwt
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.services.stock import StockService
from app.services.user import UserService
from app.core.security import AuthHelper


security = HTTPBearer()
auth_helper = AuthHelper()


def get_user_service(db: Session = Depends(get_db)) -> UserService:
    return UserService(db)


def get_stock_service(db: Session = Depends(get_db)) -> StockService:
    return StockService(db)


def get_token(credentials: HTTPAuthorizationCredentials = Depends(security)) -> str:
    return credentials.credentials


def get_current_user(
        token: str = Depends(get_token),
        user_service: UserService = Depends(get_user_service)
):

    try:
        tokenData = auth_helper.decode_token(token)
        userId = int(tokenData.id)

        if not userId:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid token payload"
            )

        user = user_service.get_user_by_id(userId)

        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found"
            )

        return user

    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Expired token")

    except jwt.InvalidTokenError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token"
        )