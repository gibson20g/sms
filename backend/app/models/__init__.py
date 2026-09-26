import uuid
from datetime import datetime, timedelta, timezone
from typing import Optional, List
from sqlalchemy import (
    String, Text, Boolean, Integer, BigInteger, DateTime, ForeignKey, CheckConstraint, PrimaryKeyConstraint, JSON
)
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.dialects.postgresql import UUID as PG_UUID, JSONB
from sqlalchemy.types import TypeDecorator, CHAR
from app.db.base import Base

def utcnow():
    return datetime.now(timezone.utc)

class GUID(TypeDecorator):
    """Platform-independent GUID type.
    Uses PostgreSQL's UUID type, otherwise uses CHAR(36), storing as stringified hex values.
    """
    impl = CHAR
    cache_ok = True

    def load_dialect_impl(self, dialect):
        if dialect.name == 'postgresql':
            return dialect.type_descriptor(PG_UUID(as_uuid=True))
        else:
            return dialect.type_descriptor(CHAR(36))

    def process_bind_param(self, value, dialect):
        if value is None:
            return value
        elif dialect.name == 'postgresql':
            return str(value)
        else:
            if not isinstance(value, uuid.UUID):
                return str(uuid.UUID(value))
            else:
                return str(value)

    def process_result_value(self, value, dialect):
        if value is None:
            return value
        else:
            if not isinstance(value, uuid.UUID):
                return uuid.UUID(value)
            else:
                return value

UUID_TYPE = GUID()
JSON_TYPE = JSONB().with_variant(JSON(), "sqlite")


class User(Base):
    __tablename__ = "users"

    id: Mapped[uuid.UUID] = mapped_column(UUID_TYPE, primary_key=True, default=uuid.uuid4)
    phone: Mapped[Optional[str]] = mapped_column(String, unique=True, nullable=True)
    email: Mapped[Optional[str]] = mapped_column(String, unique=True, nullable=True)
    hashed_password: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    auth_provider: Mapped[str] = mapped_column(String, default="password", nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utcnow, nullable=False)
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utcnow, onupdate=utcnow, nullable=False)

    settings: Mapped[Optional["UserSettings"]] = relationship("UserSettings", back_populates="user", uselist=False, cascade="all, delete-orphan")
    devices: Mapped[List["LinkedDevice"]] = relationship("LinkedDevice", back_populates="user", cascade="all, delete-orphan")
    profiles: Mapped[List["Profile"]] = relationship("Profile", back_populates="user", cascade="all, delete-orphan")


class UserSettings(Base):
    __tablename__ = "user_settings"

    user_id: Mapped[uuid.UUID] = mapped_column(UUID_TYPE, ForeignKey("users.id", ondelete="CASCADE"), primary_key=True)
    theme: Mapped[str] = mapped_column(String, default="claro", nullable=False)
    notifications_enabled: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utcnow, onupdate=utcnow, nullable=False)

    user: Mapped["User"] = relationship("User", back_populates="settings")


class LinkedDevice(Base):
    __tablename__ = "linked_devices"

    id: Mapped[uuid.UUID] = mapped_column(UUID_TYPE, primary_key=True, default=uuid.uuid4)
    user_id: Mapped[uuid.UUID] = mapped_column(UUID_TYPE, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    device_name: Mapped[str] = mapped_column(String, nullable=False)
    device_type: Mapped[str] = mapped_column(String, nullable=False)
    last_active_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utcnow, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utcnow, nullable=False)
    revoked_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), nullable=True)

    user: Mapped["User"] = relationship("User", back_populates="devices")


class Profile(Base):
    __tablename__ = "profiles"

    id: Mapped[uuid.UUID] = mapped_column(UUID_TYPE, primary_key=True, default=uuid.uuid4)
    user_id: Mapped[uuid.UUID] = mapped_column(UUID_TYPE, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    type: Mapped[str] = mapped_column(String, nullable=False)  # 'pessoal', 'comercial'
    display_name: Mapped[str] = mapped_column(String, nullable=False)
    avatar_id: Mapped[Optional[uuid.UUID]] = mapped_column(UUID_TYPE, ForeignKey("attachments.id", ondelete="SET NULL", use_alter=True), nullable=True)
    bio: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utcnow, nullable=False)
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utcnow, onupdate=utcnow, nullable=False)

    user: Mapped["User"] = relationship("User", back_populates="profiles")
    avatar: Mapped[Optional["Attachment"]] = relationship("Attachment", foreign_keys=[avatar_id])


