from fastapi import APIRouter

router = APIRouter()


@router.get("/health")
def health_check():
    """Simple health endpoint for readiness / liveness checks."""
    return {
        "status": "ok",
        "service": "real-estate-lead-bot",
    }
