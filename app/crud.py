from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import List, Optional
from app import models, schemas


# ---------------------------------------------------------------------------
# CRUD para User
# ---------------------------------------------------------------------------

async def get_user_by_username(db: AsyncSession, username: str) -> Optional[models.User]:
    result = await db.execute(select(models.User).where(models.User.username == username))
    return result.scalar_one_or_none()


async def get_user_by_email(db: AsyncSession, email: str) -> Optional[models.User]:
    result = await db.execute(select(models.User).where(models.User.email == email))
    return result.scalar_one_or_none()


async def create_user(db: AsyncSession, user_in: schemas.UserRegister) -> models.User:
    from app.auth import get_password_hash  # importación local para evitar circular
    db_user = models.User(
        username=user_in.username,
        email=user_in.email,
        hashed_password=get_password_hash(user_in.password),
        role=user_in.role,
        is_active=True,
    )
    db.add(db_user)
    await db.commit()
    await db.refresh(db_user)
    return db_user


async def get_fish(db: AsyncSession, fish_id: int) -> Optional[models.Fish]:
    result = await db.execute(select(models.Fish).where(models.Fish.id == fish_id))
    return result.scalar_one_or_none()

async def get_fish_list(db: AsyncSession, skip: int = 0, limit: int = 20) -> List[models.Fish]:
    result = await db.execute(select(models.Fish).offset(skip).limit(limit))
    return result.scalars().all()

async def create_fish(db: AsyncSession, fish: schemas.FishCreate) -> models.Fish:
    db_fish = models.Fish(**fish.model_dump())
    db.add(db_fish)
    await db.commit()
    await db.refresh(db_fish)
    return db_fish

async def update_fish(db: AsyncSession, fish_id: int, fish: schemas.FishUpdate) -> Optional[models.Fish]:
    db_fish = await get_fish(db, fish_id)
    if not db_fish:
        return None
    for key, value in fish.model_dump(exclude_unset=True).items():
        setattr(db_fish, key, value)
    await db.commit()
    await db.refresh(db_fish)
    return db_fish

async def delete_fish(db: AsyncSession, fish_id: int) -> bool:
    db_fish = await get_fish(db, fish_id)
    if not db_fish:
        return False
    await db.delete(db_fish)
    await db.commit()
    return True

# --- CRUD para Plant ---
async def get_plant(db: AsyncSession, plant_id: int) -> Optional[models.Plant]:
    result = await db.execute(select(models.Plant).where(models.Plant.id == plant_id))
    return result.scalar_one_or_none()

async def get_plant_list(db: AsyncSession, skip: int = 0, limit: int = 20) -> List[models.Plant]:
    result = await db.execute(select(models.Plant).offset(skip).limit(limit))
    return result.scalars().all()

async def create_plant(db: AsyncSession, plant: schemas.PlantCreate) -> models.Plant:
    db_plant = models.Plant(**plant.model_dump())
    db.add(db_plant)
    await db.commit()
    await db.refresh(db_plant)
    return db_plant

async def update_plant(db: AsyncSession, plant_id: int, plant: schemas.PlantUpdate) -> Optional[models.Plant]:
    db_plant = await get_plant(db, plant_id)
    if not db_plant:
        return None
    for key, value in plant.model_dump(exclude_unset=True).items():
        setattr(db_plant, key, value)
    await db.commit()
    await db.refresh(db_plant)
    return db_plant

async def delete_plant(db: AsyncSession, plant_id: int) -> bool:
    db_plant = await get_plant(db, plant_id)
    if not db_plant:
        return False
    await db.delete(db_plant)
    await db.commit()
    return True

# --- CRUD para Acuario ---
async def get_acuario(db: AsyncSession, acuario_id: int) -> Optional[models.Acuario]:
    result = await db.execute(select(models.Acuario).where(models.Acuario.id == acuario_id))
    return result.scalar_one_or_none()

async def get_acuario_list(db: AsyncSession, skip: int = 0, limit: int = 20) -> List[models.Acuario]:
    result = await db.execute(select(models.Acuario).offset(skip).limit(limit))
    return result.scalars().all()

