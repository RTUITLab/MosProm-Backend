import uuid
from fastapi import APIRouter, Depends, Response
from typing import List
from uuid import UUID

from ..database import crud, schemas
from ..dependencies import get_db
from ..utils import auth

router = APIRouter(
    prefix="/elevators",
    tags=["Elevators"]
)


@router.get("/", summary="Read list of elevators for current user",
            response_model=List[schemas.Elevator])
async def read_elevators(
    current_user: schemas.User = Depends(auth.get_current_user),
    db=Depends(get_db)
):
    return crud.get_elevators(db=db, uuid=current_user.uuid)


@router.post("/{uuid}/indicators/", status_code=201,
             summary="Create list of indicators",
             dependencies=[Depends(auth.get_current_user)])
async def create_elevator_indicators(
    indicators: List[schemas.ElevatorIndicatorCreate],
    db=Depends(get_db)
):
    crud.create_elevator_indicators(db=db, uuid=uuid, indicators=indicators)
    return Response(status_code=201)


@router.delete("/{uuid}", status_code=204,
               summary="Remove elevator by uuid for current user",
               dependencies=[Depends(auth.get_current_user)])
async def remove_elevator(uuid: UUID, db=Depends(get_db)):
    crud.delete_elevator_for_user(db=db, uuid=uuid)
    return Response(status_code=204)
