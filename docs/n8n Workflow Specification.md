# n8n Workflow Specification

## PrimeHomes Realty — Real Estate Lead Bot

**Document:** n8n Workflow Specification  
**Version:** 1.0  
**Status:** Draft  
**Automation Platform:** n8n  
**Backend:** FastAPI / Python  
**Database:** PostgreSQL  
**Frontend:** React  
**AI:** LLM-based processing  
**Secondary Data Destination:** Google Sheets

---

# 1. Purpose

This document defines the automation workflows for the PrimeHomes Realty Real Estate Lead Bot.

n8n is responsible for coordinating processes that involve multiple systems, including:

- Receiving application events.
- Processing customer messages.
- Calling AI services.
- Extracting lead information.
- Validating AI output.
- Triggering lead qualification.
- Updating the database through approved APIs.
- Sending notifications.
- Synchronizing selected data with Google Sheets.
- Scheduling follow-ups.
- Handling retries and failures.
- Recording workflow execution results.

The goal is to make the automation layer predictable, observable, maintainable, and safe for both human developers and AI coding agents.

---

# 2. Core Principle

The system follows this rule:

> **n8n orchestrates workflows; FastAPI owns application rules and controlled data access.**

Therefore:

```text
React
   ↓
FastAPI
   ↓
n8n
   ↓
AI / Integrations
   ↓
FastAPI
   ↓
PostgreSQL
```

n8n should not become a replacement for the backend.

---

# 3. n8n Responsibilities

n8n is responsible for:

```text
Workflow orchestration
AI orchestration
External integrations
Notifications
Scheduled tasks
Google Sheets synchronization
Retry handling
Conditional routing
Event-driven automation
```

---

# 4. n8n Non-Responsibilities

n8n should not independently own:

```text
Authentication
Authorization
Core business rules
Database schema ownership
Primary customer data storage
Complex domain logic
Frontend state
```

The database remains the system of record.

---

# 5. High-Level Workflow Architecture

```text
                    CUSTOMER
                       │
                       ▼
                    REACT
                       │
                       ▼
                   FASTAPI
                       │
                       ▼
                      n8n
                       │
          ┌────────────┼─────────────┐
          │            │             │
          ▼            ▼             ▼
         AI         Database      Notifications
          │            │
          ▼            ▼
      Extraction      Lead
          │           Data
          ▼
    Qualification
          │
     ┌────┴─────┐
     ▼          ▼
    HOT       NORMAL
     │          │
     ▼          ▼
 Sales Alert  Follow-up
```

---

# 6. Workflow Naming Convention

Every workflow should use a consistent name.

Format:

```text
PRH-[DOMAIN]-[ACTION]
```

Examples:

```text
PRH-LEAD-PROCESS-MESSAGE
PRH-LEAD-QUALIFY
PRH-LEAD-NOTIFY-SALES
PRH-SHEET-SYNC-LEAD
PRH-FOLLOWUP-REMINDER
PRH-ERROR-HANDLER
```

PRH stands for:

```text
PrimeHomes Realty
```

---

# 7. Workflow Categories

Initial workflow groups:

```text
01. Message Processing
02. Lead Processing
03. AI Processing
04. Lead Qualification
05. Sales Notification
06. Follow-Up Automation
07. Google Sheets Synchronization
08. Error Handling
09. Scheduled Maintenance
10. Analytics/Reporting
```

---

# 8. Workflow 01 — Message Processing

## Workflow

```text
PRH-LEAD-PROCESS-MESSAGE
```

### Purpose

Process a new customer message and determine what should happen next.

### Trigger

FastAPI sends a message event to n8n.

Example event:

```json
{
  "event": "MESSAGE_RECEIVED",
  "message_id": "message-uuid",
  "conversation_id": "conversation-uuid",
  "lead_id": "lead-uuid",
  "timestamp": "2026-09-03T10:30:00Z"
}
```

---

# 9. Message Processing Flow

