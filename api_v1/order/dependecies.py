from typing import Optional

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from api_v1.auth.dependencies import get_user_id_in_access_token
from api_v1.order import crud
from api_v1.order.schemas import OrderCreate
from core.models import db_helper


async def get_item_active_order(
    user_id: int = Depends(get_user_id_in_access_token),
    session: AsyncSession = Depends(db_helper.scoped_session_dependency),
) -> Optional[OrderCreate]:
    is_item_active_order = await crud.check_exist_active_order(
        session=session, user_id=user_id
    )

    if is_item_active_order:
        return await crud.get_active_item_orders(session=session, user_id=user_id)

    return await crud.create_order(session=session, user_id=user_id)
