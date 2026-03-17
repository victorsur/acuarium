from __future__ import annotations

from datetime import date, datetime
from typing import TYPE_CHECKING

from sqlalchemy import Date, DateTime, Float, ForeignKey, Integer, String, Text, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base

if TYPE_CHECKING:
    from app.models.aquarium_type import AquariumType
    from app.models.fish import Fish
    from app.models.lighting import LightingSchedule
    from app.models.maintenance_task import MaintenanceTask
    from app.models.plant import Plant


class Aquarium(Base):
    __tablename__ = "aquariums"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String(150), nullable=False)
    volume_liters: Mapped[float] = mapped_column(Float, nullable=False)
    aquarium_type_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("aquarium_types.id"), nullable=False
    )
    setup_date: Mapped[date | None] = mapped_column(Date, nullable=True)
    notes: Mapped[str | None] = mapped_column(Text, nullable=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime, server_default=func.now(), nullable=False
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime, server_default=func.now(), onupdate=func.now(), nullable=False
    )

    aquarium_type: Mapped[AquariumType] = relationship("AquariumType", lazy="joined")
    fish: Mapped[list[Fish]] = relationship(
        "Fish", back_populates="aquarium", cascade="all, delete-orphan"
    )
    plants: Mapped[list[Plant]] = relationship(
        "Plant", back_populates="aquarium", cascade="all, delete-orphan"
    )
    lighting_schedules: Mapped[list[LightingSchedule]] = relationship(
        "LightingSchedule", back_populates="aquarium", cascade="all, delete-orphan"
    )
    maintenance_tasks: Mapped[list[MaintenanceTask]] = relationship(
        "MaintenanceTask", back_populates="aquarium", cascade="all, delete-orphan"
    )
