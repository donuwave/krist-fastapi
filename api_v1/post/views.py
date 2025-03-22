from fastapi import APIRouter, Depends, status
from fastapi.security import HTTPBearer
from sqlalchemy.ext.asyncio import AsyncSession

from core.models import db_helper
from . import crud
from .dependencies import post_by_id
from .schemas import PostGet, PostCreate, PostUpdate, Post
from ..auth.dependencies import get_user_id_in_access_token

http_bearer = HTTPBearer()
router = APIRouter(tags=["Post"], dependencies=[Depends(http_bearer)])


@router.get("/", response_model=list[PostGet])
async def get_post(
    user_id: int = Depends(get_user_id_in_access_token),
    session: AsyncSession = Depends(db_helper.scoped_session_dependency),
):
    return await crud.get_all_posts(session=session, user_id=user_id)


@router.get("/{post_id}", response_model=PostGet)
async def get_item_posts(post: Post = Depends(post_by_id)):
    return post


@router.post("/")
async def create_post(
    post_in: PostCreate,
    user_id: int = Depends(get_user_id_in_access_token),
    session: AsyncSession = Depends(db_helper.scoped_session_dependency),
):
    return await crud.create_post(session=session, post_in=post_in, user_id=user_id)


@router.put("/{post_id}", response_model=PostUpdate)
async def update_post(
    post_update: PostUpdate,
    post: Post = Depends(post_by_id),
    session: AsyncSession = Depends(db_helper.scoped_session_dependency),
):
    return await crud.update_product(
        session=session, post_update=post_update, post=post
    )


@router.delete("/{post_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_product(
    post: Post = Depends(post_by_id),
    session: AsyncSession = Depends(db_helper.scoped_session_dependency),
) -> None:
    await crud.delete_post(session=session, post=post)