```text
Webhook
   ↓
Validate Event
   ↓
Check Idempotency
   ↓
Fetch Conversation
   ↓
Fetch Lead
   ↓
Fetch Recent Messages
   ↓
Prepare AI Context
   ↓
AI Extraction
   ↓
Validate AI Output
   ↓
Update Lead
   ↓
Qualify Lead
   ↓
Generate Customer Response
   ↓
Save Bot Response
   ↓
Determine Notification
   ↓
Send Notification
   ↓
Record Activity
```

---

# 10. Node-Level Design

The workflow should conceptually contain:

```text
1. Webhook Trigger
2. Validate Event
3. Idempotency Check
4. Get Message
5. Get Conversation
6. Get Lead
7. Get Conversation History
8. Build AI Prompt
9. AI Extraction
10. Parse JSON
11. Validate Extraction
12. Update Lead
13. Qualify Lead
14. Generate Response
15. Save Response
16. Check Lead Classification
17. Notify Sales
18. Record Activity
19. Return Result
```

---

# 11. Webhook Trigger

The webhook receives the event from FastAPI.

Expected method:

```http
POST
```

Expected content type:

```text
application/json
```

Payload:

```json
{
  "event": "MESSAGE_RECEIVED",
  "message_id": "uuid",
  "conversation_id": "uuid",
  "lead_id": "uuid",
  "timestamp": "2026-09-03T10:30:00Z"
}
```

---

# 12. Webhook Validation

The workflow must verify:

```text
event exists
message_id exists
conversation_id exists
lead_id exists
timestamp exists
```

Invalid payloads should terminate safely.

Example error:

```json
{
  "code": "INVALID_EVENT",
  "message": "Required event fields are missing."
}
```

---

# 13. Idempotency

n8n workflows may receive the same event more than once.

Therefore:

```text
Event
 ↓
Check message_id/event_id
 ↓
Already processed?
 ├── YES → Stop
 └── NO  → Continue
```

The system must avoid:

- Duplicate lead creation.
- Duplicate messages.
- Duplicate notifications.
- Duplicate activities.
- Duplicate Google Sheets rows.

---

# 14. Fetch Customer Context

The workflow should retrieve:

```text
Lead
Conversation
Recent messages
Existing extracted information
Current lead score
Current lead status
Assigned sales agent
```

Do not send unnecessary information to the AI model.

---

# 15. Conversation Context Window

The AI does not need the entire conversation indefinitely.

Preferred approach:

```text
Latest customer message
+
Relevant previous messages
+
Current structured lead data
+
Missing fields
```

This reduces:

- Token usage.
- Latency.
- Cost.
- Noise.

---

# 16. AI Extraction Workflow

The AI should extract structured information from natural language.

Example customer message:

```text
I need a 3 bedroom apartment in Lekki.
My budget is around 80 million and I want to buy within two months.
```

Expected result:

```json
{
  "transaction_type": "BUY",
  "property_type": "APARTMENT",
  "bedrooms": 3,
  "location": "Lekki",
  "budget_min": null,
  "budget_max": 80000000,
  "currency": "NGN",
  "timeline": "WITHIN_3_MONTHS",
  "confidence": 0.96
}
```

---

# 17. AI Extraction Rules

The AI should:

- Extract only information supported by the conversation.
- Avoid inventing missing information.
- Return `null` when information is unavailable.
- Preserve existing structured data unless the customer clearly changes it.
- Normalize values to the application's allowed enums.
- Return confidence where possible.

The AI must not fabricate:

```text
Budget
Phone number
Email
Location
Property availability
Property prices
Customer identity
```

---

# 18. AI Output Validation

AI output must be validated before being sent to FastAPI.

Validation should check:

```text
property_type
transaction_type
bedrooms
location
budget
currency
timeline
confidence
```

Example invalid AI response:

```json
{
  "bedrooms": "three"
}
```

Expected normalized value:

```json
{
  "bedrooms": 3
}
```

If normalization is unsafe, the value should be rejected rather than guessed.

