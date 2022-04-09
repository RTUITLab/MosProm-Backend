from sqlalchemy.orm import Session

from . import models, schemas


def create_user(db: Session, new_user: schemas.UserCreate):
    db_user = models.User(**new_user.dict())
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return


def get_user_by_login(db: Session, login: str):
    return db.query(models.User).filter_by(login=login).first()


def get_users(db: Session):
    return db.query(models.User).all()
