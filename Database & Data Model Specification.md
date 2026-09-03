# Database & Data Model Specification

## PrimeHomes Realty — Real Estate Lead Bot

**Document:** Database & Data Model Specification  
**Version:** 1.0  
**Status:** Draft  
**Product:** PrimeHomes Realty Real Estate Lead Bot  
**Primary Database:** SQL  
**Recommended Database:** PostgreSQL  
**Automation:** n8n  
**Backend:** FastAPI / Python  
**Frontend:** React  
**Secondary Operational Store:** Google Sheets

---

# 1. Purpose

This document defines the data architecture and database model for the PrimeHomes Realty Real Estate Lead Bot.

It establishes:

- What data the system stores.
- How data is structured.
- Relationships between entities.
- Data ownership.
- Data types.
- Required and optional fields.
- Constraints.
- Indexing strategy.
- Audit requirements.
- Conversation storage.
- Lead scoring storage.
- Follow-up tracking.
- User and role management.
- Integration records.
- Google Sheets synchronization.

This document is the authoritative reference for database-related implementation.

Developers and AI coding agents must use this document when creating or modifying database models.

---

# 2. Database Architecture

The primary application data store is a relational SQL database.

The recommended implementation is:

```text
PostgreSQL
```

The database acts as the:

> **System of Record**

for all critical application data.

High-level architecture:

```text
                    ┌─────────────────┐
                    │     React       │
                    └────────┬────────┘
                             │
                             ▼
                    ┌─────────────────┐
                    │    FastAPI      │
                    └────────┬────────┘
                             │
                             ▼
                    ┌─────────────────┐
                    │   PostgreSQL    │
                    │                 │
                    │ System of       │
                    │ Record          │
                    └────────┬────────┘
                             │
                             │
                    ┌────────▼────────┐
                    │      n8n        │
                    │  Orchestration  │
                    └────────┬────────┘
                             │
                  ┌──────────┼──────────┐
                  ▼          ▼          ▼
                 AI      Google Sheets Notifications
```

---

# 3. Data Ownership Principle

The most important database rule is:

> **Core business data belongs in SQL.**

The following must be persisted in SQL:

- Leads
- Customers
- Conversations
- Messages
- Lead scores
- Assignments
- Follow-ups
- Activities
- Users
- Statuses
- Important workflow events

Google Sheets is a secondary operational/reporting destination.

---

# 4. Core Data Domains

The database can be divided into the following domains:

```text
Identity
   │
   ├── Users
   └── Roles

Customer
   │
   ├── Leads
   ├── Conversations
   └── Messages

Qualification
   │
   ├── Lead Scores
   └── Qualification Results

Sales
   │
   ├── Assignments
   ├── Follow-ups
   └── Activities

Integration
   │
   ├── External IDs
   └── Synchronization Records
```

---

# 5. Entity Overview

The initial database will contain these core entities:

```text
users
roles
leads
conversations
messages
lead_scores
lead_assignments
follow_ups
activities
integration_syncs
```

Potential future entities:

```text
properties
property_matches
appointments
notifications
campaigns
tags
lead_sources
```

These are not required for the initial MVP unless the product scope expands.

---

# 6. Entity Relationship Overview

High-level relationship:

```text
                         ┌───────────┐
                         │   USERS   │
                         └─────┬─────┘
                               │
                    ┌──────────┼───────────┐
                    │          │           │
                    ▼          ▼           ▼
                 Leads     Assignments  Activities
                    │
        ┌───────────┼────────────┐
        │           │            │
        ▼           ▼            ▼
 Conversations  Lead Scores   Follow-ups
        │
        ▼
    Messages
```

---

# 7. Customer vs Lead

The system should distinguish between a **customer identity** and a **lead opportunity** where appropriate.

For the MVP, we can simplify this by keeping customer information directly on the `leads` table.

However, the architecture should allow customer identity to be extracted into a separate `customers` table later.

### MVP approach

```text
Lead
 ├── name
 ├── email
 ├── phone
 ├── requirements
 └── sales information
```

### Future CRM approach

```text
Customer
   │
   ├── Lead
   ├── Lead
   └── Lead
```

This allows the same customer to create multiple enquiries.

---

# 8. Lead Entity

