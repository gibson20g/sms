from typing import AsyncGenerator, Optional
import uuid
from fastapi import Depends, HTTPException, status, Header
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.core.config import settings
from app.core.security import ALGORITHM
from app.db.session import get_db
from app.models import User, Profile

oauth2_scheme = OAuth2PasswordBearer(tokenUrl=f"{settings.API_V1_STR}/auth/login", auto_error=False)

async def get_current_user(
    db: AsyncSession = Depends(get_db),
    token: Optional[str] = Depends(oauth2_scheme)
) -> User:
    if not token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Não autenticado",
            headers={"WWW-Authenticate": "Bearer"},
        )

    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[ALGORITHM])
        user_id = payload.get("sub")
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token de acesso inválido",
            headers={"WWW-Authenticate": "Bearer"},
        )

    if not user_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Payload de token inválido",
            headers={"WWW-Authenticate": "Bearer"},
        )

    try:
        user_uuid = uuid.UUID(user_id)
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="ID de usuário inválido"
        )

    result = await db.execute(select(User).where(User.id == user_uuid))
    user = result.scalar_one_or_none()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Usuário não encontrado")
    return user

async def get_current_profile(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
    x_profile_id: Optional[str] = Header(None, alias="X-Profile-ID")
) -> Profile:
    if x_profile_id:
        try:
            profile_uuid = uuid.UUID(x_profile_id)
            result = await db.execute(
                select(Profile).where(Profile.id == profile_uuid, Profile.user_id == current_user.id)
            )
            profile = result.scalar_one_or_none()
            if profile:
                return profile
        except ValueError:
            pass

    # Default to first profile if not specified or specified profile not found
    result = await db.execute(select(Profile).where(Profile.user_id == current_user.id))
    profiles = result.scalars().all()
    if not profiles:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Usuário não possui perfis criados")
    return profiles[0]
