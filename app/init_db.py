"""
Script para crear las tablas automáticamente y sembrar el usuario admin por defecto.

Uso:
    python -m app.init_db

El usuario admin por defecto se configura con variables de entorno:
    ADMIN_USERNAME  (default: admin)
    ADMIN_EMAIL     (default: admin@acuarium.local)
    ADMIN_PASSWORD  (default: Admin1234!)  ← cámbiala en producción
"""
import asyncio
import os

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.database import engine
from app.models import Base, User, UserRole
from app.auth import get_password_hash


async def init_models() -> None:
    """Crea todas las tablas si no existen."""
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    print("✓ Tablas creadas / verificadas correctamente.")


async def create_default_admin() -> None:
    """Crea el usuario admin por defecto si no existe ningún admin."""
    username = os.getenv("ADMIN_USERNAME", "admin")
    email    = os.getenv("ADMIN_EMAIL",    "admin@acuarium.local")
    password = os.getenv("ADMIN_PASSWORD", "Admin1234!")

    from app.database import AsyncSessionLocal
    async with AsyncSessionLocal() as db:
        result = await db.execute(
            select(User).where(User.username == username)
        )
        existing = result.scalar_one_or_none()
        if existing:
            print(f"✓ Usuario admin '{username}' ya existe — no se crea de nuevo.")
            return

        admin = User(
            username=username,
            email=email,
            hashed_password=get_password_hash(password),
            role=UserRole.ROLE_ADMIN,
            is_active=True,
        )
        db.add(admin)
        await db.commit()
        print(f"✓ Usuario admin '{username}' creado con rol ROLE_ADMIN.")
        print("  ⚠  Cambia la contraseña en producción (variable ADMIN_PASSWORD).")


async def main() -> None:
    await init_models()
    await create_default_admin()


if __name__ == "__main__":
    asyncio.run(main())