The `leads` table is the central business entity.

It represents a potential sales opportunity.

## Proposed table

```text
leads
```

### Fields

| Field | Type | Required | Description |
|---|---|---:|---|
| id | UUID | Yes | Unique lead identifier |
| name | VARCHAR | No | Customer name |
| email | VARCHAR | No | Customer email |
| phone | VARCHAR | No | Customer phone |
| property_type | VARCHAR/ENUM | No | Requested property type |
| transaction_type | VARCHAR/ENUM | No | Buy, rent, sell, etc. |
| bedrooms | INTEGER | No | Number of bedrooms |
| bathrooms | INTEGER | No | Number of bathrooms |
| location | VARCHAR | No | Preferred location |
| budget_min | DECIMAL | No | Minimum budget |
| budget_max | DECIMAL | No | Maximum budget |
| currency | VARCHAR | No | Currency code |
| timeline | VARCHAR/ENUM | No | Expected transaction timeline |
| intent | VARCHAR/ENUM | No | Detected customer intent |
| status | VARCHAR/ENUM | Yes | Current lead state |
| classification | VARCHAR/ENUM | No | HOT/WARM/COLD |
| score | INTEGER | No | Current lead score |
| source | VARCHAR | No | Lead acquisition source |
| created_at | TIMESTAMP | Yes | Creation time |
| updated_at | TIMESTAMP | Yes | Last modification |
| last_contacted_at | TIMESTAMP | No | Last sales contact |
| next_follow_up_at | TIMESTAMP | No | Next scheduled follow-up |

---

# 9. Lead ID

Every lead must have a unique identifier.

Recommended:

```text
UUID
```

Example:

```text
lead_id:
550e8400-e29b-41d4-a716-446655440000
```

The ID must not contain sensitive customer information.

Do not use:

```text
lead-john-doe-08012345678
```

---

# 10. Property Type

Supported initial values:

```text
APARTMENT
HOUSE
DUPLEX
TERRACE
DETACHED_HOUSE
LAND
COMMERCIAL
OFFICE
OTHER
UNKNOWN
```

The exact implementation may use PostgreSQL enums or controlled string values.

The API should validate allowed values.

---

# 11. Transaction Type

Supported values:

```text
BUY
RENT
SELL
INQUIRE
UNKNOWN
```

Example:

```text
"I want to buy a 3-bedroom apartment."
```

becomes:

```text
transaction_type = BUY
```

---

# 12. Lead Timeline

Supported values:

```text
IMMEDIATE
WITHIN_1_MONTH
WITHIN_3_MONTHS
WITHIN_6_MONTHS
RESEARCHING
UNKNOWN
```

The original customer message should remain available through the conversation history.

The structured field is an interpretation of that message.

---

# 13. Lead Status

Initial status model:

```text
NEW
QUALIFYING
QUALIFIED
ASSIGNED
CONTACTED
ENGAGED
VIEWING_SCHEDULED
NEGOTIATING
NURTURE
CONVERTED
LOST
```

The backend must control valid state transitions.

Example:

```text
NEW
 ↓
QUALIFYING
 ↓
QUALIFIED
 ↓
ASSIGNED
 ↓
CONTACTED
 ↓
ENGAGED
```

Invalid transitions should be rejected.

---

# 14. Lead Classification

Classification represents the business priority of the lead.

Initial values:

```text
HOT
WARM
COLD
UNQUALIFIED
```

Classification should be derived from the lead score and qualification rules.

It should not be freely controlled by the frontend.

---

# 15. Lead Score

The `score` field represents the current qualification score.

Example:

```text
0 - 100
```

Possible scoring:

```text
Budget provided          +20
Contact information      +15
Specific location        +15
Property requirement     +15
Immediate timeline       +20
Clear transaction intent +10
--------------------------------
Maximum                  95
```

The exact scoring algorithm will be defined in the Qualification Technical Specification.

---

# 16. Lead Score History

The system should preserve score changes rather than only storing the current score.

Table:

```text
lead_scores
```

Fields:

