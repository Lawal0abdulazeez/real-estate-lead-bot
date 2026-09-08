from math import ceil
from typing import Optional
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import get_db
from app.schemas.lead import (
    LeadCreate,
    LeadListResponse,
    LeadRead,
    LeadUpdate,
    QualifyResponse,
)
from app.services import leads as lead_service
from app.services.qualification import score_lead

router = APIRouter()


@router.post("", response_model=LeadRead, status_code=201)
async def create_lead(payload: LeadCreate, db: AsyncSession = Depends(get_db)):
    lead = await lead_service.create_lead(db, payload)
    return lead


@router.get("", response_model=LeadListResponse)
async def list_leads(
    page: int = Query(1, ge=1),
    limit: int = Query(20, ge=1, le=100),
    status: Optional[str] = None,
    classification: Optional[str] = None,
    db: AsyncSession = Depends(get_db),
):
    items, total = await lead_service.list_leads(
        db, page=page, limit=limit, status=status, classification=classification
    )
    return LeadListResponse(
        items=items,
        page=page,
        limit=limit,
        total=total,
        total_pages=ceil(total / limit) if limit else 0,
    )


@router.get("/{lead_id}", response_model=LeadRead)
async def get_lead(lead_id: UUID, db: AsyncSession = Depends(get_db)):
    lead = await lead_service.get_lead(db, lead_id)
    if not lead:
        raise HTTPException(status_code=404, detail="Lead not found")
    return lead


@router.patch("/{lead_id}", response_model=LeadRead)
async def update_lead(
    lead_id: UUID, payload: LeadUpdate, db: AsyncSession = Depends(get_db)
):
    lead = await lead_service.get_lead(db, lead_id)
    if not lead:
        raise HTTPException(status_code=404, detail="Lead not found")
    lead = await lead_service.update_lead(db, lead, payload)
    return lead


@router.post("/{lead_id}/qualify", response_model=QualifyResponse)
async def qualify_lead(lead_id: UUID, db: AsyncSession = Depends(get_db)):
    lead = await lead_service.get_lead(db, lead_id)
    if not lead:
        raise HTTPException(status_code=404, detail="Lead not found")
    score_row = await lead_service.qualify_lead(db, lead)
    result = score_lead(lead)
    return QualifyResponse(
        lead_id=lead.id,
        score=score_row.score,
        classification=score_row.classification,
        reasons=result.reasons,
        qualified=score_row.score >= 30,
    )
