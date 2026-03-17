"""
app/routers/auth.py — Endpoints de autenticación.

  POST /auth/register  → crear usuario (solo ROLE_ADMIN)
  POST /auth/login     → obtener access + refresh token
  POST /auth/refresh   → renovar access token
  GET  /auth/me        → perfil del usuario autenticado
"""

from fastapi import APIRouter, Depends, HTTPException, status
from jose import JWTError
from sqlalchemy.ext.asyncio import AsyncSession

from app import crud, schemas
from app.auth import (
    ACCESS_TOKEN_EXPIRE_MINUTES,
    create_access_token,
    create_refresh_token,
    decode_token,
    get_current_user,
    get_db,
    require_admin,
    verify_password,
)

router = APIRouter(prefix="/auth", tags=["auth"])


# ---------------------------------------------------------------------------
# POST /auth/register  —  solo ROLE_ADMIN
# ---------------------------------------------------------------------------

@router.post(
    "/register",
    response_model=schemas.UserProfile,
    status_code=status.HTTP_201_CREATED,
    summary="Registrar un nuevo usuario (solo ROLE_ADMIN)",
)
async def register(
    payload: schemas.UserRegister,
    db: AsyncSession = Depends(get_db),
    _admin=Depends(require_admin),
):
    if await crud.get_user_by_username(db, payload.username):
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Username already registered",
        )
    if await crud.get_user_by_email(db, payload.email):
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Email already registered",
        )
    return await crud.create_user(db, payload)


# ---------------------------------------------------------------------------
# POST /auth/login  —  público
# ---------------------------------------------------------------------------

@router.post(
    "/login",
    response_model=schemas.TokenResponse,
    summary="Iniciar sesión y obtener tokens JWT",
)
async def login(
    payload: schemas.UserLogin,
    db: AsyncSession = Depends(get_db),
):
    user = await crud.get_user_by_username(db, payload.username)

    if not user or not verify_password(payload.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Inactive user",
        )

    return schemas.TokenResponse(
        access_token=create_access_token(user.username, user.role),
        refresh_token=create_refresh_token(user.username, user.role),
        token_type="bearer",
        expires_in=ACCESS_TOKEN_EXPIRE_MINUTES * 60,
    )


# ---------------------------------------------------------------------------
# POST /auth/refresh  —  público
# ---------------------------------------------------------------------------

@router.post(
    "/refresh",
    response_model=schemas.TokenResponse,
    summary="Renovar el access token con el refresh token",
)
async def refresh(
    payload: schemas.TokenRefresh,
    db: AsyncSession = Depends(get_db),
):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        data = decode_token(payload.refresh_token)
        username: str = data.get("sub")
        token_type: str = data.get("type")
        if username is None or token_type != "refresh":
            raise credentials_exception
    except JWTError:
        raise credentials_exception

    user = await crud.get_user_by_username(db, username)
    if not user or not user.is_active:
        raise credentials_exception

    return schemas.TokenResponse(
        access_token=create_access_token(user.username, user.role),
        refresh_token=create_refresh_token(user.username, user.role),
        token_type="bearer",
        expires_in=ACCESS_TOKEN_EXPIRE_MINUTES * 60,
    )


# ---------------------------------------------------------------------------
# GET /auth/me  —  cualquier usuario autenticado
# ---------------------------------------------------------------------------

@router.get(
    "/me",
    response_model=schemas.UserProfile,
    summary="Perfil del usuario autenticado",
)
async def get_me(current_user=Depends(get_current_user)):
    return current_user

