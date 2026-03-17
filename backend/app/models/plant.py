from __future__ import annotations

from datetime import date, datetime
from typing import TYPE_CHECKING

from sqlalchemy import Date, DateTime, ForeignKey, Integer, String, Text, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base

if TYPE_CHECKING:
    from app.models.aquarium import Aquarium


class Plant(Base):
    __tablename__ = "plants"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    aquarium_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("aquariums.id"), nullable=False
    )
    species: Mapped[str] = mapped_column(String(150), nullable=False)
    common_name: Mapped[str | None] = mapped_column(String(150), nullable=True)
    quantity: Mapped[int] = mapped_column(Integer, default=1, nullable=False)
    added_date: Mapped[date | None] = mapped_column(Date, nullable=True)
    notes: Mapped[str | None] = mapped_column(Text, nullable=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime, server_default=func.now(), nullable=False
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime, server_default=func.now(), onupdate=func.now(), nullable=False
    )

    aquarium: Mapped[Aquarium] = relationship("Aquarium", back_populates="plants")
