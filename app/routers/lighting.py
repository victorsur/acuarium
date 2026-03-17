# Endpoints para la entidad Lighting
from fastapi import APIRouter, Depends, HTTPException, status
from typing import List
from sqlalchemy.ext.asyncio import AsyncSession
from app import schemas, crud
from app.auth import get_db, get_current_user, require_admin

router = APIRouter(prefix="/lighting", tags=["lighting"])

@router.get("/", response_model=List[schemas.Lighting])
async def list_lighting(
    skip: int = 0,
    limit: int = 20,
    db: AsyncSession = Depends(get_db),
    _user=Depends(get_current_user),
):
    return await crud.get_lighting_list(db, skip=skip, limit=limit)

@router.get("/{lighting_id}", response_model=schemas.Lighting)
async def get_lighting(
    lighting_id: int,
    db: AsyncSession = Depends(get_db),
    _user=Depends(get_current_user),
):
    lighting = await crud.get_lighting(db, lighting_id)
    if not lighting:
        raise HTTPException(status_code=404, detail="Lighting not found")
    return lighting

@router.post("/", response_model=schemas.Lighting, status_code=status.HTTP_201_CREATED)
async def create_lighting(
    lighting: schemas.LightingCreate,
    db: AsyncSession = Depends(get_db),
    _user=Depends(get_current_user),
):
    return await crud.create_lighting(db, lighting)

@router.put("/{lighting_id}", response_model=schemas.Lighting)
async def update_lighting(
    lighting_id: int,
    lighting: schemas.LightingUpdate,
    db: AsyncSession = Depends(get_db),
    _user=Depends(get_current_user),
):
    updated = await crud.update_lighting(db, lighting_id, lighting)
    if not updated:
        raise HTTPException(status_code=404, detail="Lighting not found")
    return updated

@router.delete("/{lighting_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_lighting(
    lighting_id: int,
    db: AsyncSession = Depends(get_db),
    _admin=Depends(require_admin),
):
    deleted = await crud.delete_lighting(db, lighting_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Lighting not found")
    return None