| Field | Type | Description |
|---|---|---|
| id | UUID | Score record ID |
| lead_id | UUID | Associated lead |
| score | INTEGER | Calculated score |
| classification | VARCHAR | HOT/WARM/COLD |
| reason | TEXT | Explanation |
| scoring_version | VARCHAR | Version of scoring rules |
| created_at | TIMESTAMP | Calculation time |

Example:

```text
Lead:
lead_123

Score:
45 → WARM

Later:

Score:
82 → HOT
```

Both records should remain available.

---

# 17. Why Score History Matters

Score history provides:

- Auditing
- Debugging
- Analytics
- Sales intelligence
- Model evaluation
- Rule comparison

It also allows us to answer:

> "Why was this lead classified as HOT?"

---

# 18. Conversation Entity

Table:

```text
conversations
```

A conversation represents an interaction session between a customer and the system.

### Fields

| Field | Type | Description |
|---|---|---|
| id | UUID | Conversation ID |
| lead_id | UUID | Associated lead |
| channel | VARCHAR | Website, WhatsApp, etc. |
| external_conversation_id | VARCHAR | ID from external channel |
| status | VARCHAR | Active/closed |
| started_at | TIMESTAMP | Start time |
| ended_at | TIMESTAMP | End time |
| created_at | TIMESTAMP | Creation time |
| updated_at | TIMESTAMP | Last update |

---

# 19. Conversation vs Lead

These concepts must remain separate.

A lead represents:

> **A business opportunity.**

A conversation represents:

> **Communication around that opportunity.**

Therefore:

```text
Lead
  │
  ├── Conversation 1
  ├── Conversation 2
  └── Conversation 3
```

This becomes important when multiple communication channels are introduced.

---

# 20. Message Entity

Table:

```text
messages
```

Every relevant customer/bot/agent message should be persisted.

### Fields

| Field | Type | Description |
|---|---|---|
| id | UUID | Message ID |
| conversation_id | UUID | Parent conversation |
| sender_type | VARCHAR | CUSTOMER/BOT/AGENT/SYSTEM |
| sender_id | UUID | User ID where applicable |
| content | TEXT | Message content |
| external_message_id | VARCHAR | External platform ID |
| metadata | JSONB | Additional information |
| created_at | TIMESTAMP | Message time |

---

# 21. Message Sender Types

Supported values:

```text
CUSTOMER
BOT
AGENT
SYSTEM
```

Example:

```text
CUSTOMER:
"I need a 3 bedroom apartment."

BOT:
"Which location are you interested in?"

CUSTOMER:
"Lekki."

SYSTEM:
"Lead score recalculated."

AGENT:
"I'll contact the customer shortly."
```

---

# 22. AI Processing Metadata

AI-specific metadata may be stored with a message or in a separate processing table.

Potential information:

```text
model
provider
prompt_version
processing_time
confidence
structured_output
tokens_used
status
```

For example:

```json
{
  "intent": "BUY",
  "confidence": 0.94,
  "property_type": "APARTMENT"
}
```

Sensitive or unnecessary AI provider information should not be stored indefinitely without a business reason.

---

# 23. Lead Assignment

Table:

```text
lead_assignments
```

This represents the relationship between a lead and a sales representative.

### Fields

| Field | Type | Description |
|---|---|---|
| id | UUID | Assignment ID |
| lead_id | UUID | Lead |
| user_id | UUID | Sales representative |
| assigned_by | UUID | User who assigned it |
| assigned_at | TIMESTAMP | Assignment time |
| unassigned_at | TIMESTAMP | End of assignment |
| is_active | BOOLEAN | Current assignment |

This allows assignment history to be retained.

---

# 24. Why Assignment History Matters

Instead of:

```text
lead.assigned_to = john
```

and losing the previous assignment, we maintain:

```text
Lead
 ↓
Agent A
 ↓
Agent B
 ↓
Agent C
```

This provides an audit trail.

---

# 25. Follow-Up Entity

Table:

```text
follow_ups
```

Represents planned or completed sales activities.

### Fields

| Field | Type | Description |
|---|---|---|
| id | UUID | Follow-up ID |
| lead_id | UUID | Associated lead |
| assigned_to | UUID | Sales representative |
| type | VARCHAR | CALL/EMAIL/WHATSAPP/MEETING/etc. |
| scheduled_at | TIMESTAMP | Planned time |
| completed_at | TIMESTAMP | Completion time |
| status | VARCHAR | PENDING/COMPLETED/CANCELLED |
| notes | TEXT | Follow-up notes |
| created_at | TIMESTAMP | Creation time |
| updated_at | TIMESTAMP | Last modification |

