# Endpoints para la entidad Acuario
from fastapi import APIRouter, Depends, HTTPException, status
from typing import List
from sqlalchemy.ext.asyncio import AsyncSession
from app import schemas, crud
from app.auth import get_db, get_current_user, require_admin

router = APIRouter(prefix="/acuario", tags=["acuario"])

@router.get("/", response_model=List[schemas.Acuario])
async def list_acuarios(
    skip: int = 0,
    limit: int = 20,
    db: AsyncSession = Depends(get_db),
    _user=Depends(get_current_user),
):
    return await crud.get_acuario_list(db, skip=skip, limit=limit)

@router.get("/{acuario_id}", response_model=schemas.Acuario)
async def get_acuario(
    acuario_id: int,
    db: AsyncSession = Depends(get_db),
    _user=Depends(get_current_user),
):
    acuario = await crud.get_acuario(db, acuario_id)
    if not acuario:
        raise HTTPException(status_code=404, detail="Acuario not found")
    return acuario

@router.post("/", response_model=schemas.Acuario, status_code=status.HTTP_201_CREATED)
async def create_acuario(
    acuario: schemas.AcuarioCreate,
    db: AsyncSession = Depends(get_db),
    _user=Depends(get_current_user),
):
    return await crud.create_acuario(db, acuario)

@router.put("/{acuario_id}", response_model=schemas.Acuario)
async def update_acuario(
    acuario_id: int,
    acuario: schemas.AcuarioUpdate,
    db: AsyncSession = Depends(get_db),
    _user=Depends(get_current_user),
):
    updated = await crud.update_acuario(db, acuario_id, acuario)
    if not updated:
        raise HTTPException(status_code=404, detail="Acuario not found")
    return updated

@router.delete("/{acuario_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_acuario(
    acuario_id: int,
    db: AsyncSession = Depends(get_db),
    _admin=Depends(require_admin),
):
    deleted = await crud.delete_acuario(db, acuario_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Acuario not found")
    return None
