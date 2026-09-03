# System Architecture Document (SAD)

## PrimeHomes Realty — Real Estate Lead Bot

**Document:** System Architecture Document  
**Version:** 1.0  
**Status:** Draft  
**Product:** PrimeHomes Realty Real Estate Lead Bot  
**Architecture Style:** Modular Application + Workflow Orchestration  
**Frontend:** React  
**Backend:** FastAPI / Python  
**Automation:** n8n  
**Primary Database:** SQL Database  
**Operational Data / Reporting:** Google Sheets  
**AI Layer:** LLM-based AI Processing

---

# 1. Purpose

This document defines the technical architecture of the PrimeHomes Realty Real Estate Lead Bot.

The purpose of this document is to establish:

- System components
- Component responsibilities
- Service boundaries
- Communication patterns
- Data ownership
- Data flow
- API boundaries
- AI responsibilities
- n8n responsibilities
- Database responsibilities
- Security boundaries
- Failure handling
- Scalability considerations
- Deployment boundaries
- Architectural constraints

This document serves as the primary technical reference for developers, technical stakeholders, and AI coding agents working on the system.

---

# 2. Architectural Goals

The architecture should enable the system to:

1. Receive customer enquiries.
2. Process natural-language messages.
3. Extract structured lead information.
4. Maintain conversation context.
5. Qualify leads.
6. Persist lead information.
7. Notify sales representatives.
8. Allow sales representatives to manage leads.
9. Track lead lifecycle.
10. Support automated follow-up.
11. Handle failures gracefully.
12. Scale as enquiry volume increases.
13. Remain maintainable by a small engineering team.
14. Be understandable by AI coding agents.

---

# 3. Architecture Principles

## 3.1 Separation of Responsibilities

Each component must have a clearly defined responsibility.

```text
React
  → User Interface

FastAPI
  → Application API + Business Logic

n8n
  → Workflow Orchestration + Integrations

AI
  → Language Understanding + Extraction

SQL Database
  → System of Record

Google Sheets
  → Operational Reporting / Lightweight Business Views
```

A component should not perform another component's responsibility simply because it is technically possible.

---

# 3.2 AI Is Not the Source of Truth

AI output must be treated as an interpretation of customer input.

AI should not directly determine critical system state without validation.

For example:

```text
Customer Message
       ↓
AI Extraction
       ↓
Validation
       ↓
Business Rules
       ↓
Database
```

Not:

```text
Customer Message
       ↓
AI
       ↓
Database
```

---

# 3.3 Deterministic Logic Should Remain Deterministic

The following should primarily be handled by traditional application code or explicit workflow rules:

- Validation
- Lead scoring
- State transitions
- Authentication
- Authorization
- Data persistence
- Calculations
- Permission checks
- Retry logic

AI should primarily handle:

- Natural-language understanding
- Entity extraction
- Intent detection
- Conversation assistance
- Summarization
- Response generation

---

# 3.4 SQL Is the System of Record

The SQL database is the authoritative source for core application data.

Google Sheets must not silently become an alternative source of truth.

```text
SQL Database
     ↑
 System of Record
```

Google Sheets can receive synchronized information for:

- Reporting
- Sales visibility
- Operational workflows
- Exports
- Lightweight analysis

---

# 3.5 n8n Is the Workflow Orchestrator

n8n is responsible for coordinating processes between systems.

n8n should not become the application's primary business database.

Its primary role is:

```text
Trigger
  ↓
Orchestrate
  ↓
Transform
  ↓
Call Services
  ↓
Handle Workflow
  ↓
Notify
```

---

# 3.6 Human-in-the-Loop

The system must support human intervention.

AI should be able to hand conversations or leads to sales representatives when:

- The customer requests a human.
- AI confidence is low.
- The enquiry is complex.
- The lead is high-value.
- Negotiation begins.
- The AI cannot safely answer.
- A business rule requires human approval.

---

# 4. High-Level Architecture

The initial architecture is:

