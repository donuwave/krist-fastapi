from typing import Annotated

from fastapi import APIRouter, Depends, Path
from fastapi.security import HTTPBearer
from sqlalchemy.ext.asyncio import AsyncSession

from api_v1.auth.dependencies import get_user_id_in_access_token
from api_v1.order import crud as crud_order
from api_v1.order.dependecies import get_item_active_order
from api_v1.order.schemas import OrderCreate, OrderGet
from api_v1.product import crud as crud_product
from core.models import db_helper, Order, OrderProductAssociation

http_bearer = HTTPBearer()
router = APIRouter(tags=["Order"], dependencies=[Depends(http_bearer)])


@router.get("/", response_model=list[OrderGet])
async def get_orders(
    user_id: int = Depends(get_user_id_in_access_token),
    session: AsyncSession = Depends(db_helper.scoped_session_dependency),
):
    return await crud_order.get_orders(session=session, user_id=user_id)


@router.get("/{order_id}", response_model=OrderGet)
async def get_item_orders(
    order_id: Annotated[int, Path],
    session: AsyncSession = Depends(db_helper.scoped_session_dependency),
):
    return await crud_order.get_item_orders(
        session=session,
        order_id=order_id,
    )


# TODO active-order
@router.post("/active_order", response_model=OrderCreate)
async def get_item_active(active_order: OrderCreate = Depends(get_item_active_order)):
    return active_order


# Этот end-point создает новый активный заказ, если он уже есть, то просто его возвращает
@router.post("/", response_model=OrderCreate)
async def create_order(
    user_id: int = Depends(get_user_id_in_access_token),
    session: AsyncSession = Depends(db_helper.scoped_session_dependency),
):
    return await crud_order.create_order(session=session, user_id=user_id)


@router.post("/add-product")
async def add_product_in_order(
    product_id: int,
    active_order: OrderCreate = Depends(get_item_active_order),
    session: AsyncSession = Depends(db_helper.scoped_session_dependency),
):
    product = await crud_product.get_item_products(
        session=session, product_id=product_id
    )

    # TODO исправить
    active_order.products_details.append(
        OrderProductAssociation(product=product, count=1)
    )

    await session.commit()

    await crud_order.update_unit_price_for_type_product_in_order(
        order_id=active_order.id, session=session
    )


@router.delete("/delete-product")
async def delete_product(
    product_id: int,
    order_id: int,
    session: AsyncSession = Depends(db_helper.scoped_session_dependency),
):
    return await crud_order.delete_product_in_order(
        order_id=order_id, product_id=product_id, session=session
    )


@router.post("/change-count")
async def change_count_product(
    count_in: int,
    product_id: int,
    order_id: int,
    session: AsyncSession = Depends(db_helper.scoped_session_dependency),
):
    if count_in <= 0:
        await crud_order.delete_product_in_order(
            order_id=order_id, product_id=product_id, session=session
        )

    return await crud_order.change_count_product(
        product_id=product_id, order_id=order_id, session=session, count_in=count_in
    )
