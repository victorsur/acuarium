from datetime import date, datetime

from pydantic import BaseModel, ConfigDict


class MaintenanceTaskBase(BaseModel):
    aquarium_id: int
    task_type: str
    scheduled_date: date
    completed_date: date | None = None
    is_completed: bool = False
    notes: str | None = None


class MaintenanceTaskCreate(MaintenanceTaskBase):
    pass


class MaintenanceTaskUpdate(BaseModel):
    aquarium_id: int | None = None
    task_type: str | None = None
    scheduled_date: date | None = None
    completed_date: date | None = None
    is_completed: bool | None = None
    notes: str | None = None


class MaintenanceTaskResponse(MaintenanceTaskBase):
    id: int
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)
