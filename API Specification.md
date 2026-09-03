# API Specification

## PrimeHomes Realty — Real Estate Lead Bot

**Document:** API Specification  
**Version:** 1.0  
**Status:** Draft  
**Backend:** Python + FastAPI  
**Frontend:** React  
**Automation:** n8n  
**Database:** PostgreSQL  
**API Style:** REST  
**Primary Format:** JSON

---

# 1. Purpose

This document defines the API contract for the PrimeHomes Realty Real Estate Lead Bot.

The API is the controlled communication layer between the frontend, backend services, n8n workflows, AI processing, and database.

It defines:

- API endpoints
- HTTP methods
- Request schemas
- Response schemas
- Validation rules
- Authentication
- Authorization
- Error handling
- Pagination
- Filtering
- Webhooks
- Idempotency
- n8n integration
- AI integration boundaries
- API versioning

This document should be treated as the **contract between system components**.

Any developer or AI coding agent implementing an API consumer or provider should follow this specification.

---

# 2. API Architecture

The primary application architecture is:

```text
┌──────────────────┐
│      React       │
│    Frontend      │
└────────┬─────────┘
         │
         │ HTTPS / JSON
         ▼
┌──────────────────┐
│     FastAPI      │
│   REST API       │
└────────┬─────────┘
         │
         ├───────────────┐
         │               │
         ▼               ▼
┌────────────────┐ ┌───────────────┐
│   PostgreSQL   │ │      n8n      │
│   Database     │ │   Workflows   │
└────────────────┘ └───────┬───────┘
                            │
                   ┌────────┼────────┐
                   ▼        ▼        ▼
                  AI    Google     Notifications
                        Sheets
```

---

# 3. API Design Principle

The API should follow this principle:

> **FastAPI owns application access and business boundaries. n8n owns workflow orchestration.**

This means n8n should not become the application's unrestricted database/API layer.

For example:

```text
React
  ↓
FastAPI
  ↓
Business Logic
  ↓
Database
```

rather than:

```text
React
  ↓
n8n
  ↓
Database
```

n8n can still communicate with FastAPI for automation-specific operations.

---

# 4. API Base URL

Development:

```text
http://localhost:8000
```

Production:

```text
https://api.primehomes.example
```

The production domain is a placeholder and must be replaced with the actual deployment domain.

---

# 5. API Versioning

All public application endpoints should be versioned.

Initial version:

```text
/api/v1
```

Example:

```text
/api/v1/leads
```

Future breaking changes should use:

```text
/api/v2
```

Avoid silently changing the behaviour of an existing API contract.

---

# 6. Content Type

Requests containing JSON should use:

```http
Content-Type: application/json
```

Responses should normally use:

```http
Content-Type: application/json
```

---

# 7. Authentication

Internal application APIs should use authenticated requests.

The preferred MVP authentication model is:

```text
JWT
```

Conceptual flow:

```text
User
 ↓
POST /auth/login
 ↓
FastAPI
 ↓
JWT Access Token
 ↓
React
 ↓
Authorization Header
```

Example:

```http
Authorization: Bearer <access_token>
```

---

# 8. Authentication Responsibilities

FastAPI is responsible for:

- Validating credentials.
- Generating tokens.
- Validating tokens.
- Identifying users.
- Checking user status.
- Enforcing authorization.

React must never contain:

- Database credentials.
- n8n credentials.
- AI provider API keys.
- Internal service secrets.

---

# 9. Roles

Initial roles:

```text
ADMIN
MANAGER
SALES_AGENT
```

Authorization should be role-aware.

Example:

```text
ADMIN
 ├── Manage users
 ├── Manage leads
 ├── View reports
 └── Configure system

MANAGER
 ├── View leads
 ├── Assign leads
 ├── Manage follow-ups
 └── View reports

SALES_AGENT
 ├── View assigned leads
 ├── Update leads
 ├── Add notes
 └── Manage follow-ups
```

---

# 10. API Resource Model

The initial API resources are:

```text
/auth
/users
/leads
/conversations
/messages
/scores
/follow-ups
/activities
/integrations
/health
```

