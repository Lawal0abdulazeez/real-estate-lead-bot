from datetime import datetime
from typing import Optional
from uuid import UUID

from pydantic import BaseModel, ConfigDict


class FollowUpCreate(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    lead_id: Optional[UUID] = None
    type: str = "CALL"
    scheduled_at: Optional[datetime] = None
    notes: Optional[str] = None
    channel: Optional[str] = "INTERNAL"
    assigned_agent_id: Optional[UUID] = None


class FollowUpUpdate(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    status: Optional[str] = None
    notes: Optional[str] = None
    channel: Optional[str] = None
    assigned_agent_id: Optional[UUID] = None
    last_reminded_at: Optional[datetime] = None


class FollowUpRead(BaseModel):
    model_config = ConfigDict(from_attributes=True, populate_by_name=True)

    id: UUID
    lead_id: UUID
    type: str
    status: str
    scheduled_at: datetime
    notes: Optional[str] = None
    channel: Optional[str] = "INTERNAL"
    assigned_agent_id: Optional[UUID] = None
    last_reminded_at: Optional[datetime] = None
    created_at: datetime
    updated_at: datetime
