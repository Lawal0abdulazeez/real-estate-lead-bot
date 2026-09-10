from datetime import datetime
from typing import Any, Dict, Optional
from uuid import UUID

from pydantic import AliasChoices, BaseModel, ConfigDict, Field


class MessageCreate(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    content: str = Field(..., min_length=1, max_length=5000, validation_alias=AliasChoices("content", "response", "text"))
    sender_type: Optional[str] = Field("CUSTOMER", description="CUSTOMER or BOT")
    external_message_id: Optional[str] = None


class MessageUpdate(BaseModel):
    processing_status: Optional[str] = None
    content: Optional[str] = None


class MessageRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    conversation_id: UUID
    sender_type: str
    content: str
    processing_status: Optional[str] = None
    created_at: datetime


class MessageListResponse(BaseModel):
    items: list[MessageRead]
    page: int = 1
    limit: int = 50
    total: int = 0

