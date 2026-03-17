from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session, joinedload

from app.database import get_db
from app.models.aquarium import Aquarium
from app.models.aquarium_type import AquariumType
from app.schemas.aquarium import (
    AquariumCreate,
    AquariumDetailResponse,
    AquariumResponse,
    AquariumUpdate,
)

router = APIRouter(prefix="/aquariums", tags=["Aquariums"])


@router.get("/", response_model=list[AquariumResponse])
def list_aquariums(db: Session = Depends(get_db)):
    return db.query(Aquarium).all()


@router.post("/", response_model=AquariumResponse, status_code=status.HTTP_201_CREATED)
def create_aquarium(payload: AquariumCreate, db: Session = Depends(get_db)):
    aq_type = db.query(AquariumType).filter(AquariumType.id == payload.aquarium_type_id).first()
    if not aq_type:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Aquarium type not found.",
        )
    obj = Aquarium(**payload.model_dump())
    db.add(obj)
    db.commit()
    db.refresh(obj)
    return obj


@router.get("/{aquarium_id}", response_model=AquariumDetailResponse)
def get_aquarium(aquarium_id: int, db: Session = Depends(get_db)):
    obj = (
        db.query(Aquarium)
        .options(
            joinedload(Aquarium.aquarium_type),
            joinedload(Aquarium.fish),
            joinedload(Aquarium.plants),
        )
        .filter(Aquarium.id == aquarium_id)
        .first()
    )
    if not obj:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Aquarium not found.")
    return obj


@router.put("/{aquarium_id}", response_model=AquariumResponse)
def update_aquarium(
    aquarium_id: int,
    payload: AquariumUpdate,
    db: Session = Depends(get_db),
):
    obj = db.query(Aquarium).filter(Aquarium.id == aquarium_id).first()
    if not obj:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Aquarium not found.")
    update_data = payload.model_dump(exclude_unset=True)
    if "aquarium_type_id" in update_data:
        aq_type = db.query(AquariumType).filter(AquariumType.id == update_data["aquarium_type_id"]).first()
        if not aq_type:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Aquarium type not found.",
            )
    for field, value in update_data.items():
        setattr(obj, field, value)
    db.commit()
    db.refresh(obj)
    return obj


@router.delete("/{aquarium_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_aquarium(aquarium_id: int, db: Session = Depends(get_db)):
    obj = db.query(Aquarium).filter(Aquarium.id == aquarium_id).first()
    if not obj:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Aquarium not found.")
    db.delete(obj)
    db.commit()
