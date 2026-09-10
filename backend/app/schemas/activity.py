from datetime import datetime
from typing import Any, Dict, Optional
from uuid import UUID

from pydantic import AliasChoices, BaseModel, ConfigDict, Field


class ActivityCreate(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    actor_type: str = Field("SYSTEM", description="CUSTOMER, BOT, SALES, or SYSTEM")
    actor_id: Optional[UUID] = None
    activity_type: str
    description: Optional[str] = None
    metadata: Optional[Dict[str, Any]] = Field(
        None, validation_alias=AliasChoices("metadata", "metadata_")
    )


class ActivityRead(BaseModel):
    model_config = ConfigDict(from_attributes=True, populate_by_name=True)

    id: UUID
    lead_id: UUID
    actor_type: str
    actor_id: Optional[UUID] = None
    activity_type: str
    description: Optional[str] = None
    metadata: Optional[Dict[str, Any]] = Field(
        None, validation_alias=AliasChoices("metadata_", "metadata")
    )
    created_at: datetime

