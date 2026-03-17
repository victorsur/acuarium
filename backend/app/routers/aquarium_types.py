from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.aquarium_type import AquariumType
from app.schemas.aquarium_type import (
    AquariumTypeCreate,
    AquariumTypeResponse,
    AquariumTypeUpdate,
)

router = APIRouter(prefix="/aquarium-types", tags=["Aquarium Types"])


@router.get("/", response_model=list[AquariumTypeResponse])
def list_aquarium_types(db: Session = Depends(get_db)):
    return db.query(AquariumType).all()


@router.post("/", response_model=AquariumTypeResponse, status_code=status.HTTP_201_CREATED)
def create_aquarium_type(payload: AquariumTypeCreate, db: Session = Depends(get_db)):
    existing = db.query(AquariumType).filter(AquariumType.name == payload.name).first()
    if existing:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"Aquarium type with name '{payload.name}' already exists.",
        )
    obj = AquariumType(**payload.model_dump())
    db.add(obj)
    db.commit()
    db.refresh(obj)
    return obj


@router.get("/{aquarium_type_id}", response_model=AquariumTypeResponse)
def get_aquarium_type(aquarium_type_id: int, db: Session = Depends(get_db)):
    obj = db.query(AquariumType).filter(AquariumType.id == aquarium_type_id).first()
    if not obj:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Aquarium type not found.")
    return obj


@router.put("/{aquarium_type_id}", response_model=AquariumTypeResponse)
def update_aquarium_type(
    aquarium_type_id: int,
    payload: AquariumTypeUpdate,
    db: Session = Depends(get_db),
):
    obj = db.query(AquariumType).filter(AquariumType.id == aquarium_type_id).first()
    if not obj:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Aquarium type not found.")
    update_data = payload.model_dump(exclude_unset=True)
    if "name" in update_data:
        conflict = (
            db.query(AquariumType)
            .filter(AquariumType.name == update_data["name"], AquariumType.id != aquarium_type_id)
            .first()
        )
        if conflict:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=f"Aquarium type with name '{update_data['name']}' already exists.",
            )
    for field, value in update_data.items():
        setattr(obj, field, value)
    db.commit()
    db.refresh(obj)
    return obj


@router.delete("/{aquarium_type_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_aquarium_type(aquarium_type_id: int, db: Session = Depends(get_db)):
    obj = db.query(AquariumType).filter(AquariumType.id == aquarium_type_id).first()
    if not obj:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Aquarium type not found.")
    db.delete(obj)
    db.commit()