---

# 19. Confidence Handling

Example:

```text
confidence >= 0.85
```

The system may accept the extraction automatically.

```text
0.60 - 0.84
```

The system may use the information but consider clarification.

```text
< 0.60
```

The system should preferably ask the customer for clarification.

These thresholds are configurable and should be tested using real conversation data.

---

# 20. Missing Information Detection

After extraction, the workflow should identify missing qualification information.

Example:

```json
{
  "property_type": "APARTMENT",
  "location": "Lekki",
  "bedrooms": 3,
  "budget_max": null,
  "transaction_type": "BUY",
  "timeline": null
}
```

Missing:

```text
budget
timeline
```

The bot can ask:

> What budget range are you working with, and when are you hoping to purchase?

---

# 21. Question Priority

The bot should not ask for every missing field at once.

Recommended priority:

```text
1. Transaction type
2. Property type
3. Location
4. Budget
5. Bedrooms
6. Timeline
7. Contact details
```

The actual priority may depend on the conversation context.

---

# 22. Lead Update

After successful extraction:

```text
AI
 ↓
Validated JSON
 ↓
FastAPI
 ↓
PATCH /api/v1/leads/{lead_id}
```

Example:

```json
{
  "property_type": "APARTMENT",
  "bedrooms": 3,
  "location": "Lekki",
  "budget_max": 80000000,
  "transaction_type": "BUY",
  "timeline": "WITHIN_3_MONTHS"
}
```

---

# 23. Lead Qualification Workflow

## Workflow

```text
PRH-LEAD-QUALIFY
```

### Purpose

Calculate the lead's score and classification.

---

# 24. Qualification Flow

```text
Trigger
   ↓
Get Lead
   ↓
Check Required Data
   ↓
Calculate Score
   ↓
Determine Classification
   ↓
Update Lead
   ↓
Save Score History
   ↓
Create Activity
   ↓
Route Next Action
```

---

# 25. Lead Score

The lead score should be represented as:

```text
0–100
```

Possible signals:

```text
Budget provided
Location provided
Property type provided
Bedrooms provided
Transaction type provided
Timeline provided
Contact information provided
Customer engagement
Explicit buying/renting intent
Urgency
```

The exact scoring formula should live in one defined service/rule set.

It should not be independently recreated inside multiple n8n workflows.

---

# 26. Lead Classification

Initial classifications:

```text
HOT
WARM
COLD
UNQUALIFIED
```

Example:

```text
80–100 → HOT
60–79  → WARM
30–59  → COLD
0–29   → UNQUALIFIED
```

These thresholds are configurable.

---

# 27. Hot Lead Routing

If:

```text
classification == HOT
```

then:

```text
Update Lead
     ↓
Notify Sales Team
     ↓
Create Follow-Up
     ↓
Record Activity
```

---

# 28. Warm Lead Routing

If:

```text
classification == WARM
```

then:

```text
Update Lead
     ↓
Assign Sales Agent if appropriate
     ↓
Create standard follow-up
     ↓
Record Activity
```

---

# 29. Cold Lead Routing

If:

```text
classification == COLD
```

then:

```text
Update Lead
     ↓
Nurture
     ↓
Scheduled follow-up
```

No urgent sales notification is required unless configured otherwise.

---

# 30. Unqualified Lead

If:

```text
classification == UNQUALIFIED
```

the system should continue collecting information where appropriate.

It should not automatically discard the lead.

---

# 31. Customer Response Generation

AI may generate the customer-facing response.

The response should:

- Be concise.
- Be professional.
- Be helpful.
- Reflect known requirements.
- Avoid inventing property availability.
- Avoid inventing prices.
- Ask only useful follow-up questions.

Example:

```text
Thanks! I understand you're looking for a 3-bedroom apartment
in Lekki with a budget around ₦80 million.

To help us narrow down the options, when are you looking to
complete the purchase?
```

---

# 32. Property Availability Rule

The AI must never claim that a property is available unless the system has verified availability.

