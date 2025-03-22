from typing import Optional

from pydantic import BaseModel, ConfigDict, EmailStr


class UserBase(BaseModel):
    email: EmailStr
    username: Optional[str]
    password: bytes


class User(UserBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
