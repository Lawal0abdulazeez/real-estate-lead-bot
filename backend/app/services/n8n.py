"""Fire-and-forget webhook calls to n8n."""

import logging
from datetime import datetime, timezone
from typing import Any, Dict
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
    if url.endswith("/webhook"):
        url = f"{url}/lead-process-message"

    payload: Dict[str, Any] = {
        "event": "MESSAGE_RECEIVED",
        "message_id": str(message_id),
        "conversation_id": str(conversation_id),
        "lead_id": str(lead_id),
        "timestamp": datetime.now(timezone.utc).isoformat(),
    }
    headers = {"Content-Type": "application/json"}
    if settings.N8N_WEBHOOK_SECRET:
        headers["X-Webhook-Secret"] = settings.N8N_WEBHOOK_SECRET

    try:
        async with httpx.AsyncClient(timeout=10.0) as client:
            resp = await client.post(url, json=payload, headers=headers)
            
            # Bidirectional Dev vs Published fallback:
            # 1. If 404 on /webhook/, retry on dev test webhook /webhook-test/
            # 2. If 404 on /webhook-test/, retry on production webhook /webhook/
            if resp.status_code == 404:
                alt_url = None
                if "/webhook/" in url:
                    alt_url = url.replace("/webhook/", "/webhook-test/")
                elif "/webhook-test/" in url:
                    alt_url = url.replace("/webhook-test/", "/webhook/")

                if alt_url:
                    try:
                        dev_resp = await client.post(alt_url, json=payload, headers=headers)
                        if dev_resp.status_code < 400:
                            mode_name = "DEV test" if "/webhook-test/" in alt_url else "PUBLISHED production"
                            logger.info("n8n workflow triggered on %s webhook (%s) for message %s", mode_name, alt_url, message_id)
                            return
                    except Exception:
                        pass

            if resp.status_code >= 400:
                logger.error(
                    "n8n webhook returned %s: %s", resp.status_code, resp.text[:300]
                )
            else:
                mode_name = "DEV test" if "/webhook-test/" in url else "PUBLISHED production"
                logger.info("n8n workflow triggered on %s webhook for message %s", mode_name, message_id)
    except Exception as exc:
        logger.exception("Failed to trigger n8n webhook: %s", exc)

