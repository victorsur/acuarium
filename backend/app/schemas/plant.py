from datetime import date, datetime

from pydantic import BaseModel, ConfigDict


class PlantBase(BaseModel):
    aquarium_id: int
    species: str
    common_name: str | None = None
    quantity: int = 1
    added_date: date | None = None
    notes: str | None = None


class PlantCreate(PlantBase):
    pass


class PlantUpdate(BaseModel):
    aquarium_id: int | None = None
    species: str | None = None
    common_name: str | None = None
    quantity: int | None = None
    added_date: date | None = None
    notes: str | None = None


class PlantResponse(PlantBase):
    id: int
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)
