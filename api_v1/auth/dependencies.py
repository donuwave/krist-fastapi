from datetime import timedelta

from asyncpg.pgproto.pgproto import timedelta
from fastapi import Form, HTTPException, status, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.ext.asyncio import AsyncSession

from .helpers import (
    create_token,
    validate_token_type,
    ACCESS_TOKEN_TYPE,
    REFRESH_TOKEN_TYPE,
)
from api_v1.user import crud as user_crud

from api_v1.auth.utils import validate_password, decode_jwt
from api_v1.user.crud import get_item_users_by_email
from api_v1.user.schemas import User
from core.config import settings
from core.models import db_helper

http_bearer = HTTPBearer()


async def create_access_token(user: User) -> str:
    jwt_payload = {"email": user.email, "user_id": user.id, "sub": user.email}
    return await create_token(
        token_type=ACCESS_TOKEN_TYPE,
        token_data=jwt_payload,
        expire_minutes=settings.auth.access_token_expire_minutes,
    )


async def create_refresh_token(user: User) -> str:
    jwt_payload = {"sub": user.email, "user_id": user.id}
    return await create_token(
        token_type=REFRESH_TOKEN_TYPE,
        token_data=jwt_payload,
        expire_timedelta=timedelta(days=settings.auth.refresh_token_expire_days),
    )


async def get_current_token_payload(
    credentials: HTTPAuthorizationCredentials = Depends(http_bearer),
) -> User:
    token = credentials.credentials
    payload = decode_jwt(token=token)
    return payload


async def get_user_id_in_access_token(
    payload: dict = Depends(get_current_token_payload),
) -> int:
    return payload.get("user_id")


async def get_current_auth_user(
    payload: dict = Depends(get_current_token_payload),
    session: AsyncSession = Depends(db_helper.scoped_session_dependency),
) -> User:
    validate_token_type(token_type=ACCESS_TOKEN_TYPE, payload=payload)

    user_id: int = payload.get("user_id")
    user = await user_crud.get_item_users(session=session, user_id=user_id)

    if user is not None:
        print(user)
        return user

    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED, detail="token not found"
    )


async def get_current_auth_user_for_refresh(
    payload: dict = Depends(get_current_token_payload),
    session: AsyncSession = Depends(db_helper.scoped_session_dependency),
) -> User:
    validate_token_type(token_type=REFRESH_TOKEN_TYPE, payload=payload)

    user_id: int = payload.get("user_id")
    user = await user_crud.get_item_users(session=session, user_id=user_id)

    if user is not None:
        return user

    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED, detail="token not found"
    )


async def validate_auth_user(
    user: User = Depends(get_item_users_by_email),
    password: str = Form(),
):
    authed_exc = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED, detail="Неверный логин или пароль"
    )

    if not user:
        raise authed_exc

    if not validate_password(password_user=password, hashed_password=user.password):
        raise authed_exc

    return user
