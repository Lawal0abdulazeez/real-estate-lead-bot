# TESTING_SPEC.md

# Real Estate Lead Bot — Testing Specification

## 1. Purpose

This document defines how the Real Estate Lead Bot should be tested.

The goal is to make sure that:

- The application works as expected.
- Customer messages are processed correctly.
- Leads are stored correctly.
- AI extraction works reliably.
- Lead qualification works correctly.
- n8n workflows execute correctly.
- Customer responses are generated correctly.
- Existing features are not broken when new features are added.

Testing should remain practical and proportional to the project.

---

# 2. Testing Philosophy

The project should follow:

> **Test the important things first.**

We do not need hundreds of tests before the application can run.

The priority is to test the critical customer journey:

```text
Customer Message
      ↓
FastAPI
      ↓
Lead / Conversation
      ↓
n8n
      ↓
AI
      ↓
Qualification
      ↓
Database
      ↓
Customer Response
      ↓
Sales Notification
```

---

# 3. Main Testing Areas

The project should initially have five testing areas:

```text
1. Backend/API
2. Database
3. AI
4. n8n Workflows
5. Frontend
```

---

# 4. Backend/API Testing

Backend tests should verify that the API behaves correctly.

## Health Check

Test:

```text
GET /api/v1/health
```

Expected:

```text
HTTP 200
```

Example response:

```json
{
  "status": "ok"
}
```

---

# 5. Lead API Tests

Test lead creation.

### Valid request

```json
{
  "name": "John Doe",
  "phone": "08000000000",
  "property_type": "APARTMENT",
  "bedrooms": 3,
  "location": "Lekki",
  "budget_max": 80000000,
  "transaction_type": "BUY"
}
```

Expected:

```text
Lead created successfully.
```

---

## Invalid Request

Test missing or invalid information.

Example:

```json
{
  "name": "",
  "bedrooms": -2
}
```

Expected:

```text
HTTP 400 / 422
```

The API should reject invalid data.

---

# 6. Lead Retrieval

Test:

```text
GET /api/v1/leads
```

Verify:

- Leads are returned.
- Pagination works.
- Filters work.
- Search works.
- Sorting works.

---

# 7. Lead Update

Test:

```text
PATCH /api/v1/leads/{id}
```

Verify that fields can be updated correctly.

Example:

```text
Status:
NEW → QUALIFIED
```

and:

```text
Score:
55 → 82
```

---

# 8. Conversation Testing

Test that conversations can be:

- Created.
- Retrieved.
- Associated with the correct lead.
- Associated with the correct customer/session.

Example:

```text
Lead
  ↓
Conversation
  ↓
Messages
```

The relationship should remain correct.

---

# 9. Message Testing

Test customer messages.

Example:

```text
POST /api/v1/messages
```

Input:

```json
{
  "conversation_id": "conversation-id",
  "content": "I want a 3-bedroom apartment in Lekki."
}
```

Expected:

```text
Message stored successfully.
```

The system should also trigger the appropriate processing flow.

---

# 10. Duplicate Message Testing

The same message should not accidentally create duplicate processing.

Example:

```text
Customer Message ID:
msg-123
```

If:

```text
msg-123
```

is received twice, the system should recognize that it has already been processed.

Expected:

```text
One message
One processing operation
```

rather than:

```text
Two leads
Two bot responses
Two notifications
```

---

# 11. AI Testing

AI should be tested with realistic customer messages.

The goal is to confirm that information is extracted correctly.

---

## Test Case 1 — Complete Enquiry

Input:

```text
Hi, I'm looking for a 3-bedroom apartment in Lekki.
My budget is ₦80 million and I want to buy within 3 months.
```

Expected:

```json
{
  "intent": "BUY",
  "property_type": "APARTMENT",
  "bedrooms": 3,
  "location": "Lekki",
  "budget_max": 80000000,
  "timeline": "WITHIN_3_MONTHS"
}
```

---

# 12. AI Test Case — Rental

Input:

```text
I need a 2 bedroom apartment to rent in Ikeja.
```

Expected:

```json
{
  "intent": "RENT",
  "property_type": "APARTMENT",
  "bedrooms": 2,
  "location": "Ikeja"
}
```

---

# 13. AI Test Case — Land

Input:

```text
I'm looking for land around Ibadan below ₦20 million.
```

Expected:

```json
{
  "intent": "LAND",
  "property_type": "LAND",
  "location": "Ibadan",
  "budget_max": 20000000
}
```

