from datetime import date

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.aquarium import Aquarium
from app.models.maintenance_task import MaintenanceTask
from app.schemas.maintenance_task import (
    MaintenanceTaskCreate,
    MaintenanceTaskResponse,
    MaintenanceTaskUpdate,
)

router = APIRouter(prefix="/maintenance-tasks", tags=["Maintenance Tasks"])


@router.get("/", response_model=list[MaintenanceTaskResponse])
def list_maintenance_tasks(
    aquarium_id: int | None = Query(default=None),
    is_completed: bool | None = Query(default=None),
    db: Session = Depends(get_db),
):
    query = db.query(MaintenanceTask)
    if aquarium_id is not None:
        query = query.filter(MaintenanceTask.aquarium_id == aquarium_id)
    if is_completed is not None:
        query = query.filter(MaintenanceTask.is_completed == is_completed)
    return query.all()


@router.post("/", response_model=MaintenanceTaskResponse, status_code=status.HTTP_201_CREATED)
def create_maintenance_task(payload: MaintenanceTaskCreate, db: Session = Depends(get_db)):
    aquarium = db.query(Aquarium).filter(Aquarium.id == payload.aquarium_id).first()
    if not aquarium:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Aquarium not found.")
    obj = MaintenanceTask(**payload.model_dump())
    db.add(obj)
    db.commit()
    db.refresh(obj)
    return obj


@router.get("/{task_id}", response_model=MaintenanceTaskResponse)
def get_maintenance_task(task_id: int, db: Session = Depends(get_db)):
    obj = db.query(MaintenanceTask).filter(MaintenanceTask.id == task_id).first()
    if not obj:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Maintenance task not found.")
    return obj


@router.put("/{task_id}", response_model=MaintenanceTaskResponse)
def update_maintenance_task(
    task_id: int,
    payload: MaintenanceTaskUpdate,
    db: Session = Depends(get_db),
):
    obj = db.query(MaintenanceTask).filter(MaintenanceTask.id == task_id).first()
    if not obj:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Maintenance task not found.")
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


@router.delete("/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_maintenance_task(task_id: int, db: Session = Depends(get_db)):
    obj = db.query(MaintenanceTask).filter(MaintenanceTask.id == task_id).first()
    if not obj:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Maintenance task not found.")
    db.delete(obj)
    db.commit()


@router.patch("/{task_id}/complete", response_model=MaintenanceTaskResponse)
def complete_maintenance_task(task_id: int, db: Session = Depends(get_db)):
    obj = db.query(MaintenanceTask).filter(MaintenanceTask.id == task_id).first()
    if not obj:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Maintenance task not found.")
    obj.is_completed = True
    obj.completed_date = date.today()
    db.commit()
    db.refresh(obj)
    return obj