```text
                         ┌─────────────────────┐
                         │      CUSTOMER       │
                         └──────────┬──────────┘
                                    │
                                    ▼
                         ┌─────────────────────┐
                         │    REACT FRONTEND   │
                         │                     │
                         │  Chat / Lead Form   │
                         └──────────┬──────────┘
                                    │
                                    ▼
                         ┌─────────────────────┐
                         │      FASTAPI        │
                         │                     │
                         │ API + Business      │
                         │ Logic + Validation  │
                         └──────────┬──────────┘
                                    │
                                    ▼
                         ┌─────────────────────┐
                         │        n8n          │
                         │                     │
                         │ Workflow            │
                         │ Orchestration       │
                         └──────────┬──────────┘
                                    │
                  ┌─────────────────┼──────────────────┐
                  │                 │                  │
                  ▼                 ▼                  ▼
           ┌────────────┐   ┌──────────────┐   ┌──────────────┐
           │     AI     │   │ SQL DATABASE │   │  NOTIFICATION│
           │            │   │              │   │   SERVICES   │
           └────────────┘   └──────────────┘   └──────────────┘
                  │                 │
                  │                 ▼
                  │         ┌──────────────┐
                  │         │ GOOGLE SHEETS│
                  │         └──────────────┘
                  │
                  ▼
           ┌──────────────────┐
           │  SALES TEAM      │
           │ Dashboard / CRM  │
           └──────────────────┘
```

---

# 5. Architecture Components

## 5.1 React Frontend

### Responsibility

The React application provides the user interface for customers and internal sales users.

### Customer-facing functionality

- Chat interface
- Lead capture
- Conversation display
- Bot responses
- Loading states
- Error states
- Contact information collection

### Sales-facing functionality

- Login
- Lead dashboard
- Lead details
- Lead status
- Lead assignment
- Conversation history
- Follow-up notes
- Follow-up dates
- Lead filtering

### React must not

- Contain core business rules.
- Directly access the SQL database.
- Contain database credentials.
- Call AI providers directly for production workflows.
- Implement lead scoring independently of the backend.

Communication should occur through the FastAPI API.

---

# 6. FastAPI Backend

FastAPI acts as the application's primary backend API.

## Responsibilities

- API endpoints
- Request validation
- Response validation
- Authentication
- Authorization
- Business logic
- Lead management
- Conversation management
- Database interaction
- State transitions
- Lead scoring
- Internal API integration
- Security controls

### Example API responsibilities

```text
POST /api/v1/chat
POST /api/v1/leads
GET  /api/v1/leads
GET  /api/v1/leads/{lead_id}
PATCH /api/v1/leads/{lead_id}
POST /api/v1/leads/{lead_id}/follow-ups
GET  /api/v1/leads/{lead_id}/messages
```

The final API contract will be defined in the API Specification document.

---

# 7. n8n Workflow Engine

n8n is the automation and orchestration layer.

## Responsibilities

- Trigger workflows
- Call AI services
- Process workflow data
- Integrate external systems
- Send notifications
- Synchronize selected data with Google Sheets
- Trigger follow-up workflows
- Execute scheduled jobs
- Handle workflow-level retries
- Route events

### Example workflow

```text
FastAPI Webhook
      ↓
Validate Event
      ↓
Retrieve Conversation
      ↓
AI Processing
      ↓
Validate AI Output
      ↓
Lead Qualification
      ↓
Update SQL
      ↓
Send Customer Response
      ↓
Notify Sales Team
```

---

# 8. AI Processing Layer

The AI layer provides natural-language intelligence.

## Responsibilities

### Intent Detection

Determine whether the customer is:

```text
BUYING
RENTING
SELLING
LAND_ENQUIRY
PROPERTY_ENQUIRY
GENERAL_ENQUIRY
UNKNOWN
```

### Entity Extraction

Extract:

```text
name
email
phone
property_type
bedrooms
location
budget
transaction_type
timeline
```

### Missing Information Detection

Determine which required fields remain unknown.

### Response Generation

Generate appropriate customer-facing responses.

### Conversation Summarization

Create concise summaries for sales representatives.

---

# 9. AI Output Contract

AI responses should be structured.

Example:

```json
{
  "intent": "BUY",
  "confidence": 0.94,
  "extracted_data": {
    "property_type": "apartment",
    "bedrooms": 3,
    "location": "Lekki",
    "budget_max": 80000000,
    "currency": "NGN",
    "timeline": "WITHIN_3_MONTHS"
  },
  "missing_fields": [
    "phone"
  ],
  "suggested_action": "ASK_FOR_PHONE",
  "response": "Great. Could you please provide your phone number so our team can contact you?"
}
```

AI output must be validated against a defined schema before being used by the application.

---

# 10. AI Confidence

AI extraction should include confidence information where supported.

Example:

```text
location confidence: 0.96
property type confidence: 0.91
budget confidence: 0.99
timeline confidence: 0.61
```

