from fastapi import APIRouter, Depends
from fastapi.security import HTTPBearer

from .dependencies import (
    validate_auth_user,
    get_current_auth_user,
    create_access_token,
    create_refresh_token,
    get_current_auth_user_for_refresh,
)
from .schemas import AuthBase
from ..user.crud import create_user
from ..user.schemas import User

http_bearer = HTTPBearer()
router = APIRouter(tags=["Auth"])


@router.post("/login", response_model=AuthBase)
async def auth_login(user: User = Depends(validate_auth_user)):
    access_token = await create_access_token(user=user)
    refresh_token = await create_refresh_token(user=user)
    return AuthBase(
        access_token=access_token, refresh_token=refresh_token, token_type="Bearer"
    )


@router.post("/registration", response_model=AuthBase)
async def auth_registration(user: User = Depends(create_user)):
    access_token = await create_access_token(user=user)
    refresh_token = await create_refresh_token(user=user)
    return AuthBase(
        access_token=access_token, refresh_token=refresh_token, token_type="Bearer"
    )


@router.post("/refresh", response_model=AuthBase, response_model_exclude_none=True)
async def auth_refresh(user: User = Depends(get_current_auth_user_for_refresh)):
    access_token = await create_access_token(user=user)
    return AuthBase(access_token=access_token, token_type="Bearer")


@router.get("/me")
async def auth_me(user: User = Depends(get_current_auth_user)):
    return user
