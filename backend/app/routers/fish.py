from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.aquarium import Aquarium
from app.models.fish import Fish
from app.schemas.fish import FishCreate, FishResponse, FishUpdate

router = APIRouter(prefix="/fish", tags=["Fish"])


@router.get("/", response_model=list[FishResponse])
def list_fish(
    aquarium_id: int | None = Query(default=None),
    db: Session = Depends(get_db),
):
    query = db.query(Fish)
    if aquarium_id is not None:
        query = query.filter(Fish.aquarium_id == aquarium_id)
    return query.all()


@router.post("/", response_model=FishResponse, status_code=status.HTTP_201_CREATED)
def create_fish(payload: FishCreate, db: Session = Depends(get_db)):
    aquarium = db.query(Aquarium).filter(Aquarium.id == payload.aquarium_id).first()
    if not aquarium:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Aquarium not found.")
    obj = Fish(**payload.model_dump())
    db.add(obj)
    db.commit()
    db.refresh(obj)
    return obj


@router.get("/{fish_id}", response_model=FishResponse)
def get_fish(fish_id: int, db: Session = Depends(get_db)):
    obj = db.query(Fish).filter(Fish.id == fish_id).first()
    if not obj:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Fish not found.")
    return obj


@router.put("/{fish_id}", response_model=FishResponse)
def update_fish(fish_id: int, payload: FishUpdate, db: Session = Depends(get_db)):
    obj = db.query(Fish).filter(Fish.id == fish_id).first()
    if not obj:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Fish not found.")
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


@router.delete("/{fish_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_fish(fish_id: int, db: Session = Depends(get_db)):
    obj = db.query(Fish).filter(Fish.id == fish_id).first()
    if not obj:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Fish not found.")
    db.delete(obj)
    db.commit()