Future resources may include:

```text
/properties
/appointments
/notifications
/analytics
```

---

# 11. Health Check

## Endpoint

```http
GET /health
```

Purpose:

Determine whether the API service is running.

### Response

```json
{
  "status": "ok"
}
```

---

# 12. Detailed Health Check

A future internal endpoint may expose dependency health.

```http
GET /health/ready
```

Example:

```json
{
  "status": "ok",
  "database": "ok",
  "n8n": "ok"
}
```

This endpoint should not expose secrets or sensitive infrastructure information.

---

# 13. Authentication Endpoints

## Login

```http
POST /api/v1/auth/login
```

### Request

```json
{
  "email": "agent@primehomes.com",
  "password": "********"
}
```

### Response

```json
{
  "access_token": "jwt-token",
  "token_type": "bearer",
  "expires_in": 3600,
  "user": {
    "id": "uuid",
    "name": "Sales Agent",
    "email": "agent@primehomes.com",
    "role": "SALES_AGENT"
  }
}
```

---

# 14. Current User

```http
GET /api/v1/auth/me
```

Returns the authenticated user's profile.

Example:

```json
{
  "id": "uuid",
  "name": "John Doe",
  "email": "john@example.com",
  "role": "SALES_AGENT",
  "status": "ACTIVE"
}
```

---

# 15. Lead Creation

## Endpoint

```http
POST /api/v1/leads
```

Purpose:

Create a new lead.

### Request

```json
{
  "name": "John Doe",
  "email": "john@example.com",
  "phone": "+2348012345678",
  "property_type": "APARTMENT",
  "transaction_type": "BUY",
  "bedrooms": 3,
  "location": "Lekki",
  "budget_max": 80000000,
  "currency": "NGN",
  "timeline": "WITHIN_3_MONTHS",
  "source": "WEBSITE"
}
```

---

# 16. Lead Creation Response

HTTP status:

```text
201 Created
```

Example:

```json
{
  "id": "550e8400-e29b-41d4-a716-446655440000",
  "name": "John Doe",
  "email": "john@example.com",
  "phone": "+2348012345678",
  "property_type": "APARTMENT",
  "transaction_type": "BUY",
  "bedrooms": 3,
  "location": "Lekki",
  "budget_max": 80000000,
  "currency": "NGN",
  "timeline": "WITHIN_3_MONTHS",
  "status": "NEW",
  "classification": null,
  "score": null,
  "source": "WEBSITE",
  "created_at": "2026-09-03T10:30:00Z",
  "updated_at": "2026-09-03T10:30:00Z"
}
```

---

# 17. Get Lead

```http
GET /api/v1/leads/{lead_id}
```

Example:

```http
GET /api/v1/leads/550e8400-e29b-41d4-a716-446655440000
```

Returns the complete lead summary available to the authenticated user.

---

# 18. Update Lead

```http
PATCH /api/v1/leads/{lead_id}
```

Use `PATCH` for partial updates.

Example:

```json
{
  "budget_max": 90000000,
  "timeline": "IMMEDIATE"
}
```

Response:

```text
200 OK
```

The backend should validate whether the requested changes are permitted.

---

# 19. Lead Status Update

Status transitions should have a dedicated operation where business rules are important.

```http
POST /api/v1/leads/{lead_id}/status
```

### Request

```json
{
  "status": "CONTACTED",
  "reason": "Sales agent contacted customer by phone."
}
```

The backend should validate the transition.

Example:

```text
NEW → CONTACTED
```

may be invalid if qualification or assignment is required first.

---

# 20. Lead Classification

Classification should normally be calculated by the qualification service.

Example:

```text
POST /api/v1/leads/{lead_id}/qualify
```

The backend/n8n workflow can trigger qualification.

Response:

```json
{
  "lead_id": "uuid",
  "score": 85,
  "classification": "HOT",
  "reason": "High budget, specific property, clear location and immediate timeline."
}
```

---

# 21. Lead List

```http
GET /api/v1/leads
```

Basic response:

```json
{
  "items": [],
  "page": 1,
  "limit": 20,
  "total": 0
}
```

