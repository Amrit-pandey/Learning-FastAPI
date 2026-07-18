from datetime import datetime
from pydantic import BaseModel, ConfigDict, Field, EmailStr


class BaseUser(BaseModel):
    username: str = Field(min_length=1, max_length=50)
    email: EmailStr = Field(max_length=50)


class UserCreate(BaseUser):
    pass


class UserResponse(BaseUser):
    model_config = ConfigDict(from_attributes=True)

    id: int
    image_file: str | None
    image_path: str


class UserUpdate(BaseUser):
    username: str | None = Field(default=None, min_length=1, max_length=50)
    email: EmailStr | None = Field(default=None, max_length=50)
    image_file: str | None = Field(default=None, max_length=200)


class PostBase(BaseModel):
    title: str = Field(min_length=1, max_length=100)
    content: str = Field(min_length=1)


class PostCreate(PostBase):
    user_id: int


class PostUpdate(PostBase):
    title: str | None = Field(min_length=1, max_length=100, default=None)
    content: str | None = Field(min_length=1, default=None)


class PostResponse(PostBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    user_id: int
    date_posted: datetime
    author: UserResponse
