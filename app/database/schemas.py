from datetime import datetime
from pydantic import BaseModel
from uuid import UUID


# region Token
class UserBase(BaseModel):
    login: str
    telegram_username: str
    company: str = None
    type: str = None
    phone_number: str = None


class UserCreate(UserBase):
    password: str


class User(UserBase):
    uuid: UUID or str
    chat_id: int = None

    class Config:
        orm_mode = True
# endregion


# region Token
class Token(BaseModel):
    access_token: str
    token_type: str
# endregion


# region Indicator
class IndicatorBase(BaseModel):
    name: str


class IndicatorCreate(IndicatorBase):
    pass


class Indicator(IndicatorBase):
    uuid: UUID or str

    class Config:
        orm_mode = True
# endregion


# region Elevetor
class ElevatorBase(BaseModel):
    title: str
    model: str
    address: str
    mac_address: str


class ElevatorCreate(ElevatorBase):
    owner_uuid: UUID = None


class Elevator(ElevatorBase):
    uuid: UUID
    owner: User = None

    class Config:
        orm_mode = True


class ElevatorIndicatorData(BaseModel):
    name: str
    min_value: float = None
    max_value: float = None
# endregion


# region ElevatorIndicator
class ElevatorIndicatorBase(BaseModel):
    min_value: float = None
    max_value: float = None


class ElevatorIndicatorCreate(ElevatorIndicatorBase):
    indicator_uuid: UUID


class ElevatorIndicator(ElevatorIndicatorBase):
    elevator: Elevator
    indicator: Indicator

    class Config:
        orm_mode = True
# endregion


# region value
class ValueBase(BaseModel):
    measured: datetime
    value: float


class ValueCreate(ValueBase):
    elevator_uuid: UUID
    indicator_uuid: UUID


class Value(ValueBase):
    uuid: UUID
    elevator: Elevator
    indicator: Indicator

    class Config:
        orm_mode = True
# endregion