Low-confidence information should not automatically become authoritative customer data.

Example:

```text
confidence < threshold
        ↓
Ask clarification
```

---

# 11. Lead Qualification Engine

Lead qualification should be deterministic wherever possible.

Architecture:

```text
AI Extraction
      ↓
Structured Lead Data
      ↓
Validation
      ↓
Qualification Rules
      ↓
Lead Score
      ↓
Lead Classification
```

Example:

```text
Score >= 80 → HOT
Score 50-79 → WARM
Score < 50  → COLD
```

The exact scoring model will be defined in the Technical Specification.

---

# 12. SQL Database

The SQL database is the primary application datastore.

Potential implementation:

```text
PostgreSQL
```

or another suitable SQL database selected during implementation.

## Core entities

```text
User
Lead
Conversation
Message
LeadScore
LeadAssignment
FollowUp
Activity
```

Potential relationships:

```text
User
 │
 ├── owns/handles ──> Leads
 │
 └── performs ──────> Activities

Lead
 │
 ├── has ──> Conversation
 │
 ├── has ──> Messages
 │
 ├── has ──> FollowUps
 │
 ├── has ──> Activities
 │
 └── has ──> LeadScore
```

The exact schema will be defined in the Database Design document.

---

# 13. Google Sheets

Google Sheets is considered a secondary operational data destination.

Possible use cases:

```text
SQL Database
      ↓
n8n
      ↓
Google Sheets
```

Examples:

- Sales team export
- Daily lead report
- Lead summary
- Management reporting
- Lightweight operational tracking

### Important Rule

If SQL and Google Sheets contain conflicting information:

```text
SQL Database = authoritative
Google Sheets = secondary
```

The synchronization process must be documented.

---

# 14. Notification Layer

The system should support sales-team notifications.

Potential channels:

- Email
- Slack
- Telegram
- WhatsApp
- Microsoft Teams

The initial implementation can select one or more channels.

### Notification example

```text
🔥 HOT LEAD

Customer: John Doe
Intent: Buying
Property: 3 Bedroom Apartment
Location: Lekki
Budget: ₦80,000,000
Timeline: Within 2 Months
Lead Score: 88

Action:
Contact customer immediately.
```

Notification delivery should occur after successful lead persistence whenever possible.

---

# 15. End-to-End Customer Message Flow

## Scenario

Customer sends:

> “Hi, I need a 3-bedroom apartment around Lekki. My budget is around ₦80 million.”

### Step 1 — React

React sends:

```http
POST /api/v1/chat
```

---

### Step 2 — FastAPI

FastAPI:

- Validates request
- Identifies conversation
- Stores incoming message if appropriate
- Sends processing request/event to n8n

---

### Step 3 — n8n

n8n receives the workflow event.

---

### Step 4 — AI

AI extracts:

```json
{
  "property_type": "APARTMENT",
  "bedrooms": 3,
  "location": "Lekki",
  "budget_max": 80000000,
  "currency": "NGN",
  "transaction_type": "BUY"
}
```

---

### Step 5 — Validation

System validates:

```text
property_type ✓
bedrooms ✓
location ✓
budget ✓
currency ✓
transaction_type ✓
```

---

### Step 6 — Qualification

Qualification engine calculates:

```text
Score = 85
Classification = HOT
```

---

### Step 7 — Database

Lead and conversation information are stored in SQL.

---

### Step 8 — Customer Response

Bot responds:

> “Thanks! I’ve captured your requirements. Our team will review suitable options and get back to you shortly.”

---

### Step 9 — Sales Notification

Sales team receives:

```text
HOT LEAD
3-bedroom
Lekki
₦80M
Buying
```

---

# 16. Conversation Architecture

A customer conversation should be represented separately from the lead.

```text
Customer
    ↓
Conversation
    ↓
Messages
    ↓
Lead
```

A conversation may contain multiple messages.

Example:

```text
Conversation #123

Message 1:
"I need a house."

Message 2:
"I want to buy."

Message 3:
"3 bedroom."

Message 4:
"Somewhere around Lekki."

Message 5:
"Budget is 80m."
```

The system should combine the relevant conversation context when processing subsequent messages.

---

# 17. Lead State Management

Lead status must follow a controlled state model.

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
 ↓
VIEWING_SCHEDULED
 ↓
NEGOTIATING
 ↓
CONVERTED
```

Alternative paths:

```text
QUALIFIED
    ↓
  NURTURE
