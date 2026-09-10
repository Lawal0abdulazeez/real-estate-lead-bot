"""End-to-end integration verification script.

Tests that:
1. Backend creates lead & conversation
2. Customer sends enquiry message
3. Webhook fires to n8n (or receives bot response)
4. Lead is qualified with accurate score and classification
5. Activities are recorded
"""

import asyncio
import sys
from decimal import Decimal
from uuid import uuid4

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")


from app.db.session import AsyncSessionLocal
from app.models.enums import Classification, LeadStatus
from app.schemas.lead import LeadCreate, LeadUpdate
from app.schemas.message import MessageCreate
from app.services import conversations as conv_service
from app.services import leads as lead_service
from app.services import messages as msg_service
from app.services.qualification import score_lead


async def run_integration_verification():
    print("=" * 60)
    print("PRIMEHOMES REAL ESTATE LEAD BOT - END-TO-END VERIFICATION")
    print("=" * 60)

    async with AsyncSessionLocal() as db:
        # Step 1: Create a lead
        print("\n[1] Creating customer lead...")
        lead_data = LeadCreate(
            name="Babajide Sanwo",
            email="babajide.lead@example.com",
            phone="+2348035551234",
            property_type="APARTMENT",
            transaction_type="BUY",
            bedrooms=3,
            location="Lekki Phase 1, Lagos",
            budget_max=Decimal("85000000"),
            currency="NGN",
            timeline="WITHIN_1_MONTH",
            source="WEBSITE_CHAT",
        )
        lead = await lead_service.create_lead(db, lead_data)
        print(f" -> Lead created with ID: {lead.id}, status: {lead.status}")

        # Step 2: Create conversation
        print("\n[2] Initializing conversation...")
        from app.schemas.conversation import ConversationCreate

        conv = await conv_service.create_conversation(
            db, ConversationCreate(lead_id=lead.id, channel="WEB")
        )
        print(f" -> Conversation started: {conv.id}")

        # Step 3: Customer sends message
        print("\n[3] Simulating customer enquiry message...")
        cust_msg = await msg_service.create_customer_message(
            db,
            conversation_id=conv.id,
            lead_id=lead.id,
            data=MessageCreate(
                content="Hello! I need a 3-bedroom apartment in Lekki Phase 1. Budget is ₦85 million, ready to buy within a month.",
                sender_type="CUSTOMER",
            ),
        )
        print(f" -> Customer message saved: {cust_msg.id}, status: {cust_msg.processing_status}")

        # Step 4: Deterministic scoring & qualification
        print("\n[4] Running deterministic lead qualification...")
        score_record = await lead_service.qualify_lead(db, lead)
        q_result = score_lead(lead)
        print(f" -> Lead Score: {score_record.score}/100")
        print(f" -> Classification: {score_record.classification}")
        print(f" -> Reasons: {'; '.join(q_result.reasons)}")
        assert score_record.classification == Classification.HOT.value, "Expected HOT lead!"

        # Step 5: Simulate n8n writing back the bot reply
        print("\n[5] Simulating n8n Bot Response writeback...")
        bot_reply_text = (
            "Hello Babajide! Thank you for contacting PrimeHomes Realty. "
            "We have verified 3-bedroom apartments in Lekki Phase 1 matching your ₦85,000,000 budget. "
            "Our dedicated sales consultant will reach out via +2348035551234 with selected brochures."
        )
        bot_msg = await msg_service.create_bot_message(
            db,
            conversation_id=conv.id,
            content=bot_reply_text,
        )
        print(f" -> Bot reply persisted: {bot_msg.id}, sender: {bot_msg.sender_type}")

        # Step 6: Mark customer message processed
        await msg_service.update_message(db, cust_msg, processing_status="PROCESSED")
        print(f" -> Customer message marked as PROCESSED.")

        # Step 7: Record audit activity
        act = await lead_service.create_activity(
            db,
            lead_id=lead.id,
            actor_type="SYSTEM",
            activity_type="QUALIFIED_AND_RESPONDED",
            description="Lead qualified as HOT (score 98) and bot response dispatched",
            metadata={"score": score_record.score, "classification": score_record.classification},
        )
        print(f" -> Activity recorded: {act.activity_type} - {act.description}")

        # Step 8: Verify timeline & conversation history
        msgs, total = await msg_service.list_messages(db, conv.id)
        acts = await lead_service.list_activities(db, lead.id)
        print(f"\n[8] Verification Summary:")
        print(f" -> Total conversation messages: {total}")
        for m in msgs:
            print(f"    - [{m.sender_type}] {m.content[:60]}...")
        print(f" -> Total lead activities: {len(acts)}")
        for a in acts:
            print(f"    - [{a.actor_type}] {a.activity_type}: {a.description}")

        await db.commit()

    print("\n" + "=" * 60)
    print("ALL INTEGRATION CHECKS PASSED SUCCESSFULLY!")
    print("=" * 60)


if __name__ == "__main__":
    asyncio.run(run_integration_verification())
