from fastapi import APIRouter, HTTPException, Depends
from datetime import datetime, timedelta, timezone

from app.dependencies import get_user_service, get_token
from app.core.security import AuthHelper
from app.schemas.user import UserRegister, UserDto, UserLogin
from app.schemas.token import Token, TokenData
from app.services.user import UserService

authRouter = APIRouter(prefix='/auth', tags=['auth'])
auth_helper = AuthHelper()

@authRouter.post('/register')
def register(userData: UserRegister, user_service: UserService = Depends(get_user_service)):
    existing_user = user_service.get_user_by_email(email=str(userData.email))
    if existing_user:
        raise HTTPException(status_code=400, detail='Email already registered')

    if user_service.get_user_by_username(username=userData.username):
        raise HTTPException(status_code=400, detail='Username already registered')

    user = user_service.create_user(userData)
    user_response = UserDto(
        email=user.email,
        username=user.username,
        id = user.id,
        created_at=user.created_at
    )

    return user_response


@authRouter.post('/login', response_model= Token)
def login(userData:UserLogin, user_service: UserService = Depends(get_user_service)):
    user = user_service.get_user_by_email(userData.email)

    if not user:
        raise HTTPException(status_code=404, detail='User not found')

    if not auth_helper.verify_password(userData.password, user.hashed_password):
        raise HTTPException(status_code=400, detail='Incorrect password')

    payload = TokenData(
        email=user.email,
        username=user.username,
        id=str(user.id)
    )
    access_token = auth_helper.encode_token(payload.model_dump(by_alias=True))
    refresh_token = auth_helper.encode_refresh_token(payload.model_dump(by_alias=True))

    expired_at = datetime.now(timezone.utc) + timedelta(days=auth_helper.refresh_token_expires_days)
    user_service.store_refresh_token(refresh_token, user.id, expired_at)

    return {
        'access_token': access_token,
        'refresh_token': refresh_token,
        'token_type': 'bearer',
    }


@authRouter.get('/refresh')
def token_refresh(
       token: str = Depends(get_token),
        user_service: UserService = Depends(get_user_service),
):
    if user_service.is_token_revoked(token):
        raise HTTPException(status_code=401, detail='Refresh token revoked')
    access_token = auth_helper.refresh_token(token)
    return {'access_token': access_token, 'token_type': 'bearer'}


@authRouter.post('/logout')
def logout(
        token: str = Depends(get_token),
        user_service: UserService = Depends(get_user_service),
):

    if user_service.is_token_revoked(token):
        raise HTTPException(status_code=401, detail='Refresh token revoked')

    if user_service.revoke_refresh_token(token):
        return {"message": "logged out successfully"}