```

```text
CONTACTED
    ↓
  LOST
```

State transitions must be validated by the backend.

The frontend must not arbitrarily set invalid states.

---

# 18. Event-Driven Interactions

The system can use events to reduce tight coupling.

Example:

```text
LeadCreated
LeadQualified
LeadScored
LeadAssigned
CustomerReplied
FollowUpDue
LeadConverted
LeadLost
```

Example:

```text
LeadQualified
      ↓
     n8n
      ↓
 ┌────┴───────────┐
 ↓                ↓
Notify Sales   Update Sheet
```

Events should contain sufficient identifiers to retrieve the authoritative data from SQL.

---

# 19. Synchronous vs Asynchronous Processing

Not every operation should happen in a single HTTP request.

### Synchronous

Use synchronous processing for operations requiring immediate responses.

Examples:

```text
Authentication
Basic validation
Simple CRUD
Dashboard queries
```

### Asynchronous

Use asynchronous processing for operations that may take longer.

Examples:

```text
AI processing
Notifications
Google Sheets synchronization
Follow-up automation
Long-running workflows
```

Potential pattern:

```text
Customer
   ↓
FastAPI
   ↓
Create Message
   ↓
Trigger Workflow
   ↓
Immediate Response
```

Then:

```text
n8n
 ↓
AI
 ↓
Qualification
 ↓
Database
 ↓
Notification
```

---

# 20. Failure Handling

The architecture must assume that external systems can fail.

Potential failures:

```text
React failure
FastAPI failure
AI provider failure
n8n failure
SQL failure
Google Sheets failure
Notification failure
Network failure
```

---

## 20.1 AI Failure

If AI fails:

```text
AI Request
    ↓
Failure
    ↓
Retry
    ↓
If retry fails
    ↓
Fallback
    ↓
Human review / retry
```

The original customer message must not be lost.

---

## 20.2 Notification Failure

A notification failure must not roll back a successfully stored lead.

Example:

```text
Store Lead ✓
     ↓
Send Notification
     ↓
Failure
     ↓
Retry / Queue
```

The lead remains stored.

---

## 20.3 Google Sheets Failure

Google Sheets is secondary.

Therefore:

```text
SQL Save ✓
     ↓
Google Sheets
     ↓
Failure
```

must not cause the lead creation process to fail.

The synchronization can be retried later.

---

# 21. Idempotency

The system should prevent duplicate lead creation caused by retries or repeated requests.

For example:

```text
Same event ID
      ↓
Already processed?
      ↓
YES
      ↓
Do not process again
```

This is particularly important for:

- Webhooks
- n8n workflows
- Notifications
- Database updates
- External integrations

---

# 22. Security Architecture

## Customer-facing API

Must implement:

- Request validation
- Rate limiting where necessary
- Input sanitization
- Secure communication
- Abuse protection

## Internal dashboard

Must implement:

```text
Authentication
      ↓
Authorization
      ↓
Role-based access
```

Possible roles:

```text
ADMIN
MANAGER
SALES_AGENT
```

---

# 23. Secrets Management

Secrets must never be stored in:

```text
Source code
Git repository
Frontend JavaScript
README
Database records
```

Examples:

```text
AI_API_KEY
DATABASE_URL
JWT_SECRET
N8N_API_KEY
GOOGLE_SERVICE_ACCOUNT
NOTIFICATION_API_KEY
```

These should be stored through environment variables or an appropriate secrets-management system.

---

# 24. API Security Boundary

The architecture should follow:

```text
Browser
   ↓
Public API
   ↓
FastAPI
   ↓
Internal Services
```

The browser should never directly access:

```text
SQL Database
AI Provider
n8n internal credentials
Google service credentials
```

---

# 25. Observability

Each request/workflow should have a correlation identifier.

Example:

```text
request_id = req_abc123
```

This identifier can be used to trace:

```text
React
 ↓
FastAPI
 ↓
n8n
 ↓
AI
 ↓
SQL
 ↓
