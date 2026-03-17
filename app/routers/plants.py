# Endpoints para la entidad Plant
from fastapi import APIRouter, Depends, HTTPException, status
from typing import List
from sqlalchemy.ext.asyncio import AsyncSession
from app import schemas, crud
from app.auth import get_db, get_current_user, require_admin

router = APIRouter(prefix="/plants", tags=["plants"])

@router.get("/", response_model=List[schemas.Plant])
async def list_plants(
    skip: int = 0,
    limit: int = 20,
    db: AsyncSession = Depends(get_db),
    _user=Depends(get_current_user),
):
    return await crud.get_plant_list(db, skip=skip, limit=limit)

@router.get("/{plant_id}", response_model=schemas.Plant)
async def get_plant(
    plant_id: int,
    db: AsyncSession = Depends(get_db),
    _user=Depends(get_current_user),
):
    plant = await crud.get_plant(db, plant_id)
    if not plant:
        raise HTTPException(status_code=404, detail="Plant not found")
    return plant

@router.post("/", response_model=schemas.Plant, status_code=status.HTTP_201_CREATED)
async def create_plant(
    plant: schemas.PlantCreate,
    db: AsyncSession = Depends(get_db),
    _user=Depends(get_current_user),
):
    return await crud.create_plant(db, plant)

@router.put("/{plant_id}", response_model=schemas.Plant)
async def update_plant(
    plant_id: int,
    plant: schemas.PlantUpdate,
    db: AsyncSession = Depends(get_db),
    _user=Depends(get_current_user),
):
    updated = await crud.update_plant(db, plant_id, plant)
    if not updated:
        raise HTTPException(status_code=404, detail="Plant not found")
    return updated

@router.delete("/{plant_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_plant(
    plant_id: int,
    db: AsyncSession = Depends(get_db),
    _admin=Depends(require_admin),
):
    deleted = await crud.delete_plant(db, plant_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Plant not found")
    return None
