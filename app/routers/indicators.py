from fastapi import APIRouter, Depends, HTTPException, Response
from uuid import UUID

from ..database import crud, schemas
from ..dependencies import get_db

router = APIRouter(
    prefix="/indicators",
    tags=["Indicators"]
)


@router.get("/", summary="Read list of indicators")
async def read_indicators(name: str = None, db=Depends(get_db)):
    return crud.get_indicators(db=db, name=name)


@router.post('/', status_code=201, summary="Create new indicator")
async def create_indicator(
    new_indicator: schemas.IndicatorCreate,
    db=Depends(get_db)
):
    indicator_db = crud.get_indicator_by_name(db=db, name=new_indicator.name)
    if indicator_db:
        raise HTTPException(status_code=401, detail="Indicator already exist")
    _ = crud.create_indicator(db=db, new_indicator=new_indicator)
    return Response(status_code=201)


@router.delete("/{uuid}", status_code=204, summary="Remove indicator by uuid")
async def remove_indicator(uuid: UUID, db=Depends(get_db)):
    _ = crud.delete_indicator_by_uuid(db=db, uuid=uuid)
    return Response(status_code=204)