---

# 22. Lead Filtering

Supported query parameters:

```text
status
classification
property_type
transaction_type
location
assigned_to
source
min_score
max_score
created_from
created_to
```

Example:

```http
GET /api/v1/leads?classification=HOT&status=QUALIFIED
```

---

# 23. Lead Sorting

Supported initial sort fields:

```text
created_at
updated_at
score
next_follow_up_at
```

Example:

```http
GET /api/v1/leads?sort=score&order=desc
```

The backend must validate allowed sort fields.

Arbitrary database expressions must never be accepted from clients.

---

# 24. Pagination

Initial pagination:

```text
page
limit
```

Example:

```http
GET /api/v1/leads?page=1&limit=20
```

Response:

```json
{
  "items": [],
  "page": 1,
  "limit": 20,
  "total": 120,
  "total_pages": 6
}
```

The API should impose a maximum page size.

Example:

```text
limit <= 100
```

---

# 25. Conversation Creation

```http
POST /api/v1/conversations
```

Example:

```json
{
  "lead_id": "lead-uuid",
  "channel": "WEB"
}
```

Response:

```json
{
  "id": "conversation-uuid",
  "lead_id": "lead-uuid",
  "channel": "WEB",
  "status": "ACTIVE",
  "created_at": "2026-09-03T10:30:00Z"
}
```

---

# 26. Get Conversation

```http
GET /api/v1/conversations/{conversation_id}
```

Returns conversation metadata.

---

# 27. Get Conversation Messages

```http
GET /api/v1/conversations/{conversation_id}/messages
```

Example:

```http
GET /api/v1/conversations/123/messages?page=1&limit=50
```

Response:

```json
{
  "items": [
    {
      "id": "message-1",
      "sender_type": "CUSTOMER",
      "content": "I need a three bedroom apartment.",
      "created_at": "2026-09-03T10:31:00Z"
    }
  ],
  "page": 1,
  "limit": 50,
  "total": 1
}
```

---

# 28. Send Message

```http
POST /api/v1/conversations/{conversation_id}/messages
```

Request:

```json
{
  "content": "I am looking for a 3-bedroom apartment in Lekki."
}
```

Response:

```json
{
  "id": "message-uuid",
  "conversation_id": "conversation-uuid",
  "sender_type": "CUSTOMER",
  "content": "I am looking for a 3-bedroom apartment in Lekki.",
  "created_at": "2026-09-03T10:32:00Z"
}
```

The message creation may trigger an n8n workflow.

---

# 29. Customer Chat Flow

For the public customer-facing chat, the expected flow is:

```text
Customer
   ↓
React
   ↓
POST /conversations/{id}/messages
   ↓
FastAPI
   ↓
Persist Message
   ↓
Trigger Processing
   ↓
n8n
   ↓
AI
   ↓
Extract Requirements
   ↓
Update Lead
   ↓
Generate Response
   ↓
Return/Deliver Response
```

---

# 30. Asynchronous Processing

AI processing may take longer than a normal API request.

The system should therefore support asynchronous processing.

Preferred architecture:

```text
POST message
      ↓
Save message
      ↓
Return acknowledgement
      ↓
Trigger workflow
      ↓
n8n
      ↓
AI processing
      ↓
Persist response
```

The API should not unnecessarily block the customer request while long-running processing occurs.

---

# 31. Message Processing Status

A message may have a processing state.

Conceptually:

```text
RECEIVED
PROCESSING
PROCESSED
FAILED
```

Example:

```json
{
  "message_id": "uuid",
  "status": "PROCESSING"
}
```

---

# 32. n8n Webhook

n8n may expose a webhook to receive processing events.

Example:

```http
POST /webhooks/n8n/lead-processing
```

However, webhook URLs and authentication mechanisms should be kept private.

The exact production n8n URL will be environment-specific.

---

# 33. FastAPI → n8n Event

When a new customer message requires AI processing:

```text
FastAPI
   ↓
n8n Webhook
```

Payload:

