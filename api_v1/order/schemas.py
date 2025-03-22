from datetime import datetime
from enum import Enum
from typing import Optional

from pydantic import BaseModel

from api_v1.product.schemas import Product
from api_v1.user.schemas import UserBase


class OrderStatus(str, Enum):
    ACTIVE = "ACTIVE"  # Активный заказ, в который сейчас складывают товары
    CREATED = "CREATED"  # Оформленный заказ
    COMPLETED = "COMPLETED"  # Полученный заказ
    CANCELED = "CANCELED"  # Отмененный заказ


class OrderProductAssociationBase(BaseModel):
    id: int
    product_id: int
    order_id: int
    unit_price: int
    count: int
    product: Product


class OrderBase(BaseModel):
    id: int
    promocode: Optional[str]
    order_status: OrderStatus
    created_at: datetime
    user_id: int


class Order(OrderBase):
    pass


class OrderGet(OrderBase):
    user: UserBase
    products_details: list[OrderProductAssociationBase] = []


class OrderCreate(OrderBase):
    user: UserBase
    products_details: list[OrderProductAssociationBase] = []
