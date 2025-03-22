from .base import Base
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String, Integer, CheckConstraint

from .mixins import UserRelationMixin


class Profile(UserRelationMixin, Base):
    _user_back_populates = "profile"
    _user_id_unique = True

    email: Mapped[str] = mapped_column(String, nullable=False)
    username: Mapped[str] = mapped_column(String(32), nullable=True)
    firstname: Mapped[str] = mapped_column(String(32), nullable=True)
    surname: Mapped[str] = mapped_column(String(32), nullable=True)
    age: Mapped[int] = mapped_column(Integer, nullable=True)
    gender: Mapped[int] = mapped_column(
        Integer, CheckConstraint("gender IN (1, 2)"), nullable=True
    )