---

# 26. Follow-Up Types

Initial values:

```text
CALL
EMAIL
WHATSAPP
MEETING
PROPERTY_VIEWING
OTHER
```

Future types may be added.

---

# 27. Activity Log

Table:

```text
activities
```

This is the audit trail for important lead events.

Examples:

```text
LEAD_CREATED
MESSAGE_RECEIVED
AI_PROCESSED
LEAD_QUALIFIED
SCORE_CHANGED
LEAD_ASSIGNED
STATUS_CHANGED
FOLLOW_UP_CREATED
FOLLOW_UP_COMPLETED
CUSTOMER_CONTACTED
LEAD_CONVERTED
LEAD_LOST
HUMAN_HANDOFF
```

### Fields

| Field | Type | Description |
|---|---|---|
| id | UUID | Activity ID |
| lead_id | UUID | Related lead |
| actor_type | VARCHAR | SYSTEM/AI/AGENT |
| actor_id | UUID | User if applicable |
| activity_type | VARCHAR | Event type |
| description | TEXT | Human-readable explanation |
| metadata | JSONB | Structured event information |
| created_at | TIMESTAMP | Event time |

---

# 28. Auditability

Important business actions must be traceable.

For example:

```text
Lead created
      ↓
AI extracted requirements
      ↓
Score = 62
      ↓
Assigned to Agent A
      ↓
Agent contacted customer
      ↓
Score = 84
      ↓
Status = NEGOTIATING
```

The activity log should make this history visible.

---

# 29. User Entity

Table:

```text
users
```

Internal users include:

- Administrators
- Sales managers
- Sales representatives

### Fields

| Field | Type | Description |
|---|---|---|
| id | UUID | User ID |
| name | VARCHAR | Full name |
| email | VARCHAR | Login email |
| password_hash | VARCHAR | Hashed password |
| role_id | UUID | User role |
| status | VARCHAR | ACTIVE/INACTIVE |
| created_at | TIMESTAMP | Creation time |
| updated_at | TIMESTAMP | Last update |
| last_login_at | TIMESTAMP | Last login |

Passwords must never be stored in plaintext.

---

# 30. Roles

Table:

```text
roles
```

Initial roles:

```text
ADMIN
MANAGER
SALES_AGENT
```

Future permissions can be more granular.

Example:

```text
MANAGER
 ├── view_leads
 ├── assign_leads
 ├── update_leads
 └── view_reports

SALES_AGENT
 ├── view_assigned_leads
 ├── update_leads
 └── create_followups
```

---

# 31. Integration Synchronization

Because Google Sheets is part of the system, synchronization should be tracked.

Table:

```text
integration_syncs
```

### Fields

| Field | Type | Description |
|---|---|---|
| id | UUID | Sync record |
| entity_type | VARCHAR | LEAD/ACTIVITY/etc. |
| entity_id | UUID | Local record |
| integration | VARCHAR | GOOGLE_SHEETS |
| external_id | VARCHAR | External record ID |
| status | VARCHAR | PENDING/SUCCESS/FAILED |
| attempts | INTEGER | Retry count |
| last_error | TEXT | Error information |
| synced_at | TIMESTAMP | Successful sync time |
| created_at | TIMESTAMP | Record creation |

---

# 32. Google Sheets Synchronization

The preferred direction is:

```text
SQL
 ↓
n8n
 ↓
Google Sheets
```

Not:

```text
Google Sheets
 ↓
SQL
```

for normal lead creation.

Google Sheets should primarily be treated as a projection of application data.

---

# 33. Synchronization Example

When a new lead is created:

```text
Lead Created
     ↓
SQL Database
     ↓
Event / Workflow
     ↓
n8n
     ↓
Google Sheets
```

If Google Sheets fails:

```text
SQL ✓
Sheets ✗
```

the lead remains valid.

n8n should retry synchronization.

---

# 34. JSON / Flexible Metadata

Some information will not fit neatly into relational columns.