```json
{
  "event": "MESSAGE_RECEIVED",
  "message_id": "uuid",
  "conversation_id": "uuid",
  "lead_id": "uuid",
  "timestamp": "2026-09-03T10:32:00Z"
}
```

n8n should retrieve whatever additional data it requires through authorized APIs rather than receiving excessive customer data in every event.

---

# 34. n8n → FastAPI

n8n may call internal APIs to update application data.

Examples:

```text
POST /api/v1/leads/{id}/qualify
PATCH /api/v1/leads/{id}
POST /api/v1/leads/{id}/activities
POST /api/v1/conversations/{id}/messages
```

n8n should not directly manipulate PostgreSQL tables.

---

# 35. Internal Service Authentication

Requests from n8n to FastAPI should use a service credential.

Conceptually:

```http
Authorization: Bearer <service-token>
```

or an equivalent secure mechanism.

Service credentials must be stored in n8n's credential system/environment secrets.

They must not be hard-coded inside workflow nodes.

---

# 36. AI Extraction Contract

The AI layer should produce structured output.

Example:

```json
{
  "intent": "BUY",
  "property_type": "APARTMENT",
  "bedrooms": 3,
  "location": "Lekki",
  "budget_min": null,
  "budget_max": 80000000,
  "currency": "NGN",
  "timeline": "WITHIN_3_MONTHS",
  "confidence": 0.94
}
```

AI output should be treated as **untrusted input**.

FastAPI/n8n must validate it before writing it to the database.

---

# 37. AI Must Not Write Directly to the Database

Preferred:

```text
AI
 ↓
Structured JSON
 ↓
Validation
 ↓
Business Rules
 ↓
FastAPI
 ↓
Database
```

Avoid:

```text
AI
 ↓
Database
```

The AI model should never have unrestricted database access.

---

# 38. Partial Information

Customers may provide incomplete information.

Example:

```text
"I need a house in Lekki."
```

AI output:

```json
{
  "property_type": "HOUSE",
  "location": "Lekki",
  "transaction_type": null,
  "bedrooms": null,
  "budget_max": null,
  "timeline": null
}
```

The system should identify missing high-value information and continue the conversation.

---

# 39. Qualification Endpoint

```http
POST /api/v1/leads/{lead_id}/qualify
```

Purpose:

Calculate or refresh lead qualification.

Response:

```json
{
  "lead_id": "uuid",
  "score": 78,
  "classification": "WARM",
  "missing_fields": [
    "timeline"
  ],
  "qualified": true
}
```

---

# 40. Lead Assignment

```http
POST /api/v1/leads/{lead_id}/assign
```

Request:

```json
{
  "user_id": "sales-agent-uuid"
}
```

Response:

```json
{
  "lead_id": "lead-uuid",
  "assigned_to": "sales-agent-uuid",
  "assigned_at": "2026-09-03T11:00:00Z"
}
```

Only authorized users should be able to assign leads.

---

# 41. Follow-Up Creation

```http
POST /api/v1/leads/{lead_id}/follow-ups
```

Request:

```json
{
  "type": "CALL",
  "scheduled_at": "2026-09-04T10:00:00Z",
  "notes": "Discuss available 3-bedroom apartments."
}
```

Response:

```json
{
  "id": "follow-up-uuid",
  "lead_id": "lead-uuid",
  "type": "CALL",
  "status": "PENDING",
  "scheduled_at": "2026-09-04T10:00:00Z"
}
```

---

# 42. List Follow-Ups

```http
GET /api/v1/follow-ups
```

Supported filters:

```text
status
assigned_to
scheduled_from
scheduled_to
lead_id
```

---

# 43. Complete Follow-Up

```http
POST /api/v1/follow-ups/{follow_up_id}/complete
```

Request:

```json
{
  "notes": "Customer requested property inspection next week."
}
```

The backend should:

```text
Mark follow-up completed
        ↓
Create activity
        ↓
Update lead
        ↓
Potentially create next follow-up
```

---

# 44. Activity API

```http
GET /api/v1/leads/{lead_id}/activities
```

Returns the lead's activity timeline.

Example:

```json
{
  "items": [
    {
      "type": "LEAD_CREATED",
      "description": "Lead created from website.",
      "created_at": "2026-09-03T10:30:00Z"
    },
    {
      "type": "AI_PROCESSED",
      "description": "Customer requirements extracted.",
      "created_at": "2026-09-03T10:31:00Z"
    },
    {
      "type": "SCORE_CHANGED",
      "description": "Lead score changed from 55 to 82.",
      "created_at": "2026-09-03T10:32:00Z"
    }
  ]
}
```

---

# 45. Error Response Standard

All API errors should follow a consistent structure.

Example:

```json
{
  "error": {
    "code": "VALIDATION_ERROR",
    "message": "The request contains invalid data.",
    "details": [
      {
        "field": "bedrooms",
        "message": "Bedrooms must be greater than zero."
      }
    ],
    "request_id": "req_123456"
  }
}
```

---

# 46. HTTP Status Codes

The API should use standard HTTP status codes.

| Status | Meaning |
|---|---|
| 200 | Successful request |
| 201 | Resource created |
| 202 | Request accepted for asynchronous processing |
| 204 | Successful request with no response body |
| 400 | Bad request |
| 401 | Authentication required |
| 403 | Insufficient permission |
| 404 | Resource not found |
| 409 | Conflict |
| 422 | Validation error |
| 429 | Rate limit exceeded |
| 500 | Internal server error |
| 502 | External service failure |
| 503 | Service unavailable |

---

# 47. Request ID

Every API request should have a request identifier.

Example:

```http
X-Request-ID: req_123456
```

If the client does not provide one, FastAPI should generate it.

The request ID should appear in:

- Logs
- Error responses
- Traces
- n8n workflow logs where appropriate

This is important for debugging distributed workflows.

---

# 48. Idempotency

Operations that can accidentally be repeated should support idempotency.

Example:

```http
Idempotency-Key: msg_external_123
```

This is especially important for:

- Webhooks
- Message ingestion
- Lead creation
- Notifications
- External integrations

---

# 49. Duplicate Lead Prevention

The system should attempt to prevent accidental duplicate leads.

Possible matching signals:

```text
phone
email
external_customer_id
active_conversation
```

However, matching must not automatically merge customers based on weak evidence.

A duplicate detection strategy should be explicitly defined before implementation.

---

# 50. Webhook Security

External webhook endpoints should validate:

- Authentication
- Signature where supported
- Timestamp
- Event ID
- Payload structure
- Idempotency

Never trust incoming webhook payloads blindly.

---

# 51. Rate Limiting

Public endpoints should eventually have rate limits.

Examples:

```text
Login
Chat message
Lead creation
Webhook endpoints
```

This protects the system against abuse and accidental traffic spikes.

---

# 52. CORS

The FastAPI API should only permit approved frontend origins.

Development:

```text
http://localhost:3000
```

Production should use the actual deployed React domain.

Avoid:

```text
allow_origins=["*"]
```

for authenticated production APIs unless there is a deliberate security reason.

---

# 53. API Logging

Logs should capture:

```text
request_id
endpoint
HTTP method
status code
duration
user/service identity
error code
```

Avoid logging:

```text
passwords
JWT tokens
API keys
database credentials
unnecessary customer PII
```

---

# 54. API Observability

The system should eventually support:

```text
Logs
Metrics
Tracing
```

Important metrics include:

```text
API response time
Error rate
AI processing time
n8n workflow failures
Lead processing latency
Message processing latency
```

---

# 55. API Timeout Rules

External calls must have timeouts.

For example:

```text
FastAPI → n8n
FastAPI → external services
n8n → AI provider
```

No external network request should be allowed to hang indefinitely.

---

# 56. Retry Strategy

Retries should be used carefully.

Good retry candidates:

```text
Temporary network failure
Temporary service unavailable
Transient database connection failure
```

Bad retry candidates:

```text
Validation errors
Authentication failures
Invalid business rules
```

Use exponential backoff where appropriate.

---

# 57. API and n8n Responsibility Boundary

The following division should be maintained.

### FastAPI

Responsible for:

```text
Authentication
Authorization
Validation
Business rules
Database access
Resource ownership
API contracts
```

