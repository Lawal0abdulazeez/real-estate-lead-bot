import pytest
from httpx import ASGITransport, AsyncClient

from app.main import app


@pytest.mark.asyncio
async def test_activities_and_followups_and_qualification():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        # 1. Create a lead first
        lead_resp = await client.post(
            "/api/v1/leads",
            json={
                "name": "Integration Test Lead",
                "phone": "+2348011223344",
                "property_type": "APARTMENT",
                "transaction_type": "BUY",
                "budget_max": 85000000,
                "location": "Lekki Phase 1",
                "timeline": "IMMEDIATE",
            },
        )
        assert lead_resp.status_code == 201
        lead_data = lead_resp.json()
        lead_id = lead_data["id"]

        # 2. Test POST /api/v1/activities (direct payload)
        act_resp = await client.post(
            "/api/v1/activities",
            json={
                "lead_id": lead_id,
                "activity_type": "WORKFLOW_TEST",
                "description": "Activity from n8n test",
                "metadata": {"source": "unit-test"},
            },
        )
        assert act_resp.status_code == 201
        act_data = act_resp.json()
        assert act_data["lead_id"] == lead_id
        assert act_data["activity_type"] == "WORKFLOW_TEST"

        # 3. Test POST /api/v1/activities (wrapped in body, matching n8n httpRequest v2)
        act_resp2 = await client.post(
            "/api/v1/activities",
            json={
                "body": {
                    "lead_id": lead_id,
                    "activity_type": "LEAD_QUALIFIED",
                    "description": "Lead qualified via n8n",
                }
            },
        )
        assert act_resp2.status_code == 201

        # 4. Test POST /api/v1/qualification/calculate
        calc_resp = await client.post(
            "/api/v1/qualification/calculate",
            json={"lead_id": lead_id},
        )
        assert calc_resp.status_code == 200
        calc_data = calc_resp.json()
        assert "score" in calc_data
        assert "classification" in calc_data
        assert calc_data["score"] > 0

        # 5. Test POST /api/v1/qualification/score-history
        score_resp = await client.post(
            "/api/v1/qualification/score-history",
            json={
                "lead_id": lead_id,
                "score": 85,
                "classification": "HOT",
                "reason": "Test high intent",
            },
        )
        assert score_resp.status_code == 200
        assert score_resp.json()["ok"] is True

        # 6. Test POST /api/v1/follow-ups
        fu_resp = await client.post(
            "/api/v1/follow-ups",
            json={
                "lead_id": lead_id,
                "type": "CALL",
                "notes": "Follow up regarding Lekki apartment",
                "channel": "PHONE",
            },
        )
        assert fu_resp.status_code == 201
        fu_data = fu_resp.json()
        fu_id = fu_data["id"]

        # 7. Test GET /api/v1/follow-ups/due
        due_resp = await client.get("/api/v1/follow-ups/due")
        assert due_resp.status_code == 200
        due_list = due_resp.json()
        assert isinstance(due_list, list)

        # 8. Test PATCH /api/v1/follow-ups/{id}
        patch_resp = await client.patch(
            f"/api/v1/follow-ups/{fu_id}",
            json={"status": "REMINDER_SENT"},
        )
        assert patch_resp.status_code == 200
        assert patch_resp.json()["status"] == "REMINDER_SENT"

        # 9. Test POST /api/v1/qualification/notifications/sales
        notif_resp = await client.post(
            "/api/v1/qualification/notifications/sales",
            json={"event": "HOT_LEAD", "lead_id": lead_id},
        )
        assert notif_resp.status_code == 200
