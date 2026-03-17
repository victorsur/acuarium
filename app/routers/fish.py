# Endpoints para la entidad Fish
from fastapi import APIRouter, Depends, HTTPException, status
from typing import List
from sqlalchemy.ext.asyncio import AsyncSession
from app import schemas, crud
from app.auth import get_db, get_current_user, require_admin

router = APIRouter(prefix="/fish", tags=["fish"])

@router.get("/", response_model=List[schemas.Fish])
async def list_fish(
    skip: int = 0,
    limit: int = 20,
    db: AsyncSession = Depends(get_db),
    _user=Depends(get_current_user),
):
    return await crud.get_fish_list(db, skip=skip, limit=limit)

@router.get("/{fish_id}", response_model=schemas.Fish)
async def get_fish(
    fish_id: int,
    db: AsyncSession = Depends(get_db),
    _user=Depends(get_current_user),
):
    fish = await crud.get_fish(db, fish_id)
    if not fish:
        raise HTTPException(status_code=404, detail="Fish not found")
    return fish

@router.post("/", response_model=schemas.Fish, status_code=status.HTTP_201_CREATED)
async def create_fish(
    fish: schemas.FishCreate,
    db: AsyncSession = Depends(get_db),
    _user=Depends(get_current_user),
):
    return await crud.create_fish(db, fish)

@router.put("/{fish_id}", response_model=schemas.Fish)
async def update_fish(
    fish_id: int,
    fish: schemas.FishUpdate,
    db: AsyncSession = Depends(get_db),
    _user=Depends(get_current_user),
):
    updated = await crud.update_fish(db, fish_id, fish)
    if not updated:
        raise HTTPException(status_code=404, detail="Fish not found")
    return updated

@router.delete("/{fish_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_fish(
    fish_id: int,
    db: AsyncSession = Depends(get_db),
    _admin=Depends(require_admin),
):
    deleted = await crud.delete_fish(db, fish_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Fish not found")
    return None
