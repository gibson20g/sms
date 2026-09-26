import uuid
from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.db.session import get_db
from app.models import User, Profile
from app.schemas import ProfileCreate, ProfileUpdate, ProfileResponse
from app.api.deps import get_current_user

router = APIRouter()

@router.get("/", response_model=List[ProfileResponse])
async def list_profiles(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    stmt = select(Profile).where(Profile.user_id == current_user.id)
    result = await db.execute(stmt)
    return result.scalars().all()

@router.post("/", response_model=ProfileResponse, status_code=status.HTTP_201_CREATED)
async def create_profile(
    profile_in: ProfileCreate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    if profile_in.type not in ("pessoal", "comercial"):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Tipo de perfil inválido. Use 'pessoal' ou 'comercial'."
        )

    new_profile = Profile(
        user_id=current_user.id,
        type=profile_in.type,
        display_name=profile_in.display_name,
        bio=profile_in.bio,
        avatar_id=profile_in.avatar_id
    )
    db.add(new_profile)
    await db.commit()
    await db.refresh(new_profile)
    return new_profile

@router.get("/{profile_id}", response_model=ProfileResponse)
async def get_profile(
    profile_id: uuid.UUID,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    stmt = select(Profile).where(Profile.id == profile_id)
    result = await db.execute(stmt)
    profile = result.scalar_one_or_none()
    if not profile:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Perfil não encontrado")
    return profile

@router.put("/{profile_id}", response_model=ProfileResponse)
async def update_profile(
    profile_id: uuid.UUID,
    profile_in: ProfileUpdate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    stmt = select(Profile).where(Profile.id == profile_id, Profile.user_id == current_user.id)
    result = await db.execute(stmt)
    profile = result.scalar_one_or_none()
    if not profile:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Perfil não encontrado ou não pertence ao usuário")

    if profile_in.display_name is not None:
        profile.display_name = profile_in.display_name
    if profile_in.bio is not None:
        profile.bio = profile_in.bio
    if profile_in.avatar_id is not None:
        profile.avatar_id = profile_in.avatar_id

    await db.commit()
    await db.refresh(profile)
    return profile
