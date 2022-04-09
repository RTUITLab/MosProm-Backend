from pydantic import BaseModel
from typing import Optional
from uuid import UUID


class UserBase(BaseModel):
    login: str
    first_name: str
    second_name: str
    phone_number: str


class UserCreate(UserBase):
    password: str


class User(UserBase):
    uuid: UUID or str

    class Config:
        orm_mode = True


# region Token
class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: Optional[str] = None
# endregion
