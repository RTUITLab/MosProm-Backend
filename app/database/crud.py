from datetime import datetime
from typing import List
from uuid import UUID
from sqlalchemy.orm import Session

from . import models, schemas


# region User
def create_user(db: Session, new_user: schemas.UserCreate):
    db_user = models.User(**new_user.dict())
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return


def get_user_by_login(db: Session, login: str) -> models.User:
    return db.query(models.User).filter_by(login=login).first()


def get_users(db: Session):
    return db.query(models.User).all()
# endregion


# region Indicator
def create_indicator(db: Session, new_indicator: schemas.IndicatorCreate):
    db_indicator = models.Indicator(**new_indicator.dict())
    db.add(db_indicator)
    db.commit()
    db.refresh(db_indicator)
    return


def get_indicators(db: Session, uuid: UUID = None):
    return db.query(models.Indicator).all()


def get_elevator_indicators(db: Session, uuid: UUID):
    query = db.query(
        models.Indicator.name,
        models.ElevatorIndicator.min_value,
        models.ElevatorIndicator.max_value
    ).join(models.ElevatorIndicator).\
        filter(models.ElevatorIndicator.elevator_uuid == uuid)
    return query.all()


def get_indicator_by_name(db: Session, name: str):
    return db.query(models.Indicator).filter_by(name=name).first()


def delete_indicator_by_uuid(db: Session, uuid: UUID):
    _ = db.query(models.Indicator).filter_by(uuid=uuid).delete()
    db.commit()
    return
# endregion


# region Elevator
def create_elevator(db: Session, new_elevator: schemas.ElevatorCreate):
    db_elevator = models.Elevator(**new_elevator.dict())
    db.add(db_elevator)
    db.commit()
    db.refresh(db_elevator)
    return


def update_elevator_by_mac(db: Session, mac_address: str, user_uuid: UUID):
    _ = db.query(models.Elevator).\
        filter_by(mac_address=mac_address).update({"owner_uuid": user_uuid})
    db.commit()
    return


def get_elevators(db: Session, owner_uuid: UUID = None):
    query = db.query(models.Elevator)
    if owner_uuid:
        query = query.filter_by(owner_uuid=owner_uuid)
    return query.all()


def delete_elevator_for_user(db: Session, uuid: UUID):
    _ = db.query(models.Elevator).filter_by(uuid=uuid).\
        update({"owner_uuid": None})
    db.commit()
    return


def create_elevator_indicators(
    db: Session,
    uuid: UUID,
    indicators: List[schemas.ElevatorIndicatorCreate]
):
    for indicator in indicators:
        db_elevator_indicator = models.ElevatorIndicator(
            elevator_uuid=uuid,
            **indicator.dict()
        )
        db.add(db_elevator_indicator)
    db.commit()
    return
# endregion


# region Value
def create_value(db: Session, new_value: schemas.ValueCreate):
    db_value = models.Value(**new_value.dict())
    db.add(db_value)
    db.commit()
    db.refresh(db_value)
    return


def get_values(db: Session, start: datetime = None, finish: datetime = None):
    query = db.query(models.Value)
    if start:
        query = query.filter(models.Value.measured >= start)
    if finish:
        query = query.filter(models.Value.measured <= finish)
    return query.all()


def delete_value_by_uuid(db: Session, uuid: UUID):
    _ = db.query(models.Value).filter_by(uuid=uuid).delete()
    db.commit()
    return
# endregion