For these cases, PostgreSQL `JSONB` fields may be used carefully.

Example:

```json
{
  "source_campaign": "facebook_leads_2026",
  "utm_source": "facebook",
  "utm_campaign": "lekki_campaign"
}
```

JSONB must not be used as an excuse to avoid proper schema design.

Frequently queried business fields should have proper database columns.

---

# 35. Database Constraints

The database should enforce important integrity rules.

Examples:

### Score

```text
score >= 0
score <= 100
```

### Bedrooms

```text
bedrooms >= 0
```

### Budget

```text
budget_min >= 0
budget_max >= 0
```

### Budget relationship

Where both exist:

```text
budget_min <= budget_max
```

### Required fields

Every lead must have:

```text
id
status
created_at
updated_at
```

---

# 36. Nullability

The system must distinguish between:

```text
NULL
```

and:

```text
UNKNOWN
```

Where appropriate.

Example:

If the customer hasn't provided a budget:

```text
budget_max = NULL
```

Do not use:

```text
budget_max = 0
```

because zero is a valid numeric value and has a different meaning.

---

# 37. Data Normalization

The database should follow relational database normalization principles where practical.

Avoid storing repeated information unnecessarily.

Bad:

```text
lead_1:
agent_name = John

lead_2:
agent_name = John
```

Better:

```text
lead_1 → user_id
lead_2 → user_id
```

The user record contains John's information.

---

# 38. Indexing Strategy

Indexes should support common queries.

Initial indexes should likely include:

```text
leads.status
leads.classification
leads.score
leads.created_at
leads.updated_at
leads.assigned_to
leads.phone
leads.email
```

Conversation:

```text
conversations.lead_id
conversations.external_conversation_id
```

Messages:

```text
messages.conversation_id
messages.created_at
```

Follow-ups:

```text
follow_ups.scheduled_at
follow_ups.status
follow_ups.assigned_to
```

The exact indexes should be validated against real query patterns.

---

# 39. Unique Constraints

Potential unique constraints:

```text
users.email
```

External identifiers may also need uniqueness within their integration.

For example:

```text
external_message_id + channel
```

This helps prevent duplicate message processing.

---

# 40. Idempotency

The database should support idempotent processing.

Example:

```text
External Message ID:
msg_123
```

If n8n receives the same webhook twice:

```text
msg_123
```

the application should recognize that the message already exists.

Result:

```text
Do not create duplicate message.
Do not create duplicate lead.
Do not send duplicate notification.
```

---

# 41. Soft Delete

Critical business records should generally not be physically deleted immediately.

For example, rather than:

```text
DELETE FROM leads
```

we may use:

```text
deleted_at
```

where appropriate.

However, not every table requires soft deletion.

Audit records should generally remain immutable.

---

# 42. Timestamps

All database timestamps should be stored consistently.

Recommended:

```text
UTC
```

Example:

```text
2026-09-03T10:30:00Z
```

The frontend can convert UTC to the user's local timezone.

---

# 43. Data Retention

The system should eventually define retention policies for:

- Customer messages
- Lead records
- Activity logs
- AI processing metadata
- Integration logs

Retention periods should be based on business, legal, privacy, and operational requirements.

This is intentionally not hard-coded in this version of the specification.

---

# 44. Sensitive Data

Potentially sensitive information includes:

- Phone numbers
- Email addresses
- Customer messages
- Internal notes
- Authentication credentials

The system must:

- Restrict access.
- Avoid exposing unnecessary data.
- Encrypt data in transit.
- Protect database credentials.
- Avoid logging sensitive information unnecessarily.

---

# 45. Data Flow

## Customer Message

```text
Customer
   ↓
React
   ↓
FastAPI
   ↓
Conversation
   ↓
Message
   ↓
n8n
   ↓
AI
   ↓
Structured Lead Data
   ↓
Validation
   ↓
Lead
   ↓
Lead Score
   ↓
Activity
```

---

# 46. Lead Creation Flow

```text
Incoming Customer Message
          ↓
Find Existing Conversation
          ↓
Conversation Exists?
       /       \
     YES        NO
      ↓          ↓
Update       Create
Conversation Conversation
      \          /
       \        /
        ▼      ▼
        Message
           ↓
        AI Process
           ↓
      Extract Fields
           ↓
        Validate
           ↓
       Create/Update
           ↓
           Lead
```

