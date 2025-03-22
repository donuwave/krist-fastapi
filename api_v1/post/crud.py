from __future__ import annotations

from typing import Optional

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload

from api_v1.post.schemas import PostCreate, PostUpdate, PostGet
from core.models import Post


async def create_post(session: AsyncSession, post_in: PostCreate, user_id: int) -> Post:
    post = Post(**post_in.model_dump(), user_id=user_id)
    session.add(post)
    await session.commit()
    await session.refresh(post)
    return post


async def get_all_posts(
    session: AsyncSession, user_id: Optional[int] = None
) -> list[Post]:
    state = (
        select(Post)
        .options(joinedload(Post.user))
        .where(Post.user_id == user_id if user_id else True)
        .order_by(Post.id)
    )

    posts = await session.scalars(state)
    return list(posts)


async def get_item_post(session: AsyncSession, post_id: int) -> PostGet | None:
    state = (
        select(Post)
        .options(joinedload(Post.user))
        .where(Post.id == post_id)
        .order_by(Post.id)
    )

    post = await session.scalars(state)
    return next(post, None)


async def update_product(session: AsyncSession, post_update: PostUpdate, post: Post):
    for name, value in post_update.model_dump().items():
        setattr(post, name, value)

    await session.commit()
    return post


async def delete_post(session: AsyncSession, post: Post) -> None:
    await session.delete(post)
    await session.commit()