### n8n

Responsible for:

```text
Workflow orchestration
Integrations
AI processing
Notifications
Scheduled workflows
Google Sheets synchronization
External automation
```

### React

Responsible for:

```text
UI
User interaction
Client state
API consumption
Form validation for UX
```

React validation does not replace backend validation.

---

# 58. API and AI Responsibility Boundary

AI is responsible for:

```text
Natural language understanding
Information extraction
Intent classification
Response generation
Conversation summarization
```

AI is not responsible for:

```text
Authentication
Authorization
Database integrity
Financial authorization
Lead ownership
Final business-rule enforcement
```

---

# 59. API Contract Example

Complete customer message flow:

```text
POST /api/v1/conversations/{id}/messages
             │
             ▼
       FastAPI validates
             │
             ▼
       Save message
             │
             ▼
       Trigger n8n
             │
             ▼
       AI extraction
             │
             ▼
       Structured output
             │
             ▼
       Validate data
             │
             ▼
       Update lead
             │
             ▼
       Calculate score
             │
             ▼
       Generate response
             │
             ▼
       Save bot message
             │
             ▼
       Notify customer
             │
             ▼
       Notify sales if required
```

---

# 60. Example End-to-End Payload

Customer sends:

```text
Hi, I'm looking for a 3-bedroom apartment around Lekki.
My budget is around ₦80 million and I'd like to move in
within the next two months.
```

AI extraction:

```json
{
  "intent": "BUY",
  "property_type": "APARTMENT",
  "bedrooms": 3,
  "location": "Lekki",
  "budget_max": 80000000,
  "currency": "NGN",
  "timeline": "WITHIN_3_MONTHS",
  "confidence": 0.96
}
```

Backend validates:

```text
✓ property_type valid
✓ bedrooms valid
✓ budget valid
✓ location provided
✓ timeline valid
```

Lead becomes:

```text
Status:
QUALIFIED

Classification:
HOT

Score:
85
```

---

# 61. API Schema Management

FastAPI/Pydantic models should define request and response contracts.

Recommended structure:

```text
backend/
└── app/
    ├── api/
    │   └── routes/
    ├── schemas/
    ├── models/
    ├── services/
    ├── repositories/
    └── core/
```

Example:

```text
schemas/
├── auth.py
├── lead.py
├── conversation.py
├── message.py
├── follow_up.py
└── activity.py
```

---

# 62. Pydantic Schema Principle

Request models and database models should not automatically be treated as the same thing.

Use:

```text
API Schema
     ↓
Service
     ↓
Domain/Database Model
```

This protects the API contract from accidental database implementation changes.

---

# 63. API Documentation

FastAPI should automatically expose OpenAPI documentation.

Development endpoints:

```text
/docs
/redoc
```

These should be appropriately protected or disabled in production if required by the security posture.

The generated OpenAPI schema should remain synchronized with this specification.

---

# 64. API Testing

Every endpoint must have tests.

Minimum categories:

```text
Happy path
Validation
Authentication
Authorization
Not found
Duplicate requests
Database failure
External service failure
```

Example:

```text
POST /leads
```

Tests:

```text
✓ valid lead
✓ missing name
✓ invalid budget
✓ invalid property type
✓ unauthorized request
✓ duplicate request
```

---

# 65. Contract Testing

Frontend and backend should validate that their assumptions about the API remain synchronized.

For important endpoints:

```text
React
  ↕
API Contract
  ↕
FastAPI
```

A breaking API change should cause tests to fail before deployment.

---

# 66. Backward Compatibility

Avoid breaking existing consumers unnecessarily.

For example, changing:

```json
{
  "score": 85
}
```

to:

```json
{
  "lead_score": 85
}
```

is potentially a breaking API change.

Instead, introduce a versioned contract or migration strategy.

---

# 67. API Security Principles

The API must follow:

```text
Never trust client input.
Never expose secrets.
Validate every request.
Authorize every protected action.
Limit public endpoints.
Use HTTPS.
Use secure tokens.
Log safely.
Protect webhooks.
```

