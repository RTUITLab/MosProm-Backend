from fastapi import APIRouter, Depends, HTTPException, Response
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from typing import List

from ..database import crud, schemas
from ..dependencies import get_db
from ..utils import auth
from ..utils import password as passwd


router = APIRouter(
    prefix="/users",
    tags=["Users"]
)


@router.get('/', summary="Read list of users",
            response_model=List[schemas.User],
            dependencies=[Depends(auth.get_current_user)])
async def read_users(db=Depends(get_db)):
    return crud.get_users(db=db)


@router.post('/', status_code=201, summary="Create new user",
             dependencies=[Depends(auth.get_current_user)])
async def create_user(new_user: schemas.UserCreate, db=Depends(get_db)):
    user_db = crud.get_user_by_login(db=db, login=new_user.login)
    if user_db:
        raise HTTPException(status_code=401, detail="User already exist")
    new_user.password = passwd.hash(new_user.password)
    _ = crud.create_user(db=db, new_user=new_user)
    return Response(status_code=201)


@router.post('/elevators/{mac_address}/', status_code=201,
             summary="Add new elevator for current user")
async def create_elevator(
    mac_address: str,
    current_user: schemas.User = Depends(auth.get_current_user),
    db=Depends(get_db)
):
    _ = crud.update_elevator_by_mac(
        db=db,
        mac_address=mac_address,
        user_uuid=current_user.uuid
    )
    return Response(status_code=201)


@router.post("/token/", response_model=schemas.Token,
             summary="Get access token for user")
async def get_user_token(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
):
    user_db = auth.authenticate_user(db=db, username=form_data.username,
                                     password=form_data.password)
    if not user_db:
        raise HTTPException(
            status_code=401,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    user = schemas.User.from_orm(user_db)
    user.uuid = str(user.uuid)
    access_token = auth.create_user_access_token(
        {"user": user.dict()}
    )
    return {"access_token": access_token, "token_type": "bearer"}