---

# 47. Lead Update Flow

If a customer sends additional information:

```text
Customer:
"My budget is 80 million."
```

The system should:

```text
Find Lead
   ↓
Extract budget
   ↓
Validate budget
   ↓
Update Lead
   ↓
Recalculate Score
   ↓
Store Score History
   ↓
Create Activity
```

---

# 48. Conversation Context

AI processing may need information from previous messages.

The application should provide controlled context such as:

```text
Lead information
+
Recent messages
+
Relevant conversation summary
```

Avoid sending unnecessary historical data to the AI provider.

---

# 49. AI Data Separation

AI-generated information should be distinguishable from customer-provided information.

For example:

```text
Customer-provided:
location = Lekki

AI-inferred:
property_type = APARTMENT
```

The exact provenance mechanism may use metadata or an AI extraction table in a future iteration.

---

# 50. Provenance

For important extracted fields, the architecture should eventually support identifying their source.

Example:

```text
budget = ₦80,000,000

source:
message_id = msg_123
confidence = 0.98
```

This is useful for debugging and AI evaluation.

---

# 51. Recommended Future AI Extraction Table

If AI complexity increases, introduce:

```text
ai_extractions
```

Potential fields:

```text
id
message_id
lead_id
model
model_version
prompt_version
extracted_data
confidence
status
created_at
```

This is optional for the MVP but recommended if detailed AI observability is required.

---

# 52. Initial Entity Relationship Model

Conceptually:

```text
┌─────────────┐
│    USERS    │
└──────┬──────┘
       │
       │ handles
       ▼
┌─────────────┐
│    LEADS    │
└──────┬──────┘
       │
       ├───────────────┐
       │               │
       ▼               ▼
┌─────────────┐   ┌─────────────┐
│CONVERSATIONS│   │ LEAD_SCORES │
└──────┬──────┘   └─────────────┘
       │
       ▼
┌─────────────┐
│  MESSAGES   │
└─────────────┘

LEADS
 │
 ├── LEAD_ASSIGNMENTS
 │
 ├── FOLLOW_UPS
 │
 ├── ACTIVITIES
 │
 └── INTEGRATION_SYNCS
```

---

# 53. Example Lead Record

Conceptual representation:

```json
{
  "id": "lead_123",
  "name": "John Doe",
  "email": "john@example.com",
  "phone": "+2348012345678",
  "property_type": "APARTMENT",
  "transaction_type": "BUY",
  "bedrooms": 3,
  "location": "Lekki",
  "budget_min": null,
  "budget_max": 80000000,
  "currency": "NGN",
  "timeline": "WITHIN_3_MONTHS",
  "status": "QUALIFIED",
  "classification": "HOT",
  "score": 85
}
```

---

# 54. Example Conversation

```json
{
  "id": "conv_123",
  "lead_id": "lead_123",
  "channel": "WEB",
  "status": "ACTIVE"
}
```

Messages:

```json
[
  {
    "sender_type": "CUSTOMER",
    "content": "I need a 3 bedroom apartment."
  },
  {
    "sender_type": "BOT",
    "content": "Which location are you interested in?"
  },
  {
    "sender_type": "CUSTOMER",
    "content": "Lekki."
  },
  {
    "sender_type": "BOT",
    "content": "What budget are you considering?"
  },
  {
    "sender_type": "CUSTOMER",
    "content": "Around 80 million."
  }
]
```

---

# 55. Database Migration Strategy

Database schema changes must use migrations.

Recommended tooling:

```text
Alembic
```

with SQLAlchemy/SQLModel depending on the backend implementation.

Example:

```text
Migration 001
Create users

Migration 002
Create leads

Migration 003
Create conversations

Migration 004
Create messages

Migration 005
Create lead_scores
```

Never manually modify production database schemas without a tracked migration.

---

# 56. Seed Data

Development environments should have seed data where useful.

Example:

```text
Admin User
Sales Manager
Sales Agent
Sample Leads
Sample Conversations
Sample Messages
```

Seed data must clearly be development/test data.

---

# 57. Repository Ownership