Bad:

```text
We have three available 3-bedroom apartments in Lekki.
```

unless verified by the property database.

Good:

```text
Thanks. I have your requirements and can help narrow down
suitable options.
```

---

# 33. Sales Notification Workflow

## Workflow

```text
PRH-LEAD-NOTIFY-SALES
```

Trigger:

```text
HOT lead
```

Example notification:

```text
🔥 HOT LEAD

Name: John Doe
Property: 3-bedroom apartment
Location: Lekki
Budget: ₦80M
Timeline: Within 3 months
Score: 85

Action: Contact customer promptly.
```

---

# 34. Notification Channels

Initial notification options:

```text
Email
Slack
Telegram
WhatsApp
```

The exact channel depends on the available integrations.

The notification system should be designed so channels can be added without changing the qualification logic.

---

# 35. Notification Failure

If notification fails:

```text
Notification
     ↓
Failure
     ↓
Retry
     ↓
Still failing?
     ↓
Record failure
     ↓
Fallback notification
```

A notification failure should not corrupt the lead.

---

# 36. Follow-Up Workflow

## Workflow

```text
PRH-FOLLOWUP-REMINDER
```

This workflow runs on a schedule.

Example:

```text
Every 15 minutes
```

The workflow searches for pending follow-ups that are due.

---

# 37. Follow-Up Flow

```text
Schedule Trigger
      ↓
Get Due Follow-Ups
      ↓
For Each Follow-Up
      ↓
Check Lead Status
      ↓
Check Assigned Agent
      ↓
Send Reminder
      ↓
Update Follow-Up
      ↓
Create Activity
```

---

# 38. Follow-Up Rules

The system should avoid reminders for:

```text
Converted leads
Lost leads
Cancelled follow-ups
Completed follow-ups
```

Unless explicitly configured.

---

# 39. Escalation

If a hot lead remains untouched:

```text
HOT
 ↓
Assigned
 ↓
No contact
 ↓
Threshold exceeded
 ↓
Escalate
```

Example:

```text
Sales Agent
    ↓
Sales Manager
```

The escalation period should be configurable.

---

# 40. Google Sheets Synchronization

Google Sheets is a secondary operational/reporting destination.

It is **not the primary database**.

Architecture:

```text
PostgreSQL
    │
    ▼
FastAPI
    │
    ▼
n8n
    │
    ▼
Google Sheets
```

---

# 41. Sheet Sync Workflow

## Workflow

```text
PRH-SHEET-SYNC-LEAD
```

Trigger:

```text
Lead created
Lead updated
Lead qualified
Lead assigned
```

The workflow updates the appropriate spreadsheet record.

---

# 42. Google Sheets Fields

Recommended operational columns:

```text
Lead ID
Name
Email
Phone
Property Type
Bedrooms
Location
Budget
Transaction Type
Timeline
Score
Classification
Status
Assigned Agent
Source
Created At
Updated At
```

---

# 43. Sheet as Projection

The rule is:

```text
PostgreSQL = Source of Truth
Google Sheets = Operational Projection
```

If the values disagree:

```text
PostgreSQL wins.
```

The system should never use a manually modified spreadsheet row as authoritative customer data without an explicitly designed import workflow.

---

# 44. Sheet Sync Idempotency

Every sheet record should have a stable:

```text
lead_id
```

The workflow should search for the lead ID before creating a row.

Conceptually:

```text
Lead ID exists?
   ├── YES → Update row
   └── NO  → Create row
```

This prevents duplicate rows.

---

# 45. Error Handling Workflow

## Workflow

```text
PRH-ERROR-HANDLER
```

The error handler should capture:

```text
Workflow name
Execution ID
Node name
Error message
Timestamp
Request ID
Lead ID
Message ID
```

Where available.

---

# 46. Error Categories

Errors should be classified.

```text
VALIDATION_ERROR
AI_ERROR
DATABASE_ERROR
NETWORK_ERROR
AUTH_ERROR
RATE_LIMIT_ERROR
INTEGRATION_ERROR
UNKNOWN_ERROR
```

