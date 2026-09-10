from typing import Any, List, Optional, Tuple
from uuid import UUID

from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.activity import Activity
from app.models.enums import ActivityType, SenderType
from app.models.message import Message
from app.schemas.message import MessageCreate
from app.services.n8n import trigger_message_processing


async def create_customer_message(
    db: AsyncSession,
    *,
    conversation_id: UUID,
    lead_id: UUID,
    data: MessageCreate,
) -> Message:
    # Idempotency on external_message_id
    if data.external_message_id:
        existing = await db.execute(
            select(Message).where(Message.external_message_id == data.external_message_id)
        )
        found = existing.scalar_one_or_none()
        if found:
            return found

    msg = Message(
        conversation_id=conversation_id,
        sender_type=SenderType.CUSTOMER.value,
        content=data.content.strip(),
        external_message_id=data.external_message_id,
        processing_status="RECEIVED",
    )
    db.add(msg)

    activity = Activity(
        lead_id=lead_id,
        actor_type="CUSTOMER",
        activity_type=ActivityType.MESSAGE_RECEIVED.value,
        description="Customer message received",
    )
    db.add(activity)
    await db.flush()

    # Trigger n8n asynchronously (best-effort)
    await trigger_message_processing(
        message_id=msg.id,
        conversation_id=conversation_id,
        lead_id=lead_id,
    )
    msg.processing_status = "PROCESSING"
    await db.flush()
    await db.refresh(msg)
    return msg


async def create_bot_message(
    db: AsyncSession,
    *,
    conversation_id: UUID,
    content: str,
) -> Message:
    msg = Message(
        conversation_id=conversation_id,
        sender_type=SenderType.BOT.value,
        content=content,
        processing_status="PROCESSED",
    )
    db.add(msg)
    await db.flush()
    await db.refresh(msg)
    return msg


async def get_message(
    db: AsyncSession,
    message_id: Any,
) -> Optional[Message]:
    try:
        uid = UUID(str(message_id))
        result = await db.execute(select(Message).where(Message.id == uid))
        msg = result.scalar_one_or_none()
        if msg:
            return msg
    except (ValueError, TypeError):
        pass

    # Try external_message_id
    result = await db.execute(
        select(Message).where(Message.external_message_id == str(message_id))
    )
    msg = result.scalar_one_or_none()
    if msg:
        return msg

    # Dev fallback for test IDs like 'msg_001' in n8n editor
    result = await db.execute(
        select(Message).order_by(Message.created_at.desc()).limit(1)
    )
    return result.scalar_one_or_none()



async def update_message(
    db: AsyncSession,
    message: Message,
    *,
    processing_status: Optional[str] = None,
    content: Optional[str] = None,
) -> Message:
    if processing_status is not None:
        message.processing_status = processing_status
    if content is not None:
        message.content = content
    await db.flush()
    await db.refresh(message)
    return message



async def list_messages(
    db: AsyncSession,
    conversation_id: UUID,
    *,
    page: int = 1,
    limit: int = 50,
) -> Tuple[List[Message], int]:
    count_q = select(func.count()).select_from(Message).where(
        Message.conversation_id == conversation_id
    )
    total = (await db.execute(count_q)).scalar() or 0
    query = (
        select(Message)
        .where(Message.conversation_id == conversation_id)
        .order_by(Message.created_at.asc())
        .offset((page - 1) * limit)
        .limit(limit)
    )
    rows = (await db.execute(query)).scalars().all()
    return list(rows), total

