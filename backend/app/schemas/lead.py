from datetime import datetime
from decimal import Decimal
from typing import List, Optional
from uuid import UUID

from pydantic import AliasChoices, BaseModel, ConfigDict, EmailStr, Field


class LeadBase(BaseModel):
    name: Optional[str] = None
    email: Optional[EmailStr] = None
    phone: Optional[str] = None
    property_type: Optional[str] = None
    transaction_type: Optional[str] = None
    bedrooms: Optional[int] = Field(None, ge=0)
    bathrooms: Optional[int] = Field(None, ge=0)
    location: Optional[str] = None
    budget_min: Optional[Decimal] = None
    budget_max: Optional[Decimal] = None
    currency: Optional[str] = "NGN"
    timeline: Optional[str] = None
    intent: Optional[str] = None
    source: Optional[str] = "WEBSITE"


class LeadCreate(LeadBase):
    pass


class LeadUpdate(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    name: Optional[str] = Field(None, validation_alias=AliasChoices("name", "customer_name"))
    email: Optional[EmailStr] = None
    phone: Optional[str] = None
    property_type: Optional[str] = None
    transaction_type: Optional[str] = None
    bedrooms: Optional[int] = Field(None, ge=0)
    bathrooms: Optional[int] = Field(None, ge=0)
    location: Optional[str] = None
    budget_min: Optional[Decimal] = None
    budget_max: Optional[Decimal] = None
    currency: Optional[str] = None
    timeline: Optional[str] = None
    intent: Optional[str] = None
    status: Optional[str] = None


class LeadRead(LeadBase):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    status: str
    classification: Optional[str] = None
    score: Optional[int] = None
    created_at: datetime
    updated_at: datetime
    last_contacted_at: Optional[datetime] = None
    next_follow_up_at: Optional[datetime] = None


class LeadListResponse(BaseModel):
    items: List[LeadRead]
    page: int
    limit: int
    total: int
    total_pages: int


class QualifyResponse(BaseModel):
    lead_id: UUID
    score: int
    classification: str
    reasons: List[str]
    qualified: bool
