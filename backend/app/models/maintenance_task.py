from __future__ import annotations

from datetime import date, datetime
from typing import TYPE_CHECKING

from sqlalchemy import Boolean, Date, DateTime, ForeignKey, Integer, String, Text, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base

if TYPE_CHECKING:
    from app.models.aquarium import Aquarium


class MaintenanceTask(Base):
    __tablename__ = "maintenance_tasks"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    aquarium_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("aquariums.id"), nullable=False
    )
    task_type: Mapped[str] = mapped_column(String(100), nullable=False)
    scheduled_date: Mapped[date] = mapped_column(Date, nullable=False)
    completed_date: Mapped[date | None] = mapped_column(Date, nullable=True)
    is_completed: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    notes: Mapped[str | None] = mapped_column(Text, nullable=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime, server_default=func.now(), nullable=False
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime, server_default=func.now(), onupdate=func.now(), nullable=False
    )

    aquarium: Mapped[Aquarium] = relationship(
        "Aquarium", back_populates="maintenance_tasks"
    )
