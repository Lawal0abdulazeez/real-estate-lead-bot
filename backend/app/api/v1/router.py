from fastapi import APIRouter

from app.api.v1 import health

api_router = APIRouter()

api_router.include_router(health.router, tags=["health"])

# Future routers (Phase 5+):
# from app.api.v1 import auth, leads, conversations, messages, followups
# api_router.include_router(auth.router, prefix="/auth", tags=["auth"])
# api_router.include_router(leads.router, prefix="/leads", tags=["leads"])
# api_router.include_router(conversations.router, prefix="/conversations", tags=["conversations"])
# api_router.include_router(messages.router, prefix="/messages", tags=["messages"])
# api_router.include_router(followups.router, prefix="/follow-ups", tags=["follow-ups"])
