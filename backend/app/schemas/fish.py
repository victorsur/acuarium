from datetime import date, datetime

from pydantic import BaseModel, ConfigDict


class FishBase(BaseModel):
    aquarium_id: int
    species: str
    common_name: str | None = None
    quantity: int = 1
    added_date: date | None = None
    notes: str | None = None


class FishCreate(FishBase):
    pass


class FishUpdate(BaseModel):
    aquarium_id: int | None = None
    species: str | None = None
    common_name: str | None = None
    quantity: int | None = None
    added_date: date | None = None
    notes: str | None = None


class FishResponse(FishBase):
    id: int
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)