---

# 14. AI Test Case — Incomplete Information

Input:

```text
I want to buy a house in Lekki.
```

Expected:

```text
Intent → BUY
Property → HOUSE
Location → Lekki
```

Missing:

```text
Budget
Timeline
Possibly bedrooms
```

The system should ask a useful follow-up question.

---

# 15. AI Test Case — Human Request

Input:

```text
Can I speak with someone from the sales team?
```

Expected:

```text
intent = HUMAN_AGENT
```

The system should initiate the appropriate human handoff process.

---

# 16. AI Test Case — Unclear Message

Input:

```text
I need something nice around there.
```

The system should not invent:

```text
Property type
Budget
Location
Bedrooms
```

Instead, it should ask for clarification.

---

# 17. AI Test Case — Ambiguous Budget

Input:

```text
My budget is around 50-ish.
```

The system should not automatically assume:

```text
₦50 million
```

It should clarify the customer's intended budget.

---

# 18. AI Output Validation

Every AI response should be validated before being used.

Example:

```text
AI
 ↓
Structured JSON
 ↓
Schema Validation
 ↓
Business Validation
 ↓
Use Result
```

If the AI returns invalid information:

```text
AI Output
   ↓
Invalid
   ↓
Do not store blindly
   ↓
Retry / fallback / ask clarification
```

---

# 19. Lead Qualification Testing

Test the scoring rules separately from AI.

Example:

```text
Intent: BUY
Property: APARTMENT
Bedrooms: 3
Location: Lekki
Budget: ₦80M
Timeline: Within 3 months
Phone: Available
Name: Available
```

Expected result should be within the documented scoring rules.

Example:

```text
Score: 92
Classification: HOT
```

---

# 20. Qualification Boundary Tests

Test scores around classification boundaries.

### Test

```text
Score = 80
```

Expected:

```text
HOT
```

### Test

```text
Score = 79
```

Expected:

```text
WARM
```

### Test

```text
Score = 60
```

Expected:

```text
WARM
```

### Test

```text
Score = 59
```

Expected:

```text
COLD
```

### Test

```text
Score = 30
```

Expected:

```text
COLD
```

### Test

```text
Score = 29
```

Expected:

```text
UNQUALIFIED
```

These boundary tests are important because small changes should not produce unexpected classifications.

---

# 21. Lead Requalification

Test that a lead can improve over time.

Example:

```text
First message
Score = 25
Classification = UNQUALIFIED
```

Customer later provides:

```text
Budget
Location
Timeline
Property type
```

Expected:

```text
New Score = Higher
Classification = Updated
```

The previous score should remain available in the score history if score history is implemented.

---

# 22. n8n Workflow Testing

The main workflow:

```text
PRH-LEAD-PROCESS-MESSAGE
```

should be tested from beginning to end.

Expected flow:

```text
Webhook
 ↓
Validate
 ↓
Get Context
 ↓
AI
 ↓
Validate AI Result
 ↓
Update Lead
 ↓
Qualification
 ↓
Generate Response
 ↓
Save Response
 ↓
Notify Customer
```

---

# 23. n8n Success Test

Input:

```text
I want a 3-bedroom apartment in Lekki.
My budget is ₦80 million.
```

Expected:

```text
Workflow succeeds.
Lead is updated.
Score is calculated.
Bot response is created.
```

---

# 24. n8n Failure Test

Simulate an AI failure.

Expected:

```text
AI fails
 ↓
Workflow handles failure
 ↓
Customer message remains stored
 ↓
Customer is not left with corrupted data
 ↓
Error is logged
```

The system should not lose the customer's original message.

---

# 25. Notification Failure

Simulate a sales notification failure.

Expected:

```text
Lead remains stored.
Lead score remains stored.
Notification failure is recorded.
```

A failed notification should not delete or corrupt the lead.

---

# 26. Google Sheets Failure

Simulate Google Sheets being unavailable.

Expected:

```text
PostgreSQL
   ↓
Lead remains safely stored

Google Sheets
   ↓
Sync fails
```

The lead should still exist in PostgreSQL.

The system can retry synchronization later.

---

# 27. Frontend Testing

The React application should test the main customer journey.

### Customer Chat

Verify:

- Chat loads.
- User can type.
- Message can be sent.
- Message appears in conversation.
- Loading state appears.
- Bot response appears.
- Errors are displayed correctly.

