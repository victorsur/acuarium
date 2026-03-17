from datetime import datetime, time

from pydantic import BaseModel, ConfigDict, Field


class LightingScheduleBase(BaseModel):
    aquarium_id: int
    light_type: str
    on_time: time
    off_time: time
    intensity_percent: int | None = Field(default=None, ge=0, le=100)
    notes: str | None = None


class LightingScheduleCreate(LightingScheduleBase):
    pass


class LightingScheduleUpdate(BaseModel):
    aquarium_id: int | None = None
    light_type: str | None = None
    on_time: time | None = None
    off_time: time | None = None
    intensity_percent: int | None = Field(default=None, ge=0, le=100)
    notes: str | None = None


class LightingScheduleResponse(LightingScheduleBase):
    id: int
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)