async def create_acuario(db: AsyncSession, acuario: schemas.AcuarioCreate) -> models.Acuario:
    db_acuario = models.Acuario(**acuario.model_dump())
    db.add(db_acuario)
    await db.commit()
    await db.refresh(db_acuario)
    return db_acuario

async def update_acuario(db: AsyncSession, acuario_id: int, acuario: schemas.AcuarioUpdate) -> Optional[models.Acuario]:
    db_acuario = await get_acuario(db, acuario_id)
    if not db_acuario:
        return None
    for key, value in acuario.model_dump(exclude_unset=True).items():
        setattr(db_acuario, key, value)
    await db.commit()
    await db.refresh(db_acuario)
    return db_acuario

async def delete_acuario(db: AsyncSession, acuario_id: int) -> bool:
    db_acuario = await get_acuario(db, acuario_id)
    if not db_acuario:
        return False
    await db.delete(db_acuario)
    await db.commit()
    return True

# --- CRUD para Lighting ---
async def get_lighting(db: AsyncSession, lighting_id: int) -> Optional[models.Lighting]:
    result = await db.execute(select(models.Lighting).where(models.Lighting.id == lighting_id))
    return result.scalar_one_or_none()

async def get_lighting_list(db: AsyncSession, skip: int = 0, limit: int = 20) -> List[models.Lighting]:
    result = await db.execute(select(models.Lighting).offset(skip).limit(limit))
    return result.scalars().all()

async def create_lighting(db: AsyncSession, lighting: schemas.LightingCreate) -> models.Lighting:
    db_lighting = models.Lighting(**lighting.model_dump())
    db.add(db_lighting)
    await db.commit()
    await db.refresh(db_lighting)
    return db_lighting

async def update_lighting(db: AsyncSession, lighting_id: int, lighting: schemas.LightingUpdate) -> Optional[models.Lighting]:
    db_lighting = await get_lighting(db, lighting_id)
    if not db_lighting:
        return None
    for key, value in lighting.model_dump(exclude_unset=True).items():
        setattr(db_lighting, key, value)
    await db.commit()
    await db.refresh(db_lighting)
    return db_lighting

async def delete_lighting(db: AsyncSession, lighting_id: int) -> bool:
    db_lighting = await get_lighting(db, lighting_id)
    if not db_lighting:
        return False
    await db.delete(db_lighting)
    await db.commit()
    return True

# --- CRUD para Maintenance ---
async def get_maintenance(db: AsyncSession, maintenance_id: int) -> Optional[models.Maintenance]:
    result = await db.execute(select(models.Maintenance).where(models.Maintenance.id == maintenance_id))
    return result.scalar_one_or_none()

async def get_maintenance_list(db: AsyncSession, skip: int = 0, limit: int = 20) -> List[models.Maintenance]:
    result = await db.execute(select(models.Maintenance).offset(skip).limit(limit))
    return result.scalars().all()

async def create_maintenance(db: AsyncSession, maintenance: schemas.MaintenanceCreate) -> models.Maintenance:
    db_maintenance = models.Maintenance(**maintenance.model_dump())
    db.add(db_maintenance)
    await db.commit()
    await db.refresh(db_maintenance)
    return db_maintenance

async def update_maintenance(db: AsyncSession, maintenance_id: int, maintenance: schemas.MaintenanceUpdate) -> Optional[models.Maintenance]:
    db_maintenance = await get_maintenance(db, maintenance_id)
    if not db_maintenance:
        return None
    for key, value in maintenance.model_dump(exclude_unset=True).items():
        setattr(db_maintenance, key, value)
    await db.commit()
    await db.refresh(db_maintenance)
    return db_maintenance

async def delete_maintenance(db: AsyncSession, maintenance_id: int) -> bool:
    db_maintenance = await get_maintenance(db, maintenance_id)
    if not db_maintenance:
        return False
    await db.delete(db_maintenance)
    await db.commit()
    return True
