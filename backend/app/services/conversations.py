from typing import Optional
from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.models.conversation import Conversation
from app.models.enums import ConversationStatus, LeadStatus
from app.models.lead import Lead
from app.schemas.conversation import ConversationCreate
from app.schemas.lead import LeadCreate
from app.services.leads import create_lead


async def create_conversation(
    db: AsyncSession, data: ConversationCreate
) -> Conversation:
    lead_id = data.lead_id
    if lead_id is None:
        lead = await create_lead(
            db,
            LeadCreate(
                name=data.name,
                email=data.email,
                phone=data.phone,
                source="WEBSITE",
            ),
        )
        lead_id = lead.id

    conv = Conversation(
        lead_id=lead_id,
        channel=data.channel or "WEB",
        status=ConversationStatus.ACTIVE.value,
    )
    db.add(conv)
    await db.flush()
    await db.refresh(conv)
    return conv



async def get_conversation(
    db: AsyncSession, conversation_id: UUID, *,
    with_messages: bool = False,
) -> Optional[Conversation]:
    query = select(Conversation).where(Conversation.id == conversation_id)
    if with_messages:
        query = query.options(selectinload(Conversation.messages))
    result = await db.execute(query)
    return result.scalar_one_or_none()
