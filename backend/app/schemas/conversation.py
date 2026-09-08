from datetime import datetime
from typing import Optional
from uuid import UUID

from pydantic import BaseModel, ConfigDict


class ConversationCreate(BaseModel):
    lead_id: Optional[UUID] = None  # if omitted, a new lead is created
    channel: str = "WEB"
    # Optional seed customer info when creating a brand-new lead
    name: Optional[str] = None
    email: Optional[str] = None
    phone: Optional[str] = None


class ConversationRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    lead_id: UUID
    channel: str
    status: str
    started_at: datetime
    created_at: datetime
