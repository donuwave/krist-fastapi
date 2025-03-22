from typing import Annotated

from fastapi import Path, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from api_v1.user import crud
from core.models import db_helper


async def user_by_id(
    user_id: Annotated[int, Path],
    session: AsyncSession = Depends(db_helper.scoped_session_dependency),
):
    user = await crud.get_item_users(session=session, user_id=user_id)

    if user is not None:
        return user

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND, detail=f"Пользователь не найден"
    )