Notification
```

Logs should help answer:

- What happened?
- When did it happen?
- Which lead was affected?
- Which workflow processed it?
- Did AI succeed?
- Did database persistence succeed?
- Did notification succeed?

---

# 26. Logging

Logs should contain useful operational information without exposing sensitive data.

Example:

```text
INFO
lead_id=lead_123
event=lead_qualified
score=86
classification=HOT
```

Avoid logging:

```text
passwords
API keys
tokens
full sensitive customer data
```

---

# 27. Monitoring

The system should eventually monitor:

### Application

- API errors
- API latency
- Request volume

### AI

- AI failures
- AI latency
- Extraction failures
- Low-confidence responses

### n8n

- Workflow failures
- Workflow duration
- Retry count

### Database

- Connection failures
- Query performance
- Storage

### Business

- Number of leads
- Hot leads
- Conversion rate
- Follow-up rate

---

# 28. Scalability Strategy

The initial system should avoid premature complexity.

We do not need to begin with:

```text
20 microservices
Kafka
Kubernetes
Multiple databases
Complex event infrastructure
```

A more appropriate initial architecture is:

```text
React
   ↓
FastAPI
   ↓
SQL Database

n8n
   ↓
External integrations
AI
Notifications
Automation
```

As demand grows, individual components can be scaled independently.

---

# 29. Initial Deployment Model

A possible deployment:

```text
                INTERNET
                    │
                    ▼
             ┌─────────────┐
             │   React     │
             │   Frontend  │
             └──────┬──────┘
                    │
                    ▼
             ┌─────────────┐
             │   FastAPI   │
             │   Backend   │
             └──────┬──────┘
                    │
          ┌─────────┴──────────┐
          ▼                    ▼
   ┌─────────────┐       ┌─────────────┐
   │ SQL Database│       │     n8n     │
   └─────────────┘       └──────┬──────┘
                                │
                   ┌────────────┼────────────┐
                   ▼            ▼            ▼
                  AI       Notifications   Sheets
```

The exact cloud provider and infrastructure will be defined later.

---

# 30. Repository Architecture

Initial repository structure:

```text
real-estate-lead-bot/
│
├── frontend/
│   ├── src/
│   │   ├── components/
│   │   ├── pages/
│   │   ├── services/
│   │   ├── hooks/
│   │   ├── types/
│   │   └── utils/
│   ├── package.json
│   └── README.md
│
├── backend/
│   ├── app/
│   │   ├── api/
│   │   ├── core/
│   │   ├── models/
│   │   ├── schemas/
│   │   ├── services/
│   │   ├── repositories/
│   │   └── main.py
│   │
│   ├── tests/
│   ├── requirements.txt
│   └── README.md
│
├── n8n/
│   ├── workflows/
│   ├── schemas/
│   └── README.md
│
├── database/
│   ├── migrations/
│   ├── seeds/
│   └── README.md
│
├── docs/
│   ├── product/
│   ├── architecture/
│   ├── technical/
│   ├── api/
│   ├── database/
│   ├── features/
│   ├── testing/
│   └── operations/
│
├── tests/
│
├── .env.example
├── AGENTS.md
├── CONTRIBUTING.md
└── README.md
```

The structure may evolve, but responsibilities should remain separated.

---

# 31. Component Ownership Matrix

| Component | Owns | Does Not Own |
|---|---|---|
| React | UI state and presentation | Business truth |
| FastAPI | API + core business logic | UI |
| n8n | Workflow orchestration | Primary database |
| AI | Language interpretation | Authoritative business state |
| SQL | Persistent application data | UI/workflows |
| Google Sheets | Operational reporting | System of record |
| Notification Service | Message delivery | Lead state |

---

# 32. Data Ownership Rules

## Lead

Owned by:

```text
SQL Database
```

## Conversation

Owned by:

```text
SQL Database
```

## Message

Owned by:

```text
SQL Database
```

## Lead Score

Owned by:

```text
Application / Qualification Logic
```

and persisted in SQL.

## Workflow State

Owned by:

```text
n8n
```

where appropriate.

## Reporting Copy

Owned by:

```text
Google Sheets
```

but derived from SQL.

---

# 33. Architectural Boundaries

The following boundaries must be maintained.

### Boundary 1

```text
React → FastAPI
```

Not:

```text
React → SQL
```

---

### Boundary 2

```text
FastAPI → SQL
```

Not:

```text
React → SQL
```

---

### Boundary 3

```text
n8n → AI
```

through controlled integration.

---

### Boundary 4

```text
n8n → Google Sheets
```

for secondary synchronization.

---

### Boundary 5

```text
AI → Structured Output
```

then:

```text
Structured Output
      ↓
Validation
      ↓