class Attachment(Base):
    __tablename__ = "attachments"

    id: Mapped[uuid.UUID] = mapped_column(UUID_TYPE, primary_key=True, default=uuid.uuid4)
    uploaded_by_profile_id: Mapped[uuid.UUID] = mapped_column(UUID_TYPE, ForeignKey("profiles.id", ondelete="CASCADE"), nullable=False)
    storage_url: Mapped[str] = mapped_column(String, nullable=False)
    mime_type: Mapped[str] = mapped_column(String, nullable=False)
    size_bytes: Mapped[Optional[int]] = mapped_column(BigInteger, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utcnow, nullable=False)


class Conversation(Base):
    __tablename__ = "conversations"

    id: Mapped[uuid.UUID] = mapped_column(UUID_TYPE, primary_key=True, default=uuid.uuid4)
    kind: Mapped[str] = mapped_column(String, nullable=False)  # 'direta', 'grupo'
    context: Mapped[str] = mapped_column(String, default="pessoal", nullable=False)  # 'pessoal', 'negocio'
    tag: Mapped[Optional[str]] = mapped_column(String, nullable=True)  # 'cliente', 'fornecedor', 'familia', 'amigos', 'orcamento', 'evento'
    title: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    avatar_id: Mapped[Optional[uuid.UUID]] = mapped_column(UUID_TYPE, ForeignKey("attachments.id", ondelete="SET NULL"), nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utcnow, nullable=False)

    participants: Mapped[List["ConversationParticipant"]] = relationship("ConversationParticipant", back_populates="conversation", cascade="all, delete-orphan")
    messages: Mapped[List["Message"]] = relationship("Message", back_populates="conversation", cascade="all, delete-orphan")


class ConversationParticipant(Base):
    __tablename__ = "conversation_participants"

    conversation_id: Mapped[uuid.UUID] = mapped_column(UUID_TYPE, ForeignKey("conversations.id", ondelete="CASCADE"), primary_key=True)
    profile_id: Mapped[uuid.UUID] = mapped_column(UUID_TYPE, ForeignKey("profiles.id", ondelete="CASCADE"), primary_key=True)
    role: Mapped[str] = mapped_column(String, default="membro", nullable=False)  # 'membro', 'admin'
    joined_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utcnow, nullable=False)
    muted: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)

    conversation: Mapped["Conversation"] = relationship("Conversation", back_populates="participants")
    profile: Mapped["Profile"] = relationship("Profile")


class Message(Base):
    __tablename__ = "messages"

    id: Mapped[uuid.UUID] = mapped_column(UUID_TYPE, primary_key=True, default=uuid.uuid4)
    conversation_id: Mapped[uuid.UUID] = mapped_column(UUID_TYPE, ForeignKey("conversations.id", ondelete="CASCADE"), nullable=False)
    sender_profile_id: Mapped[uuid.UUID] = mapped_column(UUID_TYPE, ForeignKey("profiles.id", ondelete="CASCADE"), nullable=False)
    content_type: Mapped[str] = mapped_column(String, nullable=False)  # 'texto', 'imagem', 'audio', 'documento'
    content_text: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    attachment_id: Mapped[Optional[uuid.UUID]] = mapped_column(UUID_TYPE, ForeignKey("attachments.id", ondelete="SET NULL"), nullable=True)
    reply_to_message_id: Mapped[Optional[uuid.UUID]] = mapped_column(UUID_TYPE, ForeignKey("messages.id", ondelete="SET NULL"), nullable=True)
    msg_metadata: Mapped[dict] = mapped_column("metadata", JSON_TYPE, default=dict, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utcnow, nullable=False)

    conversation: Mapped["Conversation"] = relationship("Conversation", back_populates="messages")
    sender: Mapped["Profile"] = relationship("Profile")
    attachment: Mapped[Optional["Attachment"]] = relationship("Attachment")
    statuses: Mapped[List["MessageStatus"]] = relationship("MessageStatus", back_populates="message", cascade="all, delete-orphan")


