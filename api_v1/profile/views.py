from typing import List

from fastapi import APIRouter, Depends
from fastapi.security import HTTPBearer
from sqlalchemy.ext.asyncio import AsyncSession

from core.models import db_helper
from . import crud
from .dependencies import get_base_profile
from .schemas import Profile, ProfileUpdate

http_bearer = HTTPBearer()
router = APIRouter(tags=["Profile"], dependencies=[Depends(http_bearer)])


@router.get("/{user_id}", response_model=Profile)
async def get_profile(
    profile: Profile = Depends(get_base_profile),
):
    return profile


@router.get("/", response_model=List[Profile])
async def get_profile_list(
    session: AsyncSession = Depends(db_helper.scoped_session_dependency),
):
    return await crud.get_profile_list(session=session)


@router.patch("/{user_id}", response_model=Profile)
async def update_profile(
    profile_update: ProfileUpdate,
    profile: Profile = Depends(get_base_profile),
    session: AsyncSession = Depends(db_helper.scoped_session_dependency),
):
    return await crud.update_profile(
        session=session, profile_update=profile_update, profile=profile
    )
