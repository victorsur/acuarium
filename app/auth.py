"""
app/auth.py — Núcleo de autenticación JWT.

Contiene:
  - Hashing de contraseñas (bcrypt via passlib)
  - Creación y verificación de tokens JWT (python-jose)
  - Dependencia get_db (sesión async de SQLAlchemy)
  - Dependencia get_current_user (valida Bearer token)
  - Dependencia require_admin (exige ROLE_ADMIN)
"""

import os
from datetime import datetime, timedelta, timezone
from typing import Optional

import bcrypt
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from jose import JWTError, jwt
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import AsyncSessionLocal

# ─── Configuración ────────────────────────────────────────────────────────────

SECRET_KEY: str = os.getenv("SECRET_KEY", "CHANGE_ME_IN_PRODUCTION_VERY_LONG_SECRET_KEY_32")
ALGORITHM: str = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
REFRESH_TOKEN_EXPIRE_DAYS: int = 7

# ─── Hashing de contraseñas (bcrypt directo, sin passlib) ────────────────────

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Compara una contraseña en texto plano con su hash bcrypt."""
    return bcrypt.checkpw(
        plain_password.encode("utf-8"),
        hashed_password.encode("utf-8"),
    )


def get_password_hash(password: str) -> str:
    """Genera el hash bcrypt de una contraseña (cost=12)."""
    return bcrypt.hashpw(
        password.encode("utf-8"),
        bcrypt.gensalt(12),
    ).decode("utf-8")


# ─── JWT helpers ──────────────────────────────────────────────────────────────

def _create_token(data: dict, expires_delta: timedelta) -> str:
    to_encode = data.copy()
    to_encode["exp"] = datetime.now(timezone.utc) + expires_delta
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


def create_access_token(subject: str, role: str) -> str:
    """Crea un access token JWT con expiración de 30 minutos."""
    return _create_token(
        {"sub": subject, "role": role, "type": "access"},
        timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES),
    )


def create_refresh_token(subject: str, role: str) -> str:
    """Crea un refresh token JWT con expiración de 7 días."""
    return _create_token(
        {"sub": subject, "role": role, "type": "refresh"},
        timedelta(days=REFRESH_TOKEN_EXPIRE_DAYS),
    )


def decode_token(token: str) -> dict:
    """Decodifica y verifica la firma de un JWT. Lanza JWTError si es inválido."""
    return jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])


# ─── Dependencia de base de datos ─────────────────────────────────────────────

async def get_db() -> AsyncSession:  # type: ignore[override]
    """Dependencia FastAPI: proporciona una sesión async de SQLAlchemy."""
    async with AsyncSessionLocal() as session:
        yield session


# ─── Dependencias de autenticación ────────────────────────────────────────────

_bearer_scheme = HTTPBearer()


async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(_bearer_scheme),
    db: AsyncSession = Depends(get_db),
):
    """
    Dependencia FastAPI: valida el Bearer token y devuelve el usuario activo.
    Lanza HTTP 401 si el token es inválido, expirado o el usuario no existe.
    """
    # Importación local para evitar importación circular
    from app.crud import get_user_by_username  # noqa: PLC0415

    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = decode_token(credentials.credentials)
        username: Optional[str] = payload.get("sub")
        token_type: Optional[str] = payload.get("type")
        if username is None or token_type != "access":
            raise credentials_exception
    except JWTError:
        raise credentials_exception

    user = await get_user_by_username(db, username)
    if user is None or not user.is_active:
        raise credentials_exception
    return user


async def require_admin(
    current_user=Depends(get_current_user),
):
    """
    Dependencia FastAPI: exige que el usuario tenga ROLE_ADMIN.
    Lanza HTTP 403 si el rol es insuficiente.
    """
    if current_user.role != "ROLE_ADMIN":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions",
        )
    return current_user

