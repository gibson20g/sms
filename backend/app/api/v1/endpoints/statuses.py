import uuid
from datetime import datetime, timezone
from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func, and_
from sqlalchemy.orm import selectinload

from app.db.session import get_db
from app.models import Profile, Status, StatusView, Attachment
from app.schemas import StatusCreate, StatusResponse, StatusViewResponse
from app.api.deps import get_current_profile

router = APIRouter()

@router.post("/", response_model=StatusResponse, status_code=status.HTTP_201_CREATED)
async def create_status(
    status_in: StatusCreate,
    current_profile: Profile = Depends(get_current_profile),
    db: AsyncSession = Depends(get_db)
):
    # Verify attachment exists
    att_stmt = select(Attachment).where(Attachment.id == status_in.attachment_id)
    att_res = await db.execute(att_stmt)
    if not att_res.scalar_one_or_none():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Attachment não encontrado")

    new_status = Status(
        profile_id=current_profile.id,
        attachment_id=status_in.attachment_id,
        caption=status_in.caption,
        visibility=status_in.visibility,
        catalog_item_id=status_in.catalog_item_id
    )
    db.add(new_status)
    await db.commit()

    # Re-fetch with loaded profile and attachment
    stmt = (
        select(Status)
        .where(Status.id == new_status.id)
        .options(selectinload(Status.profile), selectinload(Status.attachment))
    )
    res = await db.execute(stmt)
    full_status = res.scalar_one()

    resp = StatusResponse.model_validate(full_status)
    resp.views_count = 0
    return resp

@router.get("/", response_model=List[StatusResponse])
async def list_active_statuses(
    db: AsyncSession = Depends(get_db)
):
    now = datetime.now(timezone.utc)
    stmt = (
        select(Status)
        .where(Status.expires_at > now)
        .options(selectinload(Status.profile), selectinload(Status.attachment))
        .order_by(Status.created_at.desc())
    )
    res = await db.execute(stmt)
    statuses = res.scalars().all()

    result = []
    for st in statuses:
        # Count unique views
        cnt_stmt = select(func.count(StatusView.viewer_profile_id)).where(StatusView.status_id == st.id)
        cnt_res = await db.execute(cnt_stmt)
        views_cnt = cnt_res.scalar() or 0

        st_resp = StatusResponse.model_validate(st)
        st_resp.views_count = views_cnt
        result.append(st_resp)

    return result

@router.post("/{status_id}/view", response_model=StatusViewResponse)
async def view_status(
    status_id: uuid.UUID,
    current_profile: Profile = Depends(get_current_profile),
    db: AsyncSession = Depends(get_db)
):
    now = datetime.now(timezone.utc)
    st_stmt = select(Status).where(Status.id == status_id, Status.expires_at > now)
    st_res = await db.execute(st_stmt)
    st = st_res.scalar_one_or_none()
    if not st:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Status não encontrado ou já expirado")

    view_stmt = select(StatusView).where(
        StatusView.status_id == status_id,
        StatusView.viewer_profile_id == current_profile.id
    )
    view_res = await db.execute(view_stmt)
    existing_view = view_res.scalar_one_or_none()

    if not existing_view:
        existing_view = StatusView(
            status_id=status_id,
            viewer_profile_id=current_profile.id
        )
        db.add(existing_view)
        await db.commit()
        await db.refresh(existing_view)

    return existing_view
