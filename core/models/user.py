from .base import Base
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, LargeBinary
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .post import Post
    from .profile import Profile
    from .order import Order


class User(Base):
    email: Mapped[str] = mapped_column(String, nullable=False)
    password: Mapped[bytes] = mapped_column(LargeBinary, nullable=False)
    username: Mapped[str] = mapped_column(String(32), nullable=True)

    posts: Mapped[list["Post"]] = relationship(back_populates="user")
    profile: Mapped["Profile"] = relationship(back_populates="user")
    orders: Mapped["Order"] = relationship(back_populates="user")
