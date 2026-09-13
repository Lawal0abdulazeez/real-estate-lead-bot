"""General Activity logging endpoint for n8n workflows and integrations."""

from typing import Any, Dict, Optional
from uuid import UUID

from fastapi import APIRouter, Depends, Request
from pydantic import BaseModel, Field
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import get_db
from app.models.activity import Activity
from app.models.lead import Lead
from app.schemas.activity import ActivityRead

router = APIRouter()


class GenericActivityPayload(BaseModel):
    lead_id: Optional[Any] = None
    actor_type: str = "SYSTEM"
    actor_id: Optional[UUID] = None
    activity_type: str = "WORKFLOW_ACTIVITY"
    description: Optional[str] = None
    metadata: Optional[Dict[str, Any]] = None
    body: Optional[Dict[str, Any]] = None


@router.post("", response_model=ActivityRead, status_code=201)
async def log_activity(
    request: Request,
    payload: GenericActivityPayload,
    db: AsyncSession = Depends(get_db),
):
    """Logs an activity from n8n workflows or external webhooks.
    Gracefully unpacks unwrapped or body-wrapped payloads.
    """
    data = payload.model_dump()
    if data.get("body") and isinstance(data["body"], dict):
        inner = data["body"]
        for k in ["lead_id", "actor_type", "actor_id", "activity_type", "description", "metadata"]:
            if inner.get(k) is not None:
                data[k] = inner[k]

    # Resolve target lead_id
    raw_lead_id = data.get("lead_id")
    target_uuid = None
    if raw_lead_id:
        try:
            target_uuid = UUID(str(raw_lead_id))
        except (ValueError, TypeError):
            pass

    if not target_uuid:
        # Fallback to most recently updated lead
        result = await db.execute(select(Lead).order_by(Lead.updated_at.desc()).limit(1))
        lead = result.scalar_one_or_none()
        if lead:
            target_uuid = lead.id

    if not target_uuid:
        # Fallback: create an initial lead if database is completely empty
        new_lead = Lead(name="PrimeHomes Customer", status="NEW")
        db.add(new_lead)
        await db.flush()
        target_uuid = new_lead.id

    activity = Activity(
        lead_id=target_uuid,
        actor_type=str(data.get("actor_type") or "SYSTEM"),
        actor_id=data.get("actor_id"),
        activity_type=str(data.get("activity_type") or "WORKFLOW_EVENT"),
        description=data.get("description"),
        metadata_=data.get("metadata"),
    )
    db.add(activity)
    await db.flush()
    await db.refresh(activity)
    return activity