---

# 28. Frontend Error Testing

Test when:

- Backend is unavailable.
- Request times out.
- Message fails.
- Customer sends empty message.
- Customer sends multiple messages quickly.

The UI should provide a clear response.

Example:

```text
Unable to send your message.
Please try again.
```

---

# 29. Sales Dashboard Testing

Verify that sales users can:

- Log in.
- View leads.
- Search leads.
- Filter leads.
- Open lead details.
- View conversations.
- View lead score.
- View classification.
- Update status.
- Assign leads.
- Create follow-ups.

---

# 30. End-to-End Test

The most important test should simulate a real customer.

### Step 1

Customer sends:

```text
Hi, I'm looking for a 3-bedroom apartment in Lekki.
```

### Step 2

System extracts:

```text
BUY / APARTMENT / 3 BEDROOMS / LEKKI
```

### Step 3

Bot asks:

```text
What budget range are you considering and how soon
are you looking to buy?
```

### Step 4

Customer responds:

```text
My budget is ₦80 million and I want to buy within 2 months.
```

### Step 5

System updates:

```text
Budget = ₦80M
Timeline = WITHIN_3_MONTHS
```

### Step 6

System calculates:

```text
Lead Score
```

### Step 7

System classifies:

```text
HOT / WARM / COLD / UNQUALIFIED
```

### Step 8

System stores:

```text
Lead
Conversation
Messages
Score
```

### Step 9

If HOT:

```text
Sales Notification
```

### Step 10

Customer receives:

```text
Bot Response
```

This complete journey should work before considering the MVP ready.

---

# 31. Regression Testing

Whenever an important feature is changed, test the existing customer journey again.

For example:

```text
Change AI prompt
      ↓
Run AI tests
      ↓
Run qualification tests
      ↓
Run end-to-end lead flow
```

Do not assume that changing one part cannot affect another part.

---

# 32. Test Data

Use fake data for development and testing.

Example:

```text
Name:
John Doe

Phone:
08000000000

Email:
john@example.com

Location:
Lekki

Budget:
₦80,000,000
```

Do not use real customer information in development or automated tests.

---

# 33. Test Environment

Development and testing should use a separate environment from production.

Example:

```text
Development
    ↓
Development Database
    ↓
Development n8n
```

Production:

```text
Production
    ↓
Production Database
    ↓
Production n8n
```

Do not run automated tests against the production database.

---

# 34. Test Naming

Tests should have clear names.

Good:

```text
test_create_lead_with_valid_data
test_reject_invalid_bedroom_count
test_classify_score_80_as_hot
test_extract_buy_intent
test_handle_ai_failure
```

Avoid vague names such as:

```text
test_one
test_new
test_stuff
```

---

# 35. Minimum Test Coverage for MVP

Before calling the MVP stable, verify at minimum:

### Backend

- Health endpoint.
- Lead creation.
- Lead retrieval.
- Lead update.
- Message creation.
- Validation errors.

### AI

- BUY.
- RENT.
- LAND.
- Missing information.
- Human handoff.
- Unclear requests.

### Qualification

- Correct score calculation.
- Classification boundaries.
- Score updates.

### n8n

- Successful workflow.
- AI failure.
- Notification failure.
- Duplicate message.

### Frontend

- Send message.
- Display response.
- Display error.
- View lead.
- Update lead.

### End-to-End

At least one complete customer journey should pass successfully.

---

# 36. Testing Before Deployment

Before deploying a new version:

```text
1. Run backend tests
        ↓
2. Run AI tests
        ↓
3. Run qualification tests
        ↓
4. Test n8n workflow
        ↓
5. Test frontend
        ↓
6. Run end-to-end test
        ↓
7. Review errors
        ↓
8. Deploy
```

---

# 37. Definition of Done

A feature is considered tested when:

- The normal case works.
- Invalid input is handled.
- Important edge cases are considered.
- Errors do not corrupt data.
- Existing functionality still works.
- Relevant automated tests pass.
- The complete customer flow still works when applicable.

---

# 38. Final Testing Principle

The purpose of testing is not to make the project complicated.

The purpose is to give us confidence that:

```text
Customer
   ↓
Message
   ↓
AI
   ↓
Lead
   ↓
Qualification
   ↓
Database
   ↓
Sales Team
```

works reliably.

Start with the critical paths.

Add more tests when the application grows or real-world problems reveal new cases.