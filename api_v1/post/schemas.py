from pydantic import BaseModel, ConfigDict

from api_v1.user.schemas import User


class PostBase(BaseModel):
    title: str
    body: str


class PostCreate(PostBase):
    pass


class PostUpdate(PostBase):
    pass


class Post(PostBase):
    model_config = ConfigDict(from_attributes=True)

    id: int


class PostGet(Post):
    user: User
