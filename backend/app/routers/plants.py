from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.aquarium import Aquarium
from app.models.plant import Plant
from app.schemas.plant import PlantCreate, PlantResponse, PlantUpdate

router = APIRouter(prefix="/plants", tags=["Plants"])


@router.get("/", response_model=list[PlantResponse])
def list_plants(
    aquarium_id: int | None = Query(default=None),
    db: Session = Depends(get_db),
):
    query = db.query(Plant)
    if aquarium_id is not None:
        query = query.filter(Plant.aquarium_id == aquarium_id)
    return query.all()


@router.post("/", response_model=PlantResponse, status_code=status.HTTP_201_CREATED)
def create_plant(payload: PlantCreate, db: Session = Depends(get_db)):
    aquarium = db.query(Aquarium).filter(Aquarium.id == payload.aquarium_id).first()
    if not aquarium:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Aquarium not found.")
    obj = Plant(**payload.model_dump())
    db.add(obj)
    db.commit()
    db.refresh(obj)
    return obj


@router.get("/{plant_id}", response_model=PlantResponse)
def get_plant(plant_id: int, db: Session = Depends(get_db)):
    obj = db.query(Plant).filter(Plant.id == plant_id).first()
    if not obj:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Plant not found.")
    return obj


@router.put("/{plant_id}", response_model=PlantResponse)
def update_plant(plant_id: int, payload: PlantUpdate, db: Session = Depends(get_db)):
    obj = db.query(Plant).filter(Plant.id == plant_id).first()
    if not obj:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Plant not found.")
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


@router.delete("/{plant_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_plant(plant_id: int, db: Session = Depends(get_db)):
    obj = db.query(Plant).filter(Plant.id == plant_id).first()
    if not obj:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Plant not found.")
    db.delete(obj)
    db.commit()