---

# 68. Environment Variables

Secrets and environment-specific configuration should use environment variables or a secure secrets manager.

Examples:

```text
DATABASE_URL
JWT_SECRET
N8N_WEBHOOK_URL
N8N_API_KEY
GOOGLE_SHEETS_CREDENTIAL
AI_PROVIDER_KEY
CORS_ORIGINS
```

Do not commit real credentials to Git.

---

# 69. API Environment Separation

The API should support:

```text
Development
Staging
Production
```

Each environment should have separate:

```text
Database
Credentials
n8n instance/workflows
AI configuration
Frontend origin
```

---

# 70. API Folder Structure

Recommended:

```text
backend/
│
├── app/
│   ├── main.py
│   │
│   ├── api/
│   │   └── routes/
│   │       ├── auth.py
│   │       ├── leads.py
│   │       ├── conversations.py
│   │       ├── messages.py
│   │       ├── follow_ups.py
│   │       └── activities.py
│   │
│   ├── schemas/
│   ├── models/
│   ├── services/
│   ├── repositories/
│   ├── database/
│   ├── middleware/
│   └── core/
│
├── tests/
│
├── alembic/
│
├── requirements.txt
└── README.md
```

The exact structure may evolve as implementation progresses.

---

# 71. Agentic Coding Rules

AI coding agents working on the API must follow these rules.

## Rule 1

Do not invent API endpoints without checking this specification.

## Rule 2

Do not change an existing endpoint contract without updating this document.

## Rule 3

Do not expose database models directly as API responses without deliberate schema design.

## Rule 4

Validate all external input.

## Rule 5

Never put secrets in source code.

## Rule 6

Do not allow React to communicate directly with PostgreSQL.

## Rule 7

Do not allow AI to bypass application validation.

## Rule 8

Do not allow n8n to bypass API business rules unless explicitly designed as an internal trusted workflow.

## Rule 9

Every new endpoint requires tests.

## Rule 10

Breaking changes require versioning or an explicit migration plan.

---

# 72. Definition of Done

The API layer is considered MVP-ready when:

- [ ] FastAPI application is running.
- [ ] API versioning is implemented.
- [ ] Authentication is implemented.
- [ ] Authorization is implemented.
- [ ] Health endpoint exists.
- [ ] Lead endpoints exist.
- [ ] Conversation endpoints exist.
- [ ] Message endpoints exist.
- [ ] Qualification endpoint exists.
- [ ] Assignment endpoint exists.
- [ ] Follow-up endpoints exist.
- [ ] Activity endpoint exists.
- [ ] n8n integration contract is implemented.
- [ ] Error format is standardized.
- [ ] Request IDs are implemented.
- [ ] Idempotency is handled where required.
- [ ] Validation is implemented.
- [ ] Pagination is implemented.
- [ ] Filtering is implemented.
- [ ] API tests exist.
- [ ] OpenAPI documentation is available.
- [ ] Secrets are externalized.
- [ ] CORS is configured securely.
- [ ] Logging is implemented safely.
- [ ] API deployment configuration exists.

---

# 73. Final API Architecture

The final responsibility model should remain:

```text
                    CUSTOMER
                       │
                       ▼
                    REACT
                       │
                       │ HTTPS / JSON
                       ▼
                  ┌───────────┐
                  │  FastAPI  │
                  └─────┬─────┘
                        │
             ┌──────────┼──────────┐
             │          │          │
             ▼          ▼          ▼
          Database    n8n       Auth
             │          │
             │          ├──── AI
             │          ├──── Google Sheets
             │          └──── Notifications
             │
             ▼
           Leads
             │
       ┌─────┼─────┐
       ▼     ▼     ▼
    Scores Assign Follow-ups
       │
       ▼
    Activities
       │
       ▼
   Sales Team
```

The key principle is:

> **React is the presentation layer, FastAPI is the application/API boundary, PostgreSQL is the system of record, n8n is the workflow orchestration layer, and AI is an intelligence component—not the source of truth.**

This separation keeps the system understandable, testable, secure, and suitable for development by multiple engineers and AI coding agents.