from typing import Optional

from pydantic import BaseModel, EmailStr, Field, ConfigDict


class ProfileBase(BaseModel):
    email: EmailStr
    username: Optional[str] = None
    firstname: Optional[str] = None
    surname: Optional[str] = None
    age: Optional[int] = None
    gender: Optional[int] = Field(
        ..., description="Пол: 1 - мужской, 2 - женский", ge=1, le=2
    )


class Profile(ProfileBase):
    model_config = ConfigDict(from_attributes=True)

    id: int


class ProfileUpdate(Profile):
    email: Optional[EmailStr] = None
    gender: Optional[int] = None
