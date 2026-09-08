"""Fire-and-forget webhook calls to n8n."""

import logging
from typing import Any, Dict, Optional
from uuid import UUID

import httpx

from app.core.config import settings

logger = logging.getLogger(__name__)


async def trigger_message_processing(
    *,
    message_id: UUID,
    conversation_id: UUID,
    lead_id: UUID,
) -> None:
    """Notify n8n that a new customer message needs processing.

    n8n owns the workflow (PRH-LEAD-PROCESS-MESSAGE). Failures are logged
    but never block the API response — the message is already persisted.
    """
    if not settings.N8N_WEBHOOK_URL:
        logger.warning("N8N_WEBHOOK_URL not set — skipping workflow trigger")
        return

    url = settings.N8N_WEBHOOK_URL.rstrip("/")
    # Support both base webhook URL and full path
    if not url.endswith("lead-process-message") and not url.endswith("webhook"):
        url = f"{url}/lead-process-message"

    payload: Dict[str, Any] = {
        "event": "MESSAGE_RECEIVED",
        "message_id": str(message_id),
        "conversation_id": str(conversation_id),
        "lead_id": str(lead_id),
    }
    headers = {"Content-Type": "application/json"}
    if settings.N8N_WEBHOOK_SECRET:
        headers["X-Webhook-Secret"] = settings.N8N_WEBHOOK_SECRET

    try:
        async with httpx.AsyncClient(timeout=10.0) as client:
            resp = await client.post(url, json=payload, headers=headers)
            if resp.status_code >= 400:
                logger.error(
                    "n8n webhook returned %s: %s", resp.status_code, resp.text[:300]
                )
            else:
                logger.info("n8n workflow triggered for message %s", message_id)
    except Exception as exc:
        logger.exception("Failed to trigger n8n webhook: %s", exc)
