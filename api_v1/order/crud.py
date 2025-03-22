from typing import Optional

from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload
from sqlalchemy.engine import Result

from api_v1.order.schemas import OrderCreate, OrderGet, OrderBase
from core.models import Order, OrderProductAssociation, Product


async def create_order(session: AsyncSession, user_id: int) -> OrderCreate:
    is_item_active_order = await check_exist_active_order(
        session=session, user_id=user_id
    )

    if is_item_active_order:
        return await get_item_orders(session=session, order_id=is_item_active_order.id)

    order = Order(user_id=user_id)
    session.add(order)
    await session.commit()

    return await get_item_orders(session=session, order_id=order.id)


async def get_item_orders(
    session: AsyncSession, order_id: int
) -> Optional[OrderCreate]:
    return await session.scalar(
        select(Order)
        .where(Order.id == order_id)
        .options(selectinload(Order.user))
        .options(
            selectinload(Order.products_details).joinedload(
                OrderProductAssociation.product
            )
        )
        .order_by(Order.id)
    )


async def check_exist_active_order(
    session: AsyncSession, user_id: int
) -> Optional[OrderBase]:
    return await session.scalar(
        select(Order)
        .where(Order.user_id == user_id)
        .where(Order.order_status == "ACTIVE")
    )


async def get_active_item_orders(
    session: AsyncSession, user_id: int
) -> Optional[OrderCreate]:
    return await session.scalar(
        select(Order)
        .where(Order.user_id == user_id)
        .where(Order.order_status == "ACTIVE")
        .options(selectinload(Order.user))
        .options(
            selectinload(Order.products_details).joinedload(
                OrderProductAssociation.product
            )
        )
        .order_by(Order.id)
    )


async def get_orders(session: AsyncSession, user_id: int) -> list[OrderGet]:
    stmt = (
        select(Order)
        .where(Order.user_id == user_id)
        .options(selectinload(Order.user))
        .options(
            selectinload(Order.products_details).joinedload(
                OrderProductAssociation.product
            )
        )
        .order_by(Order.id)
    )
    result: Result = await session.execute(stmt)
    orders = result.scalars().all()
    return list(orders)


async def change_count_product(
    session: AsyncSession, count_in: int, product_id: int, order_id: int
):
    stmt = (
        update(OrderProductAssociation)
        .where(
            OrderProductAssociation.order_id == order_id,
            OrderProductAssociation.product_id == product_id,
        )
        .values(count=count_in)
    )

    await session.execute(stmt)
    await session.commit()

    await update_unit_price_for_type_product_in_order(
        session=session, order_id=order_id
    )

    return await get_item_orders(session=session, order_id=order_id)


async def update_unit_price_for_type_product_in_order(
    session: AsyncSession, order_id: int
):
    stmt = (
        update(OrderProductAssociation)
        .where(OrderProductAssociation.order_id == order_id)
        .values(
            unit_price=(
                select(Product.price * OrderProductAssociation.count)
                .where(Product.id == OrderProductAssociation.product_id)
                .scalar_subquery()
            )
        )
    )

    await session.execute(stmt)
    await session.commit()


async def delete_product_in_order(
    session: AsyncSession, order_id: int, product_id: int
) -> None:
    stmt = select(OrderProductAssociation).where(
        OrderProductAssociation.order_id == order_id,
        OrderProductAssociation.product_id == product_id,
    )
    result = await session.execute(stmt)
    association = result.scalar_one_or_none()

    await session.delete(association)
    await session.commit()
