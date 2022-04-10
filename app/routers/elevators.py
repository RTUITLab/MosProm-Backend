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
    owner_uuid: UUID = None,
    db=Depends(get_db)
):
    return crud.get_elevators(db=db, owner_uuid=owner_uuid)


@router.get("/{uuid}/indicators/",
            response_model=List[schemas.ElevatorIndicatorData],
            summary="Read list of indicators for elevator by elevator's uuid",
            dependencies=[Depends(auth.get_current_user)])
async def create_elevator_indicators(
    uuid: UUID,
    db=Depends(get_db)
):
    return crud.get_elevator_indicators(db=db, uuid=uuid)


@router.post("/{uuid}/indicators/", status_code=201,
             summary="Create list of indicators",
             dependencies=[Depends(auth.get_current_user)])
async def create_indicators(
    uuid: UUID,
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
