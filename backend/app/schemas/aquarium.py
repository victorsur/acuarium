from datetime import date, datetime

from pydantic import BaseModel, ConfigDict

from app.schemas.aquarium_type import AquariumTypeResponse
from app.schemas.fish import FishResponse
from app.schemas.plant import PlantResponse


class AquariumBase(BaseModel):
    name: str
    volume_liters: float
    aquarium_type_id: int
    setup_date: date | None = None
    notes: str | None = None


class AquariumCreate(AquariumBase):
    pass


class AquariumUpdate(BaseModel):
    name: str | None = None
    volume_liters: float | None = None
    aquarium_type_id: int | None = None
    setup_date: date | None = None
    notes: str | None = None


class AquariumResponse(AquariumBase):
    id: int
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)


class AquariumDetailResponse(AquariumResponse):
    aquarium_type: AquariumTypeResponse
    fish: list[FishResponse] = []
    plants: list[PlantResponse] = []
