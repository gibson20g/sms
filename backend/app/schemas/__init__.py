import uuid
from datetime import datetime
from typing import Optional, List, Any, Dict
from pydantic import BaseModel, EmailStr, Field, ConfigDict

# --- Auth Schemas ---
class UserRegister(BaseModel):
    phone: Optional[str] = None
    email: Optional[EmailStr] = None
    password: str

class UserLogin(BaseModel):
    phone_or_email: str
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"

class TokenPayload(BaseModel):
    sub: Optional[str] = None

class UserResponse(BaseModel):
    id: uuid.UUID
    phone: Optional[str] = None
    email: Optional[str] = None
    auth_provider: str
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


# --- Profile Schemas ---
class ProfileCreate(BaseModel):
    type: str = Field(..., description="'pessoal' ou 'comercial'")
    display_name: str
    bio: Optional[str] = None
    avatar_id: Optional[uuid.UUID] = None

class ProfileUpdate(BaseModel):
    display_name: Optional[str] = None
    bio: Optional[str] = None
    avatar_id: Optional[uuid.UUID] = None

class ProfileResponse(BaseModel):
    id: uuid.UUID
    user_id: uuid.UUID
    type: str
    display_name: str
    bio: Optional[str] = None
    avatar_id: Optional[uuid.UUID] = None
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)


# --- Attachment Schemas ---
class AttachmentCreate(BaseModel):
    storage_url: str
    mime_type: str
    size_bytes: Optional[int] = None

class AttachmentResponse(BaseModel):
    id: uuid.UUID
    uploaded_by_profile_id: uuid.UUID
    storage_url: str
    mime_type: str
    size_bytes: Optional[int] = None
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


# --- Message Schemas ---
class MessageCreate(BaseModel):
    conversation_id: uuid.UUID
    content_type: str = Field(..., description="'texto', 'imagem', 'audio', 'documento'")
    content_text: Optional[str] = None
    attachment_id: Optional[uuid.UUID] = None
    reply_to_message_id: Optional[uuid.UUID] = None
    metadata: Dict[str, Any] = Field(default_factory=dict, description="Metadata em JSONB ex: waveform, duração de áudio, dados de pedido")

class MessageStatusResponse(BaseModel):
    message_id: uuid.UUID
    profile_id: uuid.UUID
    status: str
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)

class MessageResponse(BaseModel):
    id: uuid.UUID
    conversation_id: uuid.UUID
    sender_profile_id: uuid.UUID
    content_type: str
    content_text: Optional[str] = None
    attachment_id: Optional[uuid.UUID] = None
    reply_to_message_id: Optional[uuid.UUID] = None
    metadata: Dict[str, Any] = Field(default_factory=dict, validation_alias="msg_metadata")
    created_at: datetime
    statuses: List[MessageStatusResponse] = []

    model_config = ConfigDict(from_attributes=True, populate_by_name=True)


# --- Conversation Schemas ---
class ParticipantCreate(BaseModel):
    profile_id: uuid.UUID
    role: str = "membro"

class ParticipantResponse(BaseModel):
    conversation_id: uuid.UUID
    profile_id: uuid.UUID
    role: str
    joined_at: datetime
    muted: bool
    profile: Optional[ProfileResponse] = None

    model_config = ConfigDict(from_attributes=True)

class ConversationCreate(BaseModel):
    kind: str = Field(..., description="'direta' ou 'grupo'")
    context: str = Field("pessoal", description="'pessoal' ou 'negocio'")
    tag: Optional[str] = Field(None, description="'cliente', 'fornecedor', 'familia', 'amigos', 'orcamento', 'evento'")
    title: Optional[str] = None
    avatar_id: Optional[uuid.UUID] = None
    participant_profile_ids: List[uuid.UUID] = Field(default_factory=list)

class ConversationResponse(BaseModel):
    id: uuid.UUID
    kind: str
    context: str
    tag: Optional[str] = None
    title: Optional[str] = None
    avatar_id: Optional[uuid.UUID] = None
    created_at: datetime
    participants: List[ParticipantResponse] = []
    last_message: Optional[MessageResponse] = None

    model_config = ConfigDict(from_attributes=True)


# --- Status / Stories Schemas ---
class StatusCreate(BaseModel):
    attachment_id: uuid.UUID
    caption: Optional[str] = None
    visibility: str = Field("publico", description="'publico' ou 'privado'")
    catalog_item_id: Optional[uuid.UUID] = None

class StatusViewResponse(BaseModel):
    status_id: uuid.UUID
    viewer_profile_id: uuid.UUID
    viewed_at: datetime

    model_config = ConfigDict(from_attributes=True)

class StatusResponse(BaseModel):
    id: uuid.UUID
    profile_id: uuid.UUID
    attachment_id: uuid.UUID
    caption: Optional[str] = None
    visibility: str
    catalog_item_id: Optional[uuid.UUID] = None
    created_at: datetime
    expires_at: datetime
    views_count: int = 0
    profile: Optional[ProfileResponse] = None
    attachment: Optional[AttachmentResponse] = None

    model_config = ConfigDict(from_attributes=True)
