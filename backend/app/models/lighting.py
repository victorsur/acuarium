from __future__ import annotations

from datetime import datetime, time
from typing import TYPE_CHECKING

from sqlalchemy import DateTime, ForeignKey, Integer, String, Text, Time, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base

if TYPE_CHECKING:
    from app.models.aquarium import Aquarium


class LightingSchedule(Base):
    __tablename__ = "lighting_schedules"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    aquarium_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("aquariums.id"), nullable=False
    )
    light_type: Mapped[str] = mapped_column(String(100), nullable=False)
    on_time: Mapped[time] = mapped_column(Time, nullable=False)
    off_time: Mapped[time] = mapped_column(Time, nullable=False)
    intensity_percent: Mapped[int | None] = mapped_column(Integer, nullable=True)
    notes: Mapped[str | None] = mapped_column(Text, nullable=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime, server_default=func.now(), nullable=False
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime, server_default=func.now(), onupdate=func.now(), nullable=False
    )

    aquarium: Mapped[Aquarium] = relationship(
        "Aquarium", back_populates="lighting_schedules"
    )
