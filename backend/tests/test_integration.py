import pytest
from httpx import ASGITransport, AsyncClient

from app.main import app


@pytest.mark.asyncio
async def test_full_lead_lifecycle_integration():
    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://test"
    ) as client:
        # 1. Create a lead
        lead_resp = await client.post(
            "/api/v1/leads",
            json={
                "name": "Ibrahim Adeyemi",
                "email": "ibrahim@example.com",
                "phone": "+2348012345678",
                "property_type": "APARTMENT",
                "transaction_type": "BUY",
                "bedrooms": 3,
                "location": "Lekki Phase 1",
                "budget_max": 85000000,
                "timeline": "WITHIN_1_MONTH",
            },
        )
        assert lead_resp.status_code == 201, lead_resp.text
        lead = lead_resp.json()
        lead_id = lead["id"]
        assert lead["status"] == "NEW"

        # 2. Qualify lead
        qualify_resp = await client.post(f"/api/v1/leads/{lead_id}/qualify")
        assert qualify_resp.status_code == 200
        q_data = qualify_resp.json()
        assert q_data["score"] >= 80
        assert q_data["classification"] == "HOT"
        assert q_data["qualified"] is True

        # 3. Create conversation for lead
        conv_resp = await client.post(
            "/api/v1/conversations",
            json={"lead_id": lead_id, "channel": "WEB"},
        )
        assert conv_resp.status_code == 201
        conv = conv_resp.json()
        conv_id = conv["id"]

        # 4. Post customer message
        cust_msg_resp = await client.post(
            f"/api/v1/conversations/{conv_id}/messages",
            json={
                "content": "Looking for 3 bedroom apartment in Lekki, budget is 85m",
                "sender_type": "CUSTOMER",
            },
        )
        assert cust_msg_resp.status_code == 201
        cust_msg = cust_msg_resp.json()
        msg_id = cust_msg["id"]
        assert cust_msg["sender_type"] == "CUSTOMER"
        assert cust_msg["processing_status"] in ("PROCESSING", "RECEIVED")

        # 5. Get message by ID
        get_msg_resp = await client.get(f"/api/v1/messages/{msg_id}")
        assert get_msg_resp.status_code == 200
        assert get_msg_resp.json()["id"] == msg_id

        # 6. Post bot response (as n8n does)
        bot_msg_resp = await client.post(
            f"/api/v1/conversations/{conv_id}/messages",
            json={
                "content": "Thank you! We have verified 3-bedroom apartments in Lekki Phase 1 within your 85M NGN budget.",
                "sender_type": "BOT",
            },
        )
        assert bot_msg_resp.status_code == 201
        bot_msg = bot_msg_resp.json()
        assert bot_msg["sender_type"] == "BOT"
        assert bot_msg["processing_status"] == "PROCESSED"

        # 7. Mark original customer message as processed
        patch_msg_resp = await client.patch(
            f"/api/v1/messages/{msg_id}",
            json={"processing_status": "PROCESSED"},
        )
        assert patch_msg_resp.status_code == 200
        assert patch_msg_resp.json()["processing_status"] == "PROCESSED"

        # 8. Record an activity
        act_resp = await client.post(
            f"/api/v1/leads/{lead_id}/activities",
            json={
                "actor_type": "SYSTEM",
                "activity_type": "WORKFLOW_COMPLETED",
                "description": "PRH-LEAD-PROCESS-MESSAGE processed lead message",
                "metadata": {"score": q_data["score"]},
            },
        )
        assert act_resp.status_code == 201
        act_data = act_resp.json()
        assert act_data["activity_type"] == "WORKFLOW_COMPLETED"

        # 9. List activities
        list_acts = await client.get(f"/api/v1/leads/{lead_id}/activities")
        assert list_acts.status_code == 200
        assert len(list_acts.json()) >= 1

        # 10. List messages for conversation
        msgs_resp = await client.get(f"/api/v1/conversations/{conv_id}/messages")
        assert msgs_resp.status_code == 200
        assert msgs_resp.json()["total"] >= 2
