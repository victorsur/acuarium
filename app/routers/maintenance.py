# Endpoints para la entidad Maintenance
from fastapi import APIRouter, Depends, HTTPException, status
from typing import List
from sqlalchemy.ext.asyncio import AsyncSession
from app import schemas, crud
from app.auth import get_db, get_current_user, require_admin

router = APIRouter(prefix="/maintenance", tags=["maintenance"])

@router.get("/", response_model=List[schemas.Maintenance])
async def list_maintenance(
    skip: int = 0,
    limit: int = 20,
    db: AsyncSession = Depends(get_db),
    _user=Depends(get_current_user),
):
    return await crud.get_maintenance_list(db, skip=skip, limit=limit)

@router.get("/{maintenance_id}", response_model=schemas.Maintenance)
async def get_maintenance(
    maintenance_id: int,
    db: AsyncSession = Depends(get_db),
    _user=Depends(get_current_user),
):
    maintenance = await crud.get_maintenance(db, maintenance_id)
    if not maintenance:
        raise HTTPException(status_code=404, detail="Maintenance not found")
    return maintenance

@router.post("/", response_model=schemas.Maintenance, status_code=status.HTTP_201_CREATED)
async def create_maintenance(
    maintenance: schemas.MaintenanceCreate,
    db: AsyncSession = Depends(get_db),
    _user=Depends(get_current_user),
):
    return await crud.create_maintenance(db, maintenance)

@router.put("/{maintenance_id}", response_model=schemas.Maintenance)
async def update_maintenance(
    maintenance_id: int,
    maintenance: schemas.MaintenanceUpdate,
    db: AsyncSession = Depends(get_db),
    _user=Depends(get_current_user),
):
    updated = await crud.update_maintenance(db, maintenance_id, maintenance)
    if not updated:
        raise HTTPException(status_code=404, detail="Maintenance not found")
    return updated

@router.delete("/{maintenance_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_maintenance(
    maintenance_id: int,
    db: AsyncSession = Depends(get_db),
    _admin=Depends(require_admin),
):
    deleted = await crud.delete_maintenance(db, maintenance_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Maintenance not found")
    return None