Database-related code should live primarily under:

```text
backend/
└── app/
    ├── models/
    ├── schemas/
    ├── repositories/
    ├── services/
    └── database/
```

Migrations:

```text
backend/
└── alembic/
```

or:

```text
database/
└── migrations/
```

The final location should be standardized during backend implementation.

---

# 58. Database Access Pattern

The preferred application flow is:

```text
API Route
   ↓
Service
   ↓
Repository
   ↓
Database
```

Avoid putting complex database operations directly inside API route handlers.

Example:

```text
POST /leads
      ↓
LeadService
      ↓
LeadRepository
      ↓
PostgreSQL
```

This separation makes the backend easier to test and maintain.

---

# 59. Transaction Boundaries

Operations that must succeed together should use database transactions.

Example:

```text
Create Lead
+
Create Initial Activity
```

should generally occur within a controlled transaction.

However:

```text
Save Lead
+
Send Notification
```

should not necessarily be one database transaction because the notification service is external.

Instead:

```text
Database Commit
       ↓
Notification Workflow
```

---

# 60. Data Consistency Rules

The system must maintain consistency between:

```text
Lead
Conversation
Messages
Score
Assignment
Activities
Follow-ups
```

For example:

A lead should not reference a non-existent user assignment.

A message should not reference a non-existent conversation.

A score record should not reference a non-existent lead.

These relationships should be enforced with foreign keys.

---

# 61. Cascading Rules

Cascading deletes should be used carefully.

For example:

```text
Lead
 ↓
Messages
```

should not automatically result in irreversible deletion of business history.

The preferred approach is to preserve important historical data unless a specific deletion policy has been established.

---

# 62. Query Patterns

The database should efficiently support queries such as:

### Get all hot leads

```text
classification = HOT
```

### Get new leads

```text
status = NEW
```

### Get leads assigned to a salesperson

```text
assigned_to = user_id
```

### Get today's follow-ups

```text
scheduled_at = today
```

### Get recent conversations

```text
updated_at DESC
```

### Get lead history

```text
activities
WHERE lead_id = ?
ORDER BY created_at DESC
```

---

# 63. Dashboard Queries

The sales dashboard will require aggregate queries such as:

```text
Total Leads
Hot Leads
Warm Leads
Cold Leads
New Leads
Converted Leads
Lost Leads
Leads by Agent
Leads by Location
Leads by Property Type
Leads by Source
Average Lead Score
Conversion Rate
```

Indexes and query design should account for these use cases.

---

# 64. Database Performance Principles

The MVP database should prioritize correctness and maintainability.

Avoid premature optimization.

However:

- Add indexes based on real query patterns.
- Avoid unnecessary N+1 queries.
- Paginate large datasets.
- Avoid returning entire message histories unnecessarily.
- Select only required columns for expensive queries.
- Use database transactions appropriately.

---

# 65. Pagination

Lead and message endpoints should support pagination.

Example:

```text
GET /api/v1/leads?page=1&limit=20
```

or cursor-based pagination when the system grows.

The exact API pagination contract will be defined separately.

---

# 66. Filtering

The backend should eventually support filters such as:

```text
status
classification
property_type
transaction_type
location
assigned_agent
created_at
score
```

Filtering must happen at the database/query layer rather than retrieving every lead and filtering in React.

---

# 67. Sorting

Common sorting:

```text
Newest
Oldest
Highest Score
Lowest Score
Recently Updated
Next Follow-up
```

The API should expose controlled sort fields.

The frontend must not construct arbitrary SQL-like expressions.

---

# 68. Security Rules

Database credentials must never be exposed to React.

The architecture must remain:

```text
React
  ↓
FastAPI
  ↓
Database
```

Not:

```text
React
  ↓
Database
```

Database credentials belong only in secure backend/server environments.

---

# 69. Backup Strategy

Production database backups should eventually include:

- Automated backups
- Point-in-time recovery where supported
- Backup verification
- Recovery testing
- Retention policy

A backup that has never been tested should not be considered a reliable recovery strategy.

---

# 70. Disaster Recovery

The system should eventually define:

### RPO

**Recovery Point Objective**

How much data can potentially be lost?

### RTO

**Recovery Time Objective**

