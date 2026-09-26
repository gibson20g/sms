from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, or_
from app.db.session import get_db
from app.models import User, Profile, UserSettings
from app.schemas import UserRegister, UserLogin, Token, UserResponse
from app.core.security import get_password_hash, verify_password, create_access_token
from app.api.deps import get_current_user

router = APIRouter()

@router.post("/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def register(user_in: UserRegister, db: AsyncSession = Depends(get_db)):
    if not user_in.phone and not user_in.email:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="É necessário fornecer telefone ou e-mail"
        )

    # Check if user exists
    conditions = []
    if user_in.phone:
        conditions.append(User.phone == user_in.phone)
    if user_in.email:
        conditions.append(User.email == user_in.email)

    stmt = select(User).where(or_(*conditions))
    result = await db.execute(stmt)
    existing_user = result.scalar_one_or_none()

    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Usuário com este telefone ou e-mail já existe"
        )

    hashed_pwd = get_password_hash(user_in.password)
    new_user = User(
        phone=user_in.phone,
        email=user_in.email,
        hashed_password=hashed_pwd,
        auth_provider="password"
    )
    db.add(new_user)
    await db.flush()

    # Create default settings
    user_settings = UserSettings(user_id=new_user.id)
    db.add(user_settings)

    # Create default personal profile
    default_name = user_in.phone or (user_in.email.split("@")[0] if user_in.email else "Novo Usuário")
    default_profile = Profile(
        user_id=new_user.id,
        type="pessoal",
        display_name=default_name
    )
    db.add(default_profile)

    await db.commit()
    await db.refresh(new_user)
    return new_user

@router.post("/login", response_model=Token)
async def login(login_in: UserLogin, db: AsyncSession = Depends(get_db)):
    stmt = select(User).where(
        or_(User.phone == login_in.phone_or_email, User.email == login_in.phone_or_email)
    )
    result = await db.execute(stmt)
    user = result.scalar_one_or_none()

    if not user or not user.hashed_password or not verify_password(login_in.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Credenciais inválidas"
        )

    access_token = create_access_token(subject=user.id)
    return Token(access_token=access_token, token_type="bearer")

@router.get("/me", response_model=UserResponse)
async def get_me(current_user: User = Depends(get_current_user)):
    return current_user