Business Logic
```

AI must not bypass validation.

---

# 34. Architecture Decision Summary

The current architectural decisions are:

| Decision | Choice |
|---|---|
| Frontend | React |
| Backend | FastAPI |
| Language | Python |
| Automation | n8n |
| Primary database | SQL |
| Initial SQL preference | PostgreSQL |
| Secondary operational storage | Google Sheets |
| AI | LLM-based service |
| Architecture | Modular application + workflow orchestration |
| Lead scoring | Deterministic rules |
| AI output | Structured JSON/schema |
| Authentication | Backend-controlled |
| Authorization | Role-based |
| Primary data source | SQL |
| Workflow orchestration | n8n |
| Human escalation | Supported |
| Microservices | Not required for MVP |

---

# 35. Architectural Constraints

AI coding agents and developers must follow these constraints.

### Constraint 1

Do not introduce a new backend service without documenting the architectural reason.

### Constraint 2

Do not allow frontend code to directly access the database.

### Constraint 3

Do not store secrets in source code.

### Constraint 4

Do not allow AI-generated values to bypass validation.

### Constraint 5

Do not make Google Sheets the authoritative database.

### Constraint 6

Do not put core business logic inside React components.

### Constraint 7

Do not put all business logic inside n8n workflows.

### Constraint 8

Do not duplicate lead-scoring logic across frontend, backend and n8n.

### Constraint 9

Do not introduce microservices merely for organizational appearance.

### Constraint 10

Every major architectural change must be recorded as an ADR.

---

# 36. Future Architecture Evolution

The architecture should be capable of evolving toward:

```text
                         CUSTOMER
                            │
                            ▼
                     CHANNEL LAYER
              ┌─────────────┼─────────────┐
              │             │             │
           Website       WhatsApp       Email
              │             │             │
              └─────────────┼─────────────┘
                            ▼
                     API / Gateway
                            │
                            ▼
                    Lead Management
                            │
             ┌──────────────┼──────────────┐
             ▼              ▼              ▼
        AI Services   Qualification    Property
                       Engine           Matching
             │              │              │
             └──────────────┼──────────────┘
                            ▼
                      SQL Database
                            │
             ┌──────────────┼──────────────┐
             ▼              ▼              ▼
          Analytics       CRM          Automation
```

This is future scope, not an MVP requirement.

---

# 37. Architecture Validation Checklist

Before implementation begins, verify:

- [ ] Component responsibilities are defined.
- [ ] Data ownership is defined.
- [ ] SQL is established as the system of record.
- [ ] Google Sheets is clearly secondary.
- [ ] n8n responsibilities are defined.
- [ ] AI responsibilities are defined.
- [ ] Frontend/backend boundary is defined.
- [ ] Authentication boundary is defined.
- [ ] Lead state model is defined.
- [ ] Failure handling is defined.
- [ ] Retry strategy is defined.
- [ ] Idempotency strategy is defined.
- [ ] Observability requirements are defined.
- [ ] Security boundaries are defined.
- [ ] Repository structure is defined.
- [ ] Architecture constraints are documented.
- [ ] Future scaling path is understood.

---

# 38. Relationship With Other Documents

This architecture document is the technical foundation for subsequent engineering documents.

```text
PRD
 │
 │ Product Requirements
 ▼
SYSTEM ARCHITECTURE
 │
 ├───────────────┐
 ▼               ▼
DATABASE       API CONTRACT
DESIGN         SPECIFICATION
 │               │
 └───────┬───────┘
         ▼
TECHNICAL SPECIFICATIONS
         │
         ├──────────────┐
         ▼              ▼
       n8n             React
     Workflows        Features
         │              │
         └──────┬───────┘
                ▼
          IMPLEMENTATION
                │
                ▼
              TESTS
```

---

# 39. Final Architectural Principle

The Real Estate Lead Bot should be treated as a **small distributed business system**, even though its first implementation can remain relatively simple.

The architecture should optimize for:

```text
Clarity
   +
Reliability
   +
Maintainability
   +
Observability
   +
AI-Agent Compatibility
   +
Controlled Complexity
```

The system should not be designed around:

```text
"How many technologies can we use?"
```

Instead, every technology must have a clear responsibility.

The target architecture is therefore:

```text
React
  ↓
FastAPI
  ↓
SQL
```

with:

```text
n8n
  ↓
Workflow orchestration
  ↓
AI
  ↓
Notifications
  ↓
Google Sheets synchronization
```

while keeping **business-critical state and data ownership inside the application architecture rather than inside AI prompts or automation workflows**.