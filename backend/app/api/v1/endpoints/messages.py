import uuid
from typing import List
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, and_
from sqlalchemy.orm import selectinload

from app.db.session import get_db
from app.models import Profile, ConversationParticipant, Message, MessageStatus
from app.schemas import MessageCreate, MessageResponse, MessageStatusResponse
from app.api.deps import get_current_profile
from app.core.ws_manager import manager

router = APIRouter()

@router.get("/{conversation_id}", response_model=List[MessageResponse])
async def list_messages(
    conversation_id: uuid.UUID,
    limit: int = Query(50, ge=1, le=100),
    offset: int = Query(0, ge=0),
    current_profile: Profile = Depends(get_current_profile),
    db: AsyncSession = Depends(get_db)
):
    # Verify participant
    part_stmt = select(ConversationParticipant).where(
        ConversationParticipant.conversation_id == conversation_id,
        ConversationParticipant.profile_id == current_profile.id
    )
    part_res = await db.execute(part_stmt)
    if not part_res.scalar_one_or_none():
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Acesso negado a esta conversa")

    stmt = (
        select(Message)
        .where(Message.conversation_id == conversation_id)
        .options(selectinload(Message.statuses))
        .order_by(Message.created_at.asc())
        .offset(offset)
        .limit(limit)
    )
    result = await db.execute(stmt)
    return result.scalars().all()

@router.post("/", response_model=MessageResponse, status_code=status.HTTP_201_CREATED)
async def send_message(
    msg_in: MessageCreate,
    current_profile: Profile = Depends(get_current_profile),
    db: AsyncSession = Depends(get_db)
):
    # Verify participant
    part_stmt = select(ConversationParticipant).where(
        ConversationParticipant.conversation_id == msg_in.conversation_id,
        ConversationParticipant.profile_id == current_profile.id
    )
    part_res = await db.execute(part_stmt)
    if not part_res.scalar_one_or_none():
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Acesso negado a esta conversa")

    new_msg = Message(
        conversation_id=msg_in.conversation_id,
        sender_profile_id=current_profile.id,
        content_type=msg_in.content_type,
        content_text=msg_in.content_text,
        attachment_id=msg_in.attachment_id,
        reply_to_message_id=msg_in.reply_to_message_id,
        msg_metadata=msg_in.metadata or {}
    )
    db.add(new_msg)
    await db.flush()

    # Create status for sender
    status_entry = MessageStatus(
        message_id=new_msg.id,
        profile_id=current_profile.id,
        status="enviado"
    )
    db.add(status_entry)

    # Fetch other participants to notify via WebSocket
    participants_stmt = select(ConversationParticipant).where(
        ConversationParticipant.conversation_id == msg_in.conversation_id
    )
    participants_res = await db.execute(participants_stmt)
    participants = participants_res.scalars().all()

    await db.commit()

    # Re-fetch message with loaded statuses
    stmt = (
        select(Message)
        .where(Message.id == new_msg.id)
        .options(selectinload(Message.statuses))
    )
    res = await db.execute(stmt)
    full_msg = res.scalar_one()

    # Broadcast to other online participants via WebSocket
    payload = {
        "event": "new_message",
        "data": MessageResponse.model_validate(full_msg).model_dump(mode="json")
    }
    for participant in participants:
        if participant.profile_id != current_profile.id:
            await manager.send_personal_message(payload, str(participant.profile_id))

    return full_msg

@router.post("/{message_id}/read", response_model=MessageStatusResponse)
async def mark_message_as_read(
    message_id: uuid.UUID,
    current_profile: Profile = Depends(get_current_profile),
    db: AsyncSession = Depends(get_db)
):
    msg_stmt = select(Message).where(Message.id == message_id)
    msg_res = await db.execute(msg_stmt)
    msg = msg_res.scalar_one_or_none()
    if not msg:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Mensagem não encontrada")

    status_stmt = select(MessageStatus).where(
        MessageStatus.message_id == message_id,
        MessageStatus.profile_id == current_profile.id
    )
    status_res = await db.execute(status_stmt)
    msg_status = status_res.scalar_one_or_none()

    if not msg_status:
        msg_status = MessageStatus(
            message_id=message_id,
            profile_id=current_profile.id,
            status="lido"
        )
        db.add(msg_status)
    else:
        msg_status.status = "lido"

    await db.commit()
    await db.refresh(msg_status)

    # Notify message sender via WebSocket
    read_event = {
        "event": "read_receipt",
        "data": {
            "message_id": str(message_id),
            "conversation_id": str(msg.conversation_id),
            "reader_profile_id": str(current_profile.id),
            "status": "lido"
        }
    }
    await manager.send_personal_message(read_event, str(msg.sender_profile_id))

    return msg_status
