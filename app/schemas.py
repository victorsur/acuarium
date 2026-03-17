from pydantic import BaseModel, Field, ConfigDict, EmailStr
from typing import Optional
from datetime import datetime


# ---------------------------------------------------------------------------
# Maintenance Schemas
# ---------------------------------------------------------------------------

class MaintenanceBase(BaseModel):
    task: str = Field(..., min_length=3, max_length=100, examples=["Cambio de agua"])
    date: datetime = Field(..., examples=["2024-03-16T10:00:00"])
    acuarioId: int = Field(..., examples=[1], description="ID del acuario al que pertenece")


class MaintenanceCreate(MaintenanceBase):
    pass


class MaintenanceUpdate(MaintenanceBase):
    pass


class Maintenance(MaintenanceBase):
    model_config = ConfigDict(
        from_attributes=True,
        json_schema_extra={
            "example": {
                "id": 10,
                "task": "Cambio de agua",
                "date": "2024-03-16T10:00:00",
                "acuarioId": 1,
            }
        },
    )
    id: int = Field(..., examples=[10])


# ---------------------------------------------------------------------------
# Fish Schemas
# ---------------------------------------------------------------------------

class FishBase(BaseModel):
    name: str = Field(..., min_length=2, max_length=50, examples=["Nemo"])
    species: str = Field(..., min_length=2, max_length=50, examples=["Amphiprioninae"])
    age: int = Field(..., ge=0, le=20, examples=[2])
    behavior: str = Field(..., min_length=2, max_length=100, examples=["Pacífico"])
    area_of_tank: str = Field(..., min_length=2, max_length=50, examples=["Zona media"])
    picture: Optional[str] = Field(None, examples=["https://example.com/nemo.jpg"])
    acuarioId: int = Field(..., examples=[1])


class FishCreate(FishBase):
    pass


class FishUpdate(FishBase):
    pass


class Fish(FishBase):
    model_config = ConfigDict(
        from_attributes=True,
        json_schema_extra={
            "example": {
                "id": 5,
                "name": "Nemo",
                "species": "Amphiprioninae",
                "age": 2,
                "behavior": "Pacífico",
                "area_of_tank": "Zona media",
                "picture": "https://example.com/nemo.jpg",
                "acuarioId": 1,
            }
        },
    )
    id: int = Field(..., examples=[5])


# ---------------------------------------------------------------------------
# Plant Schemas
# ---------------------------------------------------------------------------

class PlantBase(BaseModel):
    name: str = Field(..., min_length=2, max_length=50, examples=["Anubias"])
    species: str = Field(..., min_length=2, max_length=50, examples=["Anubias barteri"])
    age: int = Field(..., ge=0, le=10, examples=[1])
    picture: Optional[str] = Field(None, examples=["https://example.com/anubias.jpg"])
    acuarioId: int = Field(..., examples=[1])
    description: Optional[str] = Field(None, max_length=200, examples=["Planta resistente y de bajo mantenimiento."])


class PlantCreate(PlantBase):
    pass


class PlantUpdate(PlantBase):
    pass


class Plant(PlantBase):
    model_config = ConfigDict(
        from_attributes=True,
        json_schema_extra={
            "example": {
                "id": 3,
                "name": "Anubias",
                "species": "Anubias barteri",
                "age": 1,
                "picture": "https://example.com/anubias.jpg",
                "acuarioId": 1,
                "description": "Planta resistente y de bajo mantenimiento.",
            }
        },
    )
    id: int = Field(..., examples=[3])


# ---------------------------------------------------------------------------
# Acuario Schemas
# ---------------------------------------------------------------------------

class AcuarioBase(BaseModel):
    name: str = Field(..., min_length=2, max_length=50, examples=["Acuario principal"])
    volume: int = Field(..., ge=1, le=10000, examples=[200])


class AcuarioCreate(AcuarioBase):
    pass


class AcuarioUpdate(AcuarioBase):
    pass


class Acuario(AcuarioBase):
    model_config = ConfigDict(
        from_attributes=True,
        json_schema_extra={
            "example": {
                "id": 1,
                "name": "Acuario principal",
                "volume": 200,
            }
        },
    )
    id: int = Field(..., examples=[1])


# ---------------------------------------------------------------------------
# Lighting Schemas
# ---------------------------------------------------------------------------

TIME_PATTERN = r"^([01]\d|2[0-3]):[0-5]\d$"


class LightingBase(BaseModel):
    light_type: str = Field(..., min_length=2, max_length=30, examples=["LED"])
    watts: int = Field(..., ge=1, le=1000, examples=[20])
    wifi: bool = Field(..., examples=[True])
    start_time: str = Field(..., pattern=TIME_PATTERN, examples=["08:00"], description="Formato HH:mm")
    end_time: str = Field(..., pattern=TIME_PATTERN, examples=["20:00"], description="Formato HH:mm")
    aquariumId: int = Field(..., examples=[1])


class LightingCreate(LightingBase):
    pass


class LightingUpdate(LightingBase):
    pass


class Lighting(LightingBase):
    model_config = ConfigDict(
        from_attributes=True,
        json_schema_extra={
            "example": {
                "id": 2,
                "light_type": "LED",
                "watts": 20,
                "wifi": True,
                "start_time": "08:00",
                "end_time": "20:00",
                "aquariumId": 1,
            }
        },
    )
    id: int = Field(..., examples=[2])


# ---------------------------------------------------------------------------
# Auth Schemas
# ---------------------------------------------------------------------------

class UserRegister(BaseModel):
    """Datos para registrar un nuevo usuario. Solo ROLE_ADMIN puede usarlo."""
    username: str = Field(..., min_length=3, max_length=50, examples=["victor"])
    email: EmailStr = Field(..., examples=["victor@example.com"])
    password: str = Field(
        ..., min_length=8, examples=["Secret1234!"],
        description="Mínimo 8 caracteres, al menos una mayúscula y un número",
    )
    role: str = Field(default="ROLE_USER", examples=["ROLE_USER"])


class UserLogin(BaseModel):
    """Credenciales para iniciar sesión."""
    username: str = Field(..., examples=["victor"])
    password: str = Field(..., examples=["Secret1234!"])


class UserProfile(BaseModel):
    """Perfil público del usuario (sin contraseña)."""
    model_config = ConfigDict(from_attributes=True)

    id: int = Field(..., examples=[1])
    username: str = Field(..., examples=["victor"])
    email: str = Field(..., examples=["victor@example.com"])
    role: str = Field(..., examples=["ROLE_USER"])
    is_active: bool = Field(..., examples=[True])
    created_at: datetime = Field(..., examples=["2026-03-16T10:00:00"])


class TokenResponse(BaseModel):
    """Tokens JWT devueltos tras login o refresh exitoso."""
    access_token: str
    refresh_token: str
    token_type: str = "bearer"
    expires_in: int = Field(default=1800, description="Segundos hasta expiración del access_token")


class TokenRefresh(BaseModel):
    """Body para renovar el access_token."""
    refresh_token: str = Field(..., examples=["eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."])

