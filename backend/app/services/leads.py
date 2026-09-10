from typing import Optional, Tuple
from uuid import UUID

from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.activity import Activity
from app.models.enums import ActivityType, LeadStatus
from app.models.lead import Lead
from app.models.lead_score import LeadScore
from app.schemas.lead import LeadCreate, LeadUpdate
from app.services.qualification import score_lead


async def create_lead(db: AsyncSession, data: LeadCreate) -> Lead:
    lead = Lead(
        name=data.name,
        email=str(data.email) if data.email else None,
        phone=data.phone,
        property_type=data.property_type,
        transaction_type=data.transaction_type,
        bedrooms=data.bedrooms,
        bathrooms=data.bathrooms,
        location=data.location,
        budget_min=data.budget_min,
        budget_max=data.budget_max,
        currency=data.currency or "NGN",
        timeline=data.timeline,
        intent=data.intent,
        source=data.source or "WEBSITE",
        status=LeadStatus.NEW.value,
    )
    db.add(lead)
    await db.flush()

    activity = Activity(
        lead_id=lead.id,
        actor_type="SYSTEM",
        activity_type=ActivityType.LEAD_CREATED.value,
        description="Lead created",
    )
    db.add(activity)
    await db.flush()
    await db.refresh(lead)
    return lead


async def get_lead(db: AsyncSession, lead_id: UUID) -> Optional[Lead]:
    result = await db.execute(select(Lead).where(Lead.id == lead_id))
    return result.scalar_one_or_none()


async def list_leads(
    db: AsyncSession,
    *,
    page: int = 1,
    limit: int = 20,
    status: Optional[str] = None,
    classification: Optional[str] = None,
) -> Tuple[list[Lead], int]:
    query = select(Lead)
    count_q = select(func.count()).select_from(Lead)

    if status:
        query = query.where(Lead.status == status)
        count_q = count_q.where(Lead.status == status)
    if classification:
        query = query.where(Lead.classification == classification)
        count_q = count_q.where(Lead.classification == classification)

    total = (await db.execute(count_q)).scalar() or 0
    query = query.order_by(Lead.created_at.desc()).offset((page - 1) * limit).limit(limit)
    rows = (await db.execute(query)).scalars().all()
    return list(rows), total


async def update_lead(db: AsyncSession, lead: Lead, data: LeadUpdate) -> Lead:
    payload = data.model_dump(exclude_unset=True)
    for key, value in payload.items():
        if key == "email" and value is not None:
            value = str(value)
        setattr(lead, key, value)
    await db.flush()
    await db.refresh(lead)
    return lead


async def qualify_lead(db: AsyncSession, lead: Lead) -> LeadScore:
    result = score_lead(lead)
    lead.score = result.score
    lead.classification = result.classification
    if lead.status == LeadStatus.NEW.value:
        lead.status = LeadStatus.QUALIFYING.value
    if result.score >= 30:
        lead.status = LeadStatus.QUALIFIED.value

    score_row = LeadScore(
        lead_id=lead.id,
        score=result.score,
        classification=result.classification,
        reason="; ".join(result.reasons) if result.reasons else None,
        scoring_version="v1",
    )
    db.add(score_row)

    activity = Activity(
        lead_id=lead.id,
        actor_type="SYSTEM",
        activity_type=ActivityType.LEAD_QUALIFIED.value,
        description=f"Score {result.score} → {result.classification}",
        metadata_={"reasons": result.reasons},
    )
    db.add(activity)
    await db.flush()
    await db.refresh(score_row)
    await db.refresh(lead)
    return score_row


async def create_activity(
    db: AsyncSession,
    lead_id: UUID,
    *,
    actor_type: str = "SYSTEM",
    actor_id: Optional[UUID] = None,
    activity_type: str,
    description: Optional[str] = None,
    metadata: Optional[dict] = None,
) -> Activity:
    act = Activity(
        lead_id=lead_id,
        actor_type=actor_type,
        actor_id=actor_id,
        activity_type=activity_type,
        description=description,
        metadata_=metadata,
    )
    db.add(act)
    await db.flush()
    await db.refresh(act)
    return act



async def list_activities(
    db: AsyncSession,
    lead_id: UUID,
    *,
    limit: int = 50,
) -> list[Activity]:
    query = (
        select(Activity)
        .where(Activity.lead_id == lead_id)
        .order_by(Activity.created_at.desc())
        .limit(limit)
    )
    result = await db.execute(query)
    return list(result.scalars().all())