---

# 47. Retry Policy

Retry only transient failures.

Example:

```text
Network failure
     ↓
Retry 1
     ↓
Retry 2
     ↓
Retry 3
     ↓
Failure queue
```

Do not retry invalid input indefinitely.

---

# 48. AI Failure Handling

If AI processing fails:

```text
Customer Message
      ↓
AI Failure
      ↓
Record Error
      ↓
Retry
      ↓
Still failing?
      ↓
Fallback Response
```

Fallback response example:

```text
Thanks for your message. We're having a brief issue processing
your request. Your enquiry has been received and a member of
our team will follow up with you.
```

The system should still preserve the customer's message.

---

# 49. Database Failure Handling

If PostgreSQL is unavailable:

```text
Workflow
   ↓
Database Error
   ↓
Retry
   ↓
Failure
   ↓
Log Execution
   ↓
Alert Operations
```

The workflow must not claim successful processing when the database update failed.

---

# 50. Workflow Execution States

Where useful, workflows should record:

```text
RECEIVED
PROCESSING
COMPLETED
FAILED
RETRYING
```

---

# 51. Workflow Timeouts

Every external operation should have a reasonable timeout.

Examples:

```text
FastAPI request
AI request
Google Sheets request
Notification request
```

No node should wait indefinitely.

---

# 52. Secrets Management

Credentials must be stored using:

```text
n8n Credentials
Environment Variables
Secret Manager
```

Never store credentials directly inside workflow JSON.

Never commit:

```text
API keys
Passwords
JWT secrets
OAuth tokens
Database credentials
```

to Git.

---

# 53. AI Prompt Management

AI prompts should be versioned.

Example:

```text
lead-extraction-v1
lead-response-v1
lead-summary-v1
```

A prompt change that affects structured output should be treated as a contract change.

---

# 54. Structured AI Output

AI extraction should always prefer structured output.

Example:

```json
{
  "transaction_type": "BUY",
  "property_type": "APARTMENT",
  "bedrooms": 3,
  "location": "Lekki",
  "budget_max": 80000000,
  "currency": "NGN",
  "timeline": "WITHIN_3_MONTHS"
}
```

Avoid depending on free-form AI text for database updates.

---

# 55. AI Prompt Principle

Prompts should instruct the model:

```text
Extract only information present in the conversation.
Do not invent missing values.
Use null for unknown values.
Follow the allowed enum values.
Return valid JSON.
```

---

# 56. Workflow Data Minimization

Only send required information between systems.

For example, an AI extraction workflow does not necessarily need:

```text
Internal user permissions
Database credentials
Full sales team information
Unrelated leads
```

This reduces security and privacy risks.

---

# 57. Customer Data Protection

Customer information may include:

```text
Name
Email
Phone
Property preferences
Budget
Conversation history
```

n8n workflows must only expose this information to systems and personnel that require it.

---

# 58. Workflow Logging

Useful execution metadata:

```text
workflow_id
execution_id
request_id
lead_id
message_id
started_at
completed_at
status
error
```

Avoid logging sensitive content unnecessarily.

---

# 59. Workflow Observability

Monitor:

```text
Workflow success rate
Workflow failure rate
Average processing time
AI latency
AI failure rate
Notification failures
Google Sheets failures
Retry count
Unprocessed messages
```

---

# 60. Workflow Performance

The workflow should avoid unnecessary calls.

Bad:

```text
Get Lead
Get Lead
Get Lead
Get Lead
```

Good:

```text
Get Lead once
     ↓
Reuse data
```

Similarly, avoid repeatedly sending the same conversation history to multiple AI calls when one structured result can be reused.

---

# 61. Token Optimization

The AI workflow should minimize unnecessary token consumption.

Use:

```text
Relevant conversation history
Structured lead state
Current customer message
Required instructions
```

Avoid:

```text
Entire database
Entire conversation history
Unrelated workflow data
Repeated system instructions
```

