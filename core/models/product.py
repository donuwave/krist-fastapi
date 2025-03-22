from sqlalchemy.orm import Mapped, relationship

from .base import Base
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .order_product import OrderProductAssociation


class Product(Base):
    name: Mapped[str]
    price: Mapped[int]
    description: Mapped[str]

    orders_details: Mapped[list["OrderProductAssociation"]] = relationship(
        back_populates="product"
    )
