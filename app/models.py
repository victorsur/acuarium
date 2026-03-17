# Modelos de Base de Datos (Tablas MySQL) con SQLAlchemy 2.0
from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey
from sqlalchemy.orm import relationship, DeclarativeBase
from datetime import datetime, timezone
import enum


def _utcnow() -> datetime:
    """Devuelve la hora actual en UTC (compatible con Python 3.12+)."""
    return datetime.now(timezone.utc)


class Base(DeclarativeBase):
    pass


class Acuario(Base):
    __tablename__ = "acuario"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(50), nullable=False)
    volume = Column(Integer, nullable=False)
    peces = relationship("Fish", back_populates="acuario", cascade="all, delete-orphan")
    plants = relationship("Plant", back_populates="acuario", cascade="all, delete-orphan")
    lightings = relationship("Lighting", back_populates="acuario", cascade="all, delete-orphan")
    maintenances = relationship("Maintenance", back_populates="acuario", cascade="all, delete-orphan")


class Fish(Base):
    __tablename__ = "fish"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(50), nullable=False)
    species = Column(String(50), nullable=False)
    age = Column(Integer, nullable=False)
    behavior = Column(String(100), nullable=False)
    area_of_tank = Column(String(50), nullable=False)
    picture = Column(String(255))
    acuarioId = Column(Integer, ForeignKey("acuario.id"), nullable=False)
    acuario = relationship("Acuario", back_populates="peces")


class Plant(Base):
    __tablename__ = "plant"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(50), nullable=False)
    species = Column(String(50), nullable=False)
    age = Column(Integer, nullable=False)
    picture = Column(String(255))
    acuarioId = Column(Integer, ForeignKey("acuario.id"), nullable=False)
    acuario = relationship("Acuario", back_populates="plants")
    description = Column(String(200))


class Lighting(Base):
    __tablename__ = "lighting"
    id = Column(Integer, primary_key=True, index=True)
    light_type = Column(String(30), nullable=False)
    watts = Column(Integer, nullable=False)
    wifi = Column(Boolean, nullable=False)
    start_time = Column(String(5), nullable=False)  # Formato HH:mm
    end_time = Column(String(5), nullable=False)    # Formato HH:mm
    aquariumId = Column(Integer, ForeignKey("acuario.id"), nullable=False)
    acuario = relationship("Acuario", back_populates="lightings")


class Maintenance(Base):
    __tablename__ = "maintenance"
    id = Column(Integer, primary_key=True, index=True)
    task = Column(String(100), nullable=False)
    date = Column(DateTime, nullable=False, default=_utcnow)
    acuarioId = Column(Integer, ForeignKey("acuario.id"), nullable=False)
    acuario = relationship("Acuario", back_populates="maintenances")


# ---------------------------------------------------------------------------
# User (autenticación y roles)
# ---------------------------------------------------------------------------

class UserRole(str, enum.Enum):
    ROLE_USER = "ROLE_USER"
    ROLE_ADMIN = "ROLE_ADMIN"


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, nullable=False, index=True)
    email = Column(String(100), unique=True, nullable=False)
    hashed_password = Column(String(255), nullable=False)
    role = Column(String(20), nullable=False, default=UserRole.ROLE_USER)
    is_active = Column(Boolean, nullable=False, default=True)
    created_at = Column(DateTime, nullable=False, default=_utcnow)

