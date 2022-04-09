import uuid

from sqlalchemy import Column, String
from sqlalchemy.dialects.postgresql import UUID

from .database import DataBase


class User(DataBase):
    __tablename__ = "message"

    uuid = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    login = Column(String(), nullable=False)
    password = Column(String(), nullable=False)
    first_name = Column(String())
    second_name = Column(String())
    phone_number = Column(String())