---

# 62. Cost Optimization

AI calls should only happen when required.

For example:

```text
Customer message
       ↓
Is this meaningful?
   ├── NO → Basic response
   └── YES → AI extraction
```

Avoid calling an LLM for:

```text
"Thanks"
"Okay"
"Good morning"
```

unless conversational intelligence is actually required.

---

# 63. Workflow Modularity

Do not build one giant n8n workflow containing everything.

Prefer:

```text
Message Processing
       │
       ├── AI Extraction
       │
       ├── Qualification
       │
       ├── Response
       │
       └── Notification
```

Each major workflow should have a clearly defined purpose.

---

# 64. Workflow-to-Workflow Communication

Where appropriate, workflows may trigger other workflows.

Example:

```text
MESSAGE PROCESSING
       ↓
LEAD QUALIFICATION
       ↓
SALES NOTIFICATION
```

The input/output contract between workflows should be explicit.

---

# 65. Workflow Event Contract

Example:

```json
{
  "event": "LEAD_QUALIFIED",
  "lead_id": "uuid",
  "score": 85,
  "classification": "HOT",
  "timestamp": "2026-09-03T10:40:00Z"
}
```

Downstream workflows should not depend on undocumented fields.

---

# 66. Event Types

Initial events:

```text
MESSAGE_RECEIVED
MESSAGE_PROCESSED
LEAD_CREATED
LEAD_UPDATED
LEAD_QUALIFIED
LEAD_ASSIGNED
FOLLOWUP_DUE
FOLLOWUP_COMPLETED
NOTIFICATION_FAILED
```

Future events may include:

```text
PROPERTY_MATCHED
VIEWING_SCHEDULED
LEAD_CONVERTED
LEAD_LOST
```

---

# 67. Lead Processing State Machine

Conceptually:

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
 ↓
VIEWING_SCHEDULED
 ↓
NEGOTIATING
 ↓
CONVERTED
```

Alternative path:

```text
Any Active State
      ↓
    NURTURE
      ↓
Re-engagement
```

Failure path:

```text
Any State
    ↓
   LOST
```

n8n should respect backend-controlled state transitions.

---

# 68. Scheduled Workflows

Scheduled workflows may include:

```text
Follow-up reminders
Stale lead detection
Lead escalation
Google Sheets synchronization
Data consistency checks
Daily reporting
Failed workflow retry
```

---

# 69. Stale Lead Workflow

Example:

```text
PRH-LEAD-DETECT-STALE
```

Purpose:

Find leads that have not received appropriate follow-up.

Flow:

```text
Schedule
  ↓
Find stale leads
  ↓
Check status
  ↓
Check classification
  ↓
Create follow-up
  ↓
Notify responsible person
  ↓
Record activity
```

---

# 70. Daily Reporting Workflow

Future workflow:

```text
PRH-REPORT-DAILY
```

Possible metrics:

```text
New leads
Qualified leads
Hot leads
Warm leads
Cold leads
Converted leads
Lost leads
Average lead score
Average response time
Uncontacted hot leads
```

---

# 71. Google Sheets Failure Strategy

If Google Sheets fails:

```text
PostgreSQL
    ↓
Still successful
    ↓
Google Sheets sync fails
    ↓
Record integration failure
    ↓
Retry later
```

A Google Sheets failure must not cause the primary lead transaction to be rolled back.

---

# 72. External Integration Principle

External services are secondary dependencies.

For example:

```text
Google Sheets unavailable
```

should not mean:

```text
Lead creation failed
```

if the lead was successfully stored in PostgreSQL.

---

# 73. Transaction Boundary

The primary transaction should be:

```text
FastAPI
   ↓
Validate
   ↓
PostgreSQL
   ↓
Commit
```

After successful persistence:

```text
n8n
   ↓
