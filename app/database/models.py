import uuid

from datetime import datetime
from sqlalchemy import Column, DateTime, Float, ForeignKey, Integer, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from .database import DataBase


class User(DataBase):
    __tablename__ = "user"

    uuid = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    login = Column(String, nullable=False, unique=True)
    password = Column(String, nullable=False)
    telegram_username = Column(String, nullable=False)
    company = Column(String)
    type = Column(String)
    chat_id = Column(Integer)
    phone_number = Column(String)


class Elevator(DataBase):
    __tablename__ = "elevator"

    uuid = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    title = Column(String, nullable=False)
    model = Column(String, nullable=False)
    address = Column(String, nullable=False)
    mac_address = Column(String, nullable=False)
    owner_uuid = Column(UUID(as_uuid=True), ForeignKey("user.uuid"))

    owner = relationship("User")


class Indicator(DataBase):
    __tablename__ = "indicator"

    uuid = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String)


class Value(DataBase):
    __tablename__ = "value"

    uuid = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    elevator_uuid = Column(UUID(as_uuid=True), ForeignKey("elevator.uuid"),
                           nullable=False)
    indicator_uuid = Column(UUID(as_uuid=True), ForeignKey("indicator.uuid"),
                            nullable=False)
    measured = Column(DateTime, default=datetime.now, nullable=False)
    value = Column(Float, nullable=False)

    elevator = relationship("Elevator")
    indicator = relationship("Indicator")


class ElevatorIndicator(DataBase):
    __tablename__ = "elevator_indicator"

    elevator_uuid = Column(UUID(as_uuid=True), ForeignKey("elevator.uuid"),
                           primary_key=True)
    indicator_uuid = Column(UUID(as_uuid=True), ForeignKey("indicator.uuid"),
                            primary_key=True)
    min_value = Column(Float)
    max_value = Column(Float)

    elevator = relationship("Elevator")
    indicator = relationship("Indicator")
