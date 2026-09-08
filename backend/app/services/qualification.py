"""Deterministic lead qualification (LEAD_QUALIFICATION_SPEC.md)."""

from dataclasses import dataclass
from typing import List, Optional

from app.models.enums import Classification, Timeline, TransactionType
from app.models.lead import Lead


@dataclass
class QualificationResult:
    score: int
    classification: str
    reasons: List[str]


def classify(score: int) -> str:
    if score >= 80:
        return Classification.HOT.value
    if score >= 60:
        return Classification.WARM.value
    if score >= 30:
        return Classification.COLD.value
    return Classification.UNQUALIFIED.value


def score_lead(lead: Lead) -> QualificationResult:
    """Apply the documented point system (max 100)."""
    score = 0
    reasons: List[str] = []

    # Intent / transaction — max 20
    intent = (lead.intent or lead.transaction_type or "").upper()
    if intent in {TransactionType.BUY.value, TransactionType.RENT.value,
                 TransactionType.SELL.value, "LAND"}:
        score += 20
        reasons.append("Clear BUY/RENT/SELL/LAND intent (+20)")
    elif intent in {"PROPERTY_ENQUIRY", "GENERAL_ENQUIRY"}:
        score += 10
        reasons.append("General property enquiry (+10)")

    # Property requirement — max 15
    if lead.property_type and lead.property_type.upper() not in ("UNKNOWN", "OTHER", ""):
        score += 10
        reasons.append(f"Specific property type: {lead.property_type} (+10)")
        if lead.bedrooms is not None and lead.bedrooms > 0:
            score += 5
            reasons.append(f"Bedrooms specified: {lead.bedrooms} (+5)")

    # Location — max 15
    if lead.location and lead.location.strip():
        # Treat any concrete location as specific for MVP
        score += 15
        reasons.append(f"Location provided: {lead.location} (+15)")

    # Budget — max 20
    if lead.budget_max is not None or lead.budget_min is not None:
        score += 20
        reasons.append("Budget provided (+20)")

    # Timeline — max 20
    timeline = (lead.timeline or "").upper()
    timeline_points = {
        Timeline.IMMEDIATE.value: 20,
        Timeline.WITHIN_1_MONTH.value: 18,
        Timeline.WITHIN_3_MONTHS.value: 15,
        Timeline.WITHIN_6_MONTHS.value: 10,
        Timeline.RESEARCHING.value: 5,
    }
    pts = timeline_points.get(timeline, 0)
    if pts:
        score += pts
        reasons.append(f"Timeline {timeline} (+{pts})")

    # Contact — max 10
    contact = 0
    if lead.phone:
        contact += 5
        reasons.append("Phone available (+5)")
    if lead.email:
        contact += 3
        reasons.append("Email available (+3)")
    if lead.name:
        contact += 2
        reasons.append("Name available (+2)")
    score += contact

    score = min(score, 100)
    classification = classify(score)
    return QualificationResult(score=score, classification=classification, reasons=reasons)