External integrations
```

This prevents external integration failures from corrupting core business data.

---

# 74. Human Handoff

The bot should know when to hand the conversation to a human.

Examples:

```text
Customer explicitly requests an agent
Complex negotiation
Complaint
Unusual request
AI confidence too low
High-value customer
Repeated misunderstanding
```

Workflow:

```text
AI
 ↓
Human required?
 ├── NO → Continue bot
 └── YES
      ↓
Assign/Notify Sales
      ↓
Mark conversation for handoff
```

---

# 75. Human Handoff State

Possible conversation states:

```text
ACTIVE_BOT
WAITING_CUSTOMER
WAITING_SALES
HUMAN_ASSIGNED
CLOSED
```

---

# 76. Avoid Automation Loops

The workflow must prevent:

```text
Bot message
 ↓
Message event
 ↓
Bot processes own message
 ↓
Bot generates message
 ↓
Message event
 ↓
Infinite loop
```

Use sender metadata:

```text
CUSTOMER
BOT
SALES_AGENT
SYSTEM
```

Only appropriate message types should trigger customer-message processing.

---

# 77. Workflow Security

Every internal webhook should use authentication.

Possible mechanisms:

```text
API key
Bearer token
HMAC signature
IP restrictions
Private networking
```

The exact mechanism should be selected during deployment.

---

# 78. n8n Production Rules

Production workflows should:

- Have descriptive names.
- Use versioned prompts.
- Use credentials securely.
- Have explicit error handling.
- Avoid hard-coded production URLs.
- Avoid unnecessary AI calls.
- Avoid duplicate operations.
- Have retry policies.
- Have execution logging.
- Have documented inputs/outputs.

---

# 79. Development Workflow

Recommended development process:

```text
Design
  ↓
Build workflow
  ↓
Test with sample payload
  ↓
Test failure paths
  ↓
Test duplicate event
  ↓
Test AI failure
  ↓
Test API failure
  ↓
Test notification failure
  ↓
Document
  ↓
Deploy
```

---

# 80. Testing Scenarios

## Scenario 1 — Complete Lead

```text
Customer provides:
Name
Property
Location
Budget
Bedrooms
Transaction
Timeline
```

Expected:

```text
Lead created
AI extraction succeeds
Score calculated
Classification assigned
Response generated
```

---

## Scenario 2 — Missing Budget

Customer:

```text
I want a 3-bedroom apartment in Lekki.
```

Expected:

```text
Property = APARTMENT
Bedrooms = 3
Location = Lekki
Budget = null
```

Bot asks for budget.

---

## Scenario 3 — Hot Lead

Customer provides:

```text
Specific property
High budget
Immediate timeline
Contact details
```

Expected:

```text
High score
HOT classification
Sales notification
Follow-up
```

---

## Scenario 4 — Duplicate Event

Same event received twice.

Expected:

```text
First → processed
Second → ignored safely
```

No duplicate lead or notification.

---

## Scenario 5 — AI Failure

Expected:

```text
Message preserved
AI failure logged
Retry performed
Fallback response used if necessary
```

---

## Scenario 6 — Google Sheets Failure

Expected:

```text
Lead remains successfully stored in PostgreSQL
Sheet sync marked failed
Retry scheduled
```

---

# 81. Agentic Development Rules

AI coding agents working on n8n must follow these rules.

### Rule 1

Do not create a workflow without documenting its purpose.

### Rule 2

Do not modify the database directly from n8n unless explicitly approved.

### Rule 3

Use FastAPI endpoints for application-level database operations.

### Rule 4

Do not invent undocumented event fields.

### Rule 5

Do not expose credentials inside workflow definitions.

### Rule 6

Every workflow needs an error path.

### Rule 7

Every event-driven workflow must consider idempotency.

### Rule 8

Every AI output must be validated.

### Rule 9

Do not trust AI output as authoritative business data.

### Rule 10

Do not create unnecessary AI calls.

### Rule 11

Do not create workflow loops.

### Rule 12

Document every external integration.

---

# 82. Recommended n8n Folder Structure

Conceptually:

```text
n8n/
│
├── workflows/
│   ├── lead/
│   │   ├── process-message
│   │   ├── qualify-lead
│   │   └── notify-sales
│   │
│   ├── follow-ups/
│   │   ├── reminder
│   │   └── escalation
│   │
│   ├── integrations/
│   │   └── google-sheets-sync
│   │
│   ├── ai/
│   │   ├── extraction
│   │   ├── response
│   │   └── summarization
│   │
│   └── system/
│       ├── error-handler
│       └── health-check
│
└── README.md
```

The actual n8n export format may differ.

---

# 83. Environment Configuration

Development:

```text
N8N_ENV=development
API_BASE_URL=http://localhost:8000
```

Staging:

```text
N8N_ENV=staging
API_BASE_URL=<staging-api>
```

Production:

```text
N8N_ENV=production
API_BASE_URL=<production-api>
```

Never hard-code environment-specific endpoints into reusable workflow logic.

---

# 84. Workflow Versioning

Important workflow changes should be versioned.

Example:

```text
PRH-LEAD-PROCESS-MESSAGE-v1
PRH-LEAD-PROCESS-MESSAGE-v2
```

A production workflow should not be changed casually without testing.

---

# 85. Rollback

Before deploying a major workflow change:

```text
Export/backup workflow
        ↓
