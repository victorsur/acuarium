from datetime import datetime

from pydantic import BaseModel, ConfigDict


class AquariumTypeBase(BaseModel):
    name: str
    description: str | None = None


class AquariumTypeCreate(AquariumTypeBase):
    pass


class AquariumTypeUpdate(BaseModel):
    name: str | None = None
    description: str | None = None


class AquariumTypeResponse(AquariumTypeBase):
    id: int
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)
