from fastapi import APIRouter

from app.api.v1 import conversations, health, leads

api_router = APIRouter()

api_router.include_router(health.router, tags=["health"])
api_router.include_router(leads.router, prefix="/leads", tags=["leads"])
api_router.include_router(
    conversations.router, prefix="/conversations", tags=["conversations"]
)
