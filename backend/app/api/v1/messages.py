from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import get_db
from app.schemas.message import MessageRead, MessageUpdate
from app.services import messages as msg_service

router = APIRouter()


@router.get("/{message_id}", response_model=MessageRead)
async def get_message(message_id: str, db: AsyncSession = Depends(get_db)):
    msg = await msg_service.get_message(db, message_id)
    if not msg:
        raise HTTPException(status_code=404, detail="Message not found")
    return msg


@router.patch("/{message_id}", response_model=MessageRead)
async def update_message(
    message_id: str, payload: MessageUpdate, db: AsyncSession = Depends(get_db)
):

    msg = await msg_service.get_message(db, message_id)
    if not msg:
        raise HTTPException(status_code=404, detail="Message not found")
    updated = await msg_service.update_message(
        db,
        msg,
        processing_status=payload.processing_status,
        content=payload.content,
    )
    return updated