How quickly should the service be restored?

These values will be established based on the business requirements.

---

# 71. Database Environment Separation

At minimum:

```text
Development
Staging
Production
```

Each environment should have its own database.

Never use the production database for local development.

---

# 72. Development Database

Developers should be able to initialize the database with:

```text
Migration
+
Seed
```

Example conceptual command:

```bash
alembic upgrade head
```

followed by a seed process where required.

---

# 73. Database Versioning

Database schema changes must be version controlled.

Example:

```text
Git
 │
 ├── Application Code
 └── Database Migrations
```

A code change requiring a schema change must include the corresponding migration.

---

# 74. Agentic Development Rules

AI coding agents modifying database code must follow these rules.

## Rule 1

Never modify the production database directly.

## Rule 2

Every schema change requires a migration.

## Rule 3

Do not rename or remove a field without checking API, frontend, n8n, tests, and existing data dependencies.

## Rule 4

Do not change enum values without checking all consumers.

## Rule 5

Do not create duplicate representations of existing entities.

## Rule 6

Do not store frequently queried structured data inside JSONB when a proper relational field is appropriate.

## Rule 7

Do not expose database credentials.

## Rule 8

Add/update tests when changing database behaviour.

## Rule 9

Consider backward compatibility for schema changes.

## Rule 10

Document significant database architecture changes using an ADR.

---

# 75. MVP Database

The minimum viable database should contain:

```text
users
roles
leads
conversations
messages
lead_scores
lead_assignments
follow_ups
activities
integration_syncs
```

This is sufficient to support the initial business workflow.

---

# 76. Future Database Expansion

As the product grows, additional entities may include:

```text
customers
properties
property_images
property_locations
property_matches
appointments
notifications
notification_deliveries
campaigns
lead_sources
tags
teams
sales_pipelines
ai_extractions
ai_evaluations
```

These should only be introduced when required by actual product functionality.

---

# 77. Database Design Summary

The fundamental model is:

```text
                       USER
                        │
                        │
                        ▼
                       LEAD
                 ┌──────┼──────┐
                 │      │      │
                 ▼      ▼      ▼
          CONVERSATION SCORE ASSIGNMENT
                 │
                 ▼
              MESSAGE
                 
                 LEAD
                  │
          ┌───────┼────────┐
          ▼       ▼        ▼
      FOLLOW-UP ACTIVITY  SYNC
```

The SQL database is the authoritative source of truth.

n8n orchestrates workflows.

AI interprets natural language.

React presents information.

FastAPI controls access and business operations.

Google Sheets receives selected operational data.

---

# 78. Definition of Done

The database layer is considered ready for MVP implementation when:

- [ ] PostgreSQL environment is configured.
- [ ] Database schema is version controlled.
- [ ] Migrations are implemented.
- [ ] Users table exists.
- [ ] Roles table exists.
- [ ] Leads table exists.
- [ ] Conversations table exists.
- [ ] Messages table exists.
- [ ] Lead scores table exists.
- [ ] Lead assignments table exists.
- [ ] Follow-ups table exists.
- [ ] Activities table exists.
- [ ] Integration synchronization table exists.
- [ ] Foreign keys are implemented.
- [ ] Required constraints are implemented.
- [ ] Appropriate indexes exist.
- [ ] Seed data exists for development.
- [ ] Database connection is secured.
- [ ] Tests exist for important database operations.
- [ ] Migration rollback strategy is understood.
- [ ] Backup strategy is documented for production.

---

# 79. Final Database Principle

The database should be designed around the **business domain**, not around whichever technology happens to process the data.

The central business object is:

```text
LEAD
```

Around the lead we maintain:

```text
Customer Information
       +
Property Requirements
       +
Conversation
       +
Messages
       +
Qualification
       +
Score
       +
Assignment
       +
Follow-up
       +
Activity History
```

This gives PrimeHomes Realty a persistent representation of the entire customer journey:

```text
Customer Enquiry
       ↓
Conversation
       ↓
Lead
       ↓
Qualification
       ↓
Sales Assignment
       ↓
Follow-up
       ↓
Engagement
       ↓
Conversion / Lost
```

The database therefore becomes the durable business memory of the Real Estate Lead Bot.