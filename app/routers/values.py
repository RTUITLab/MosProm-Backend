from datetime import datetime
from fastapi import APIRouter, Depends, Response
from typing import List
from uuid import UUID

from ..database import crud, schemas
from ..dependencies import get_db

router = APIRouter(
    prefix="/values",
    tags=["Values"]
)


@router.get("/", summary="Read list of values",
            response_model=List[schemas.Value])
async def read_values(
    start: datetime = None,
    finish: datetime = None,
    db=Depends(get_db)
):
    return crud.get_values(db=db, start=start, finish=finish)


@router.post('/', status_code=201, summary="Create new value")
async def create_value(
    new_value: schemas.ValueCreate,
    db=Depends(get_db)
):
    _ = crud.create_value(db=db, new_value=new_value)
    return Response(status_code=201)


@router.delete("/{uuid}", status_code=204, summary="Remove value by uuid")
async def remove_value(uuid: UUID, db=Depends(get_db)):
    _ = crud.delete_value_by_uuid(db=db, uuid=uuid)
    return Response(status_code=204)