class MessageStatus(Base):
    __tablename__ = "message_status"

    message_id: Mapped[uuid.UUID] = mapped_column(UUID_TYPE, ForeignKey("messages.id", ondelete="CASCADE"), primary_key=True)
    profile_id: Mapped[uuid.UUID] = mapped_column(UUID_TYPE, ForeignKey("profiles.id", ondelete="CASCADE"), primary_key=True)
    status: Mapped[str] = mapped_column(String, nullable=False)  # 'enviado', 'entregue', 'lido'
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utcnow, onupdate=utcnow, nullable=False)

    message: Mapped["Message"] = relationship("Message", back_populates="statuses")


class SavedMessage(Base):
    __tablename__ = "saved_messages"

    profile_id: Mapped[uuid.UUID] = mapped_column(UUID_TYPE, ForeignKey("profiles.id", ondelete="CASCADE"), primary_key=True)
    message_id: Mapped[uuid.UUID] = mapped_column(UUID_TYPE, ForeignKey("messages.id", ondelete="CASCADE"), primary_key=True)
    saved_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utcnow, nullable=False)


class PersonalNote(Base):
    __tablename__ = "personal_notes"

    id: Mapped[uuid.UUID] = mapped_column(UUID_TYPE, primary_key=True, default=uuid.uuid4)
    profile_id: Mapped[uuid.UUID] = mapped_column(UUID_TYPE, ForeignKey("profiles.id", ondelete="CASCADE"), nullable=False)
    content: Mapped[str] = mapped_column(Text, nullable=False)
    pinned: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utcnow, nullable=False)
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utcnow, onupdate=utcnow, nullable=False)


class Contact(Base):
    __tablename__ = "contacts"

    owner_profile_id: Mapped[uuid.UUID] = mapped_column(UUID_TYPE, ForeignKey("profiles.id", ondelete="CASCADE"), primary_key=True)
    contact_profile_id: Mapped[uuid.UUID] = mapped_column(UUID_TYPE, ForeignKey("profiles.id", ondelete="CASCADE"), primary_key=True)
    relation_label: Mapped[str] = mapped_column(String, nullable=False)  # 'familia', 'amigo'
    status: Mapped[str] = mapped_column(String, default="pendente", nullable=False)  # 'pendente', 'aceito'
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utcnow, nullable=False)


def default_expires_at():
    return datetime.now(timezone.utc) + timedelta(hours=24)

class Status(Base):
    __tablename__ = "statuses"

    id: Mapped[uuid.UUID] = mapped_column(UUID_TYPE, primary_key=True, default=uuid.uuid4)
    profile_id: Mapped[uuid.UUID] = mapped_column(UUID_TYPE, ForeignKey("profiles.id", ondelete="CASCADE"), nullable=False)
    attachment_id: Mapped[uuid.UUID] = mapped_column(UUID_TYPE, ForeignKey("attachments.id", ondelete="CASCADE"), nullable=False)
    caption: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    visibility: Mapped[str] = mapped_column(String, nullable=False)  # 'publico', 'privado'
    catalog_item_id: Mapped[Optional[uuid.UUID]] = mapped_column(UUID_TYPE, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utcnow, nullable=False)
    expires_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=default_expires_at, nullable=False)

    profile: Mapped["Profile"] = relationship("Profile")
    attachment: Mapped["Attachment"] = relationship("Attachment")
    views: Mapped[List["StatusView"]] = relationship("StatusView", back_populates="status", cascade="all, delete-orphan")


class StatusView(Base):
    __tablename__ = "status_views"

    status_id: Mapped[uuid.UUID] = mapped_column(UUID_TYPE, ForeignKey("statuses.id", ondelete="CASCADE"), primary_key=True)
    viewer_profile_id: Mapped[uuid.UUID] = mapped_column(UUID_TYPE, ForeignKey("profiles.id", ondelete="CASCADE"), primary_key=True)
    viewed_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utcnow, nullable=False)

    status: Mapped["Status"] = relationship("Status", back_populates="views")
