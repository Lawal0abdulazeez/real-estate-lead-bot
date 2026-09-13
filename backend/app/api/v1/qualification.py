"""Qualification and scoring helper endpoints for n8n workflows."""

from typing import Any, Dict, List, Optional
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import get_db
from app.models.lead import Lead
from app.models.lead_score import LeadScore
from app.services.qualification import score_lead

router = APIRouter()


class CalculateScoreRequest(BaseModel):
    lead_id: Optional[Any] = None
    body: Optional[Dict[str, Any]] = None


class CalculateScoreResponse(BaseModel):
    lead_id: UUID
    score: int
    classification: str
    reasons: List[str]
    qualified: bool


class SaveScoreHistoryRequest(BaseModel):
    lead_id: Optional[Any] = None
    score: Optional[int] = None
    classification: Optional[str] = None
    reason: Optional[str] = None
    body: Optional[Dict[str, Any]] = None


@router.post("/calculate", response_model=CalculateScoreResponse)
async def calculate_score(
    payload: CalculateScoreRequest, db: AsyncSession = Depends(get_db)
):
    """Calculates lead score and classification for n8n qualification workflow."""
    raw_lead_id = payload.lead_id
    if payload.body and isinstance(payload.body, dict):
        raw_lead_id = payload.body.get("lead_id") or raw_lead_id

    lead = None
    if raw_lead_id:
        try:
            uid = UUID(str(raw_lead_id))
            res = await db.execute(select(Lead).where(Lead.id == uid))
            lead = res.scalar_one_or_none()
        except (ValueError, TypeError):
            pass

    if not lead:
        # Fallback to latest lead
        res = await db.execute(select(Lead).order_by(Lead.updated_at.desc()).limit(1))
        lead = res.scalar_one_or_none()

    if not lead:
        raise HTTPException(status_code=404, detail="No lead found for qualification")

    result = score_lead(lead)
    return CalculateScoreResponse(
        lead_id=lead.id,
        score=result.score,
        classification=result.classification,
        reasons=result.reasons,
        qualified=result.score >= 30,
    )


@router.post("/score-history")
async def save_score_history(
    payload: SaveScoreHistoryRequest, db: AsyncSession = Depends(get_db)
):
    """Saves a lead qualification score entry in history."""
    raw_lead_id = payload.lead_id
    score = payload.score
    classification = payload.classification
    reason = payload.reason

    if payload.body and isinstance(payload.body, dict):
        b = payload.body
        raw_lead_id = b.get("lead_id") or raw_lead_id
        score = b.get("score") if b.get("score") is not None else score
        classification = b.get("classification") or classification
        reason = b.get("reason") or reason

    lead = None
    if raw_lead_id:
        try:
            uid = UUID(str(raw_lead_id))
            res = await db.execute(select(Lead).where(Lead.id == uid))
            lead = res.scalar_one_or_none()
        except (ValueError, TypeError):
            pass

    if not lead:
        res = await db.execute(select(Lead).order_by(Lead.updated_at.desc()).limit(1))
        lead = res.scalar_one_or_none()

    if not lead:
        raise HTTPException(status_code=404, detail="No lead found to attach score")

    score_row = LeadScore(
        lead_id=lead.id,
        score=int(score if score is not None else 50),
        classification=str(classification or "WARM"),
        reason=reason,
        scoring_version="v1",
    )
    db.add(score_row)
    await db.flush()
    await db.refresh(score_row)

    return {
        "ok": True,
        "id": str(score_row.id),
        "lead_id": str(lead.id),
        "score": score_row.score,
        "classification": score_row.classification,
    }


@router.post("/notifications/sales")
async def receive_sales_notification(payload: Dict[str, Any]):
    """Receives and acknowledges sales notifications / fallbacks."""
    return {"status": "received", "data": payload}
