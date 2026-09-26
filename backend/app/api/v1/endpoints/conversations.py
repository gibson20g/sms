import uuid
from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, and_
from sqlalchemy.orm import selectinload

from app.db.session import get_db
from app.models import Profile, Conversation, ConversationParticipant, Message
from app.schemas import ConversationCreate, ConversationResponse, MessageResponse
from app.api.deps import get_current_profile

router = APIRouter()

@router.get("/", response_model=List[ConversationResponse])
async def list_conversations(
    context: Optional[str] = Query(None, description="Filtro por contexto: 'pessoal' ou 'negocio'"),
    tag: Optional[str] = Query(None, description="Filtro por tag: 'cliente', 'familia', etc."),
    current_profile: Profile = Depends(get_current_profile),
    db: AsyncSession = Depends(get_db)
):
    stmt = (
        select(Conversation)
        .join(ConversationParticipant, ConversationParticipant.conversation_id == Conversation.id)
        .where(ConversationParticipant.profile_id == current_profile.id)
        .options(selectinload(Conversation.participants).selectinload(ConversationParticipant.profile))
    )

    if context:
        stmt = stmt.where(Conversation.context == context)
    if tag:
        stmt = stmt.where(Conversation.tag == tag)

    stmt = stmt.order_by(Conversation.created_at.desc())
    result = await db.execute(stmt)
    conversations = result.scalars().unique().all()

    response_list = []
    for conv in conversations:
        # Get last message for each conversation
        msg_stmt = (
            select(Message)
            .where(Message.conversation_id == conv.id)
            .order_by(Message.created_at.desc())
            .limit(1)
        )
        msg_res = await db.execute(msg_stmt)
        last_msg = msg_res.scalar_one_or_none()

        conv_dict = ConversationResponse.model_validate(conv)
        if last_msg:
            conv_dict.last_message = MessageResponse.model_validate(last_msg)
        response_list.append(conv_dict)

    return response_list

@router.post("/", response_model=ConversationResponse, status_code=status.HTTP_201_CREATED)
async def create_conversation(
    conv_in: ConversationCreate,
    current_profile: Profile = Depends(get_current_profile),
    db: AsyncSession = Depends(get_db)
):
    if conv_in.kind not in ("direta", "grupo"):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Tipo de conversa inválido ('direta' ou 'grupo')")

    new_conv = Conversation(
        kind=conv_in.kind,
        context=conv_in.context,
        tag=conv_in.tag,
        title=conv_in.title,
        avatar_id=conv_in.avatar_id
    )
    db.add(new_conv)
    await db.flush()

    # Ensure current profile is added as admin/participant
    all_participant_ids = set(conv_in.participant_profile_ids)
    all_participant_ids.add(current_profile.id)

    for p_id in all_participant_ids:
        role = "admin" if p_id == current_profile.id else "membro"
        part = ConversationParticipant(
            conversation_id=new_conv.id,
            profile_id=p_id,
            role=role
        )
        db.add(part)

    await db.commit()

    # Re-fetch with loaded participants
    stmt = (
        select(Conversation)
        .where(Conversation.id == new_conv.id)
        .options(selectinload(Conversation.participants).selectinload(ConversationParticipant.profile))
    )
    result = await db.execute(stmt)
    created_conv = result.scalar_one()
    return created_conv
