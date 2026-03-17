from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.aquarium import Aquarium
from app.models.lighting import LightingSchedule
from app.schemas.lighting import (
    LightingScheduleCreate,
    LightingScheduleResponse,
    LightingScheduleUpdate,
)

router = APIRouter(prefix="/lighting", tags=["Lighting"])


@router.get("/", response_model=list[LightingScheduleResponse])
def list_lighting_schedules(
    aquarium_id: int | None = Query(default=None),
    db: Session = Depends(get_db),
):
    query = db.query(LightingSchedule)
    if aquarium_id is not None:
        query = query.filter(LightingSchedule.aquarium_id == aquarium_id)
    return query.all()


@router.post("/", response_model=LightingScheduleResponse, status_code=status.HTTP_201_CREATED)
def create_lighting_schedule(payload: LightingScheduleCreate, db: Session = Depends(get_db)):
    aquarium = db.query(Aquarium).filter(Aquarium.id == payload.aquarium_id).first()
    if not aquarium:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Aquarium not found.")
    obj = LightingSchedule(**payload.model_dump())
    db.add(obj)
    db.commit()
    db.refresh(obj)
    return obj


@router.get("/{lighting_id}", response_model=LightingScheduleResponse)
def get_lighting_schedule(lighting_id: int, db: Session = Depends(get_db)):
    obj = db.query(LightingSchedule).filter(LightingSchedule.id == lighting_id).first()
    if not obj:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Lighting schedule not found.")
    return obj


@router.put("/{lighting_id}", response_model=LightingScheduleResponse)
def update_lighting_schedule(
    lighting_id: int,
    payload: LightingScheduleUpdate,
    db: Session = Depends(get_db),
):
    obj = db.query(LightingSchedule).filter(LightingSchedule.id == lighting_id).first()
    if not obj:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Lighting schedule not found.")
    update_data = payload.model_dump(exclude_unset=True)
    if "aquarium_id" in update_data:
        aquarium = db.query(Aquarium).filter(Aquarium.id == update_data["aquarium_id"]).first()
        if not aquarium:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Aquarium not found.")
    for field, value in update_data.items():
        setattr(obj, field, value)
    db.commit()
    db.refresh(obj)
    return obj


@router.delete("/{lighting_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_lighting_schedule(lighting_id: int, db: Session = Depends(get_db)):
    obj = db.query(LightingSchedule).filter(LightingSchedule.id == lighting_id).first()
    if not obj:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Lighting schedule not found.")
    db.delete(obj)
    db.commit()
