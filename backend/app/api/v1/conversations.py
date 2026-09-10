from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import get_db
from app.schemas.conversation import ConversationCreate, ConversationRead
from app.schemas.message import MessageCreate, MessageListResponse, MessageRead
from app.services import conversations as conv_service
from app.services import messages as msg_service

router = APIRouter()


@router.post("", response_model=ConversationRead, status_code=201)
async def create_conversation(
    payload: ConversationCreate, db: AsyncSession = Depends(get_db)
):
    conv = await conv_service.create_conversation(db, payload)
    return conv


@router.get("/{conversation_id}", response_model=ConversationRead)
async def get_conversation(
    conversation_id: UUID, db: AsyncSession = Depends(get_db)
):
    conv = await conv_service.get_conversation(db, conversation_id)
    if not conv:
        raise HTTPException(status_code=404, detail="Conversation not found")
    return conv


@router.get("/{conversation_id}/messages", response_model=MessageListResponse)
async def get_messages(
    conversation_id: UUID,
    page: int = 1,
    limit: int = 50,
    db: AsyncSession = Depends(get_db),
):
    conv = await conv_service.get_conversation(db, conversation_id)
    if not conv:
        raise HTTPException(status_code=404, detail="Conversation not found")
    items, total = await msg_service.list_messages(
        db, conversation_id, page=page, limit=limit
    )
    return MessageListResponse(items=items, page=page, limit=limit, total=total)


@router.post(
    "/{conversation_id}/messages",
    response_model=MessageRead,
    status_code=201,
)
async def post_message(
    conversation_id: UUID,
    payload: MessageCreate,
    db: AsyncSession = Depends(get_db),
):
    conv = await conv_service.get_conversation(db, conversation_id)
    if not conv:
        raise HTTPException(status_code=404, detail="Conversation not found")

    sender = (payload.sender_type or "CUSTOMER").upper()
    if sender == "BOT":
        msg = await msg_service.create_bot_message(
            db,
            conversation_id=conversation_id,
            content=payload.content,
        )
    else:
        msg = await msg_service.create_customer_message(
            db,
            conversation_id=conversation_id,
            lead_id=conv.lead_id,
            data=payload,
        )
    return msg

