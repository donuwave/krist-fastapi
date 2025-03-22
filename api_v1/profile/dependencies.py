from fastapi import Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from api_v1.user import crud as crud_user
from api_v1.profile import crud as crud_profile
from core.models import db_helper


async def get_base_profile(
    user_id: int, session: AsyncSession = Depends(db_helper.scoped_session_dependency)
):
    profile = await crud_profile.get_profile(session=session, user_id=user_id)

    if profile is not None:
        return profile

    user = await crud_user.get_item_users(session=session, user_id=user_id)

    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found",
        )

    return await crud_profile.create_profile(
        session=session,
        user_id=user_id,
        identity=user.id,
        email=user.email,
        username=user.username,
    )
