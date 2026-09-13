"""Follow-up endpoints for scheduling and reminders."""

from datetime import datetime, timezone
from typing import Optional
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import get_db
from app.models.activity import Activity
from app.models.followup import FollowUp
from app.models.lead import Lead
from app.schemas.followup import FollowUpCreate, FollowUpRead, FollowUpUpdate

router = APIRouter()


@router.get("/due", response_model=list[FollowUpRead])
async def get_due_followups(db: AsyncSession = Depends(get_db)):
    """Returns follow-ups that are due for reminders."""
    now = datetime.now(timezone.utc)
    query = (
        select(FollowUp)
        .where(
            FollowUp.status.in_(["PENDING", "DUE"]),
            FollowUp.scheduled_at <= now,
        )
        .order_by(FollowUp.scheduled_at.asc())
    )
    result = await db.execute(query)
    return list(result.scalars().all())


@router.get("", response_model=list[FollowUpRead])
async def list_followups(
    status: Optional[str] = None,
    lead_id: Optional[UUID] = None,
    limit: int = Query(50, ge=1, le=100),
    db: AsyncSession = Depends(get_db),
):
    """List follow-ups with optional filtering."""
    query = select(FollowUp)
    if status:
        query = query.where(FollowUp.status == status)
    if lead_id:
        query = query.where(FollowUp.lead_id == lead_id)
    query = query.order_by(FollowUp.scheduled_at.asc()).limit(limit)
    result = await db.execute(query)
    return list(result.scalars().all())


@router.post("", response_model=FollowUpRead, status_code=201)
async def create_followup(
    payload: FollowUpCreate, db: AsyncSession = Depends(get_db)
):
    """Create a new follow-up."""
    if not payload.lead_id:
        # Fallback to latest lead if not provided
        latest = await db.execute(select(Lead).order_by(Lead.updated_at.desc()).limit(1))
        lead = latest.scalar_one_or_none()
        if not lead:
            raise HTTPException(status_code=400, detail="lead_id is required")
        target_lead_id = lead.id
    else:
        target_lead_id = payload.lead_id

    followup = FollowUp(
        lead_id=target_lead_id,
        type=payload.type or "CALL",
        status="PENDING",
        scheduled_at=payload.scheduled_at or datetime.now(timezone.utc),
        notes=payload.notes,
        channel=payload.channel or "INTERNAL",
        assigned_agent_id=payload.assigned_agent_id,
    )
    db.add(followup)
    await db.flush()
    await db.refresh(followup)
    return followup


@router.get("/{follow_up_id}", response_model=FollowUpRead)
async def get_followup(follow_up_id: UUID, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(FollowUp).where(FollowUp.id == follow_up_id))
    followup = result.scalar_one_or_none()
    if not followup:
        raise HTTPException(status_code=404, detail="Follow-up not found")
    return followup


@router.patch("/{follow_up_id}", response_model=FollowUpRead)
async def update_followup(
    follow_up_id: UUID,
    payload: FollowUpUpdate,
    db: AsyncSession = Depends(get_db),
):
    result = await db.execute(select(FollowUp).where(FollowUp.id == follow_up_id))
    followup = result.scalar_one_or_none()
    if not followup:
        raise HTTPException(status_code=404, detail="Follow-up not found")

    data = payload.model_dump(exclude_unset=True)
    for key, val in data.items():
        if val is not None:
            setattr(followup, key, val)

    await db.flush()
    await db.refresh(followup)
    return followup


@router.post("/{follow_up_id}/complete", response_model=FollowUpRead)
async def complete_followup(
    follow_up_id: UUID,
    db: AsyncSession = Depends(get_db),
):
    result = await db.execute(select(FollowUp).where(FollowUp.id == follow_up_id))
    followup = result.scalar_one_or_none()
    if not followup:
        raise HTTPException(status_code=404, detail="Follow-up not found")

    followup.status = "COMPLETED"
    activity = Activity(
        lead_id=followup.lead_id,
        actor_type="SYSTEM",
        activity_type="FOLLOW_UP_COMPLETED",
        description=f"Follow-up {followup.type} completed.",
    )
    db.add(activity)
    await db.flush()
    await db.refresh(followup)
    return followup
