from datetime import datetime

from sqlalchemy import func, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base

from typing import TYPE_CHECKING

from .mixins import UserRelationMixin

if TYPE_CHECKING:
    from .order_product import OrderProductAssociation


class Order(UserRelationMixin, Base):
    _user_back_populates = "orders"

    promocode: Mapped[str] = mapped_column(String, nullable=True)
    created_at: Mapped[datetime] = mapped_column(
        server_default=func.now(), default=datetime.now
    )
    order_status: Mapped[str] = mapped_column(
        String, nullable=False, server_default="ACTIVE"
    )

    products_details: Mapped[list["OrderProductAssociation"]] = relationship(
        back_populates="order"
    )