Deploy new version
        ↓
Test
        ↓
Monitor
```

If the new workflow fails:

```text
Rollback
```

---

# 86. Monitoring Dashboard

The system should eventually provide visibility into:

```text
Total workflow executions
Successful executions
Failed executions
Average processing time
AI failures
API failures
Notification failures
Sheet sync failures
Pending follow-ups
Stale leads
```

---

# 87. Definition of Done

The n8n automation layer is MVP-ready when:

- [ ] Message processing workflow exists.
- [ ] Lead qualification workflow exists.
- [ ] Sales notification workflow exists.
- [ ] Follow-up workflow exists.
- [ ] Google Sheets sync exists.
- [ ] Error handling exists.
- [ ] Idempotency is implemented.
- [ ] AI extraction is structured.
- [ ] AI output is validated.
- [ ] AI prompts are versioned.
- [ ] Credentials are secured.
- [ ] Workflow inputs are documented.
- [ ] Workflow outputs are documented.
- [ ] Retry policies are configured.
- [ ] External failures do not corrupt primary data.
- [ ] Bot loops are prevented.
- [ ] Human handoff is supported.
- [ ] Workflow tests exist.
- [ ] Production workflow backup/versioning exists.

---

# 88. Final Workflow Architecture

The final automation architecture should be:

```text
                         CUSTOMER
                            │
                            ▼
                         REACT UI
                            │
                            ▼
                         FASTAPI
                            │
                            ▼
                           n8n
                            │
             ┌──────────────┼───────────────┐
             │              │               │
             ▼              ▼               ▼
       AI PROCESSING    QUALIFICATION    INTEGRATIONS
             │              │               │
             │              ▼               ├── Google Sheets
             │          Lead Score           ├── Email
             │              │               ├── Telegram
             │              │               └── Other Services
             ▼              ▼
       Structured Data    Classification
             │              │
             └──────┬───────┘
                    ▼
                FASTAPI
                    │
                    ▼
               PostgreSQL
                    │
           ┌────────┼────────┐
           ▼        ▼        ▼
         Leads   Messages  Activities
                    │
                    ▼
              Sales Team
```

---

# 89. Final Architectural Principle

The PrimeHomes Realty automation system should follow this separation:

```text
React
→ User experience

FastAPI
→ API + validation + business boundaries

PostgreSQL
→ Source of truth

n8n
→ Workflow orchestration

AI
→ Interpretation + extraction + generation

Google Sheets
→ Operational projection/reporting

Sales Team
→ Human decision-making + follow-up
```

The objective is not to make n8n or AI responsible for everything.

The objective is to use each technology where it provides the greatest value while keeping the overall system reliable, observable, maintainable, and easy to extend.