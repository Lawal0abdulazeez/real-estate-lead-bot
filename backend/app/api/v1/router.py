from fastapi import APIRouter

from app.api.v1 import (
    activities,
    conversations,
    followups,
    health,
    leads,
    messages,
    qualification,
)

api_router = APIRouter()

api_router.include_router(health.router, tags=["health"])
api_router.include_router(leads.router, prefix="/leads", tags=["leads"])
api_router.include_router(
    conversations.router, prefix="/conversations", tags=["conversations"]
)
api_router.include_router(messages.router, prefix="/messages", tags=["messages"])
api_router.include_router(followups.router, prefix="/follow-ups", tags=["follow-ups"])
api_router.include_router(activities.router, prefix="/activities", tags=["activities"])
api_router.include_router(qualification.router, prefix="/qualification", tags=["qualification"])

