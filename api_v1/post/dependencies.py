from typing import Annotated

from fastapi import Path, Depends, status, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from api_v1.post import crud
from api_v1.post.schemas import PostGet
from core.models import db_helper


async def post_by_id(
    post_id: Annotated[int, Path],
    session: AsyncSession = Depends(db_helper.scoped_session_dependency),
) -> PostGet:
    post = await crud.get_item_post(session=session, post_id=post_id)

    if post is not None:
        return post

    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Пост не найден")
