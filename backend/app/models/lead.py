import uuid
from datetime import datetime
from decimal import Decimal
from typing import TYPE_CHECKING, List, Optional

from sqlalchemy import DateTime, Integer, Numeric, String, Text, Uuid, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base
from app.models.enums import (
    Classification,
    Intent,
    LeadStatus,
    PropertyType,
    Timeline,
    TransactionType,
)

if TYPE_CHECKING:
    from app.models.conversation import Conversation
    from app.models.lead_score import LeadScore
    from app.models.activity import Activity


class Lead(Base):
    __tablename__ = "leads"

    id: Mapped[uuid.UUID] = mapped_column(
        Uuid(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    name: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    email: Mapped[Optional[str]] = mapped_column(String(255), nullable=True, index=True)
    phone: Mapped[Optional[str]] = mapped_column(String(50), nullable=True, index=True)

    property_type: Mapped[Optional[str]] = mapped_column(String(50), nullable=True)
    transaction_type: Mapped[Optional[str]] = mapped_column(String(50), nullable=True)
    bedrooms: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    bathrooms: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    location: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    budget_min: Mapped[Optional[Decimal]] = mapped_column(Numeric(18, 2), nullable=True)
    budget_max: Mapped[Optional[Decimal]] = mapped_column(Numeric(18, 2), nullable=True)
    currency: Mapped[Optional[str]] = mapped_column(String(10), nullable=True, default="NGN")
    timeline: Mapped[Optional[str]] = mapped_column(String(50), nullable=True)
    intent: Mapped[Optional[str]] = mapped_column(String(50), nullable=True)

    status: Mapped[str] = mapped_column(
        String(50), nullable=False, default=LeadStatus.NEW.value, index=True
    )
    classification: Mapped[Optional[str]] = mapped_column(String(50), nullable=True, index=True)
    score: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    source: Mapped[Optional[str]] = mapped_column(String(100), nullable=True, default="WEBSITE")

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False
    )
    last_contacted_at: Mapped[Optional[datetime]] = mapped_column(
        DateTime(timezone=True), nullable=True
    )
    next_follow_up_at: Mapped[Optional[datetime]] = mapped_column(
        DateTime(timezone=True), nullable=True
    )

    conversations: Mapped[List["Conversation"]] = relationship(
        "Conversation", back_populates="lead", cascade="all, delete-orphan"
    )
    scores: Mapped[List["LeadScore"]] = relationship(
        "LeadScore", back_populates="lead", cascade="all, delete-orphan"
    )
    activities: Mapped[List["Activity"]] = relationship(
        "Activity", back_populates="lead", cascade="all, delete-orphan"
    )
