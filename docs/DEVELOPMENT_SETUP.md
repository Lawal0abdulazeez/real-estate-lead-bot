# DEVELOPMENT_SETUP.md

# Real Estate Lead Bot — Development Setup & Implementation Guide

## 1. Purpose

This document explains how the Real Estate Lead Bot should be set up and developed.

The goal is to provide a simple implementation guide that developers and AI coding agents can follow without introducing unnecessary complexity.

The project should be developed in small, testable stages.

---

# 2. Core Technology Stack

The initial stack is:

```text
Frontend
→ React

Backend
→ Python + FastAPI

Database
→ PostgreSQL

Automation
→ n8n

AI
→ LLM through the chosen AI provider

Reporting / Operations
→ Google Sheets
```

---

# 3. Development Philosophy

The project should follow these principles:

### Keep it simple

Do not introduce technologies that are not required.

### Build incrementally

Do not attempt to build the entire system at once.

### Test as we go

Each major feature should work before moving to the next one.

### Keep responsibilities clear

Each technology should do what it is best suited for.

### Avoid unnecessary abstraction

Do not create complicated architectures for simple functionality.

---

# 4. Initial Project Structure

```text
real-estate-lead-bot/
│
├── frontend/
│
├── backend/
│
├── n8n/
│
├── database/
│
├── tests/
│
├── docs/
│
├── .env.example
├── .gitignore
├── README.md
└── docker-compose.yml
```

The structure can be adjusted as development progresses.

---

# 5. Frontend Structure

The React application should be organized around features rather than putting everything into a single folder.

Recommended structure:

```text
frontend/
│
├── src/
│   ├── components/
│   │   ├── ui/
│   │   ├── chat/
│   │   ├── leads/
│   │   ├── dashboard/
│   │   └── followups/
│   │
│   ├── pages/
│   │   ├── customer/
│   │   ├── auth/
│   │   └── dashboard/
│   │
│   ├── services/
│   │
│   ├── hooks/
│   │
│   ├── types/
│   │
│   ├── utils/
│   │
│   └── app/
│
├── package.json
└── README.md
```

---

# 6. Backend Structure

Recommended FastAPI structure:

```text
backend/
│
├── app/
│   ├── main.py
│   │
│   ├── api/
│   │   └── v1/
│   │       ├── auth.py
│   │       ├── leads.py
│   │       ├── conversations.py
│   │       ├── messages.py
│   │       ├── followups.py
│   │       └── health.py
│   │
│   ├── models/
│   │
│   ├── schemas/
│   │
│   ├── services/
│   │
│   ├── repositories/
│   │
│   ├── core/
│   │
│   └── db/
│
├── tests/
│
├── requirements.txt
└── README.md
```

---

# 7. Backend Responsibilities

FastAPI should handle:

- API endpoints.
- Request validation.
- Authentication.
- Authorization.
- Database operations.
- Lead management.
- Conversation management.
- Message management.
- Lead status updates.
- Lead assignments.
- Follow-up management.
- Business rules.

FastAPI should not contain large automation workflows.

Those belong in n8n.

---

# 8. Database Setup

PostgreSQL should be the primary database.

The application should use a database URL stored in an environment variable.

Example:

```env
DATABASE_URL=postgresql://username:password@localhost:5432/real_estate_leads
```

Credentials must not be committed to Git.

---

# 9. Database Migration

Use a migration system such as Alembic.

Initial process:

```text
Create database
      ↓
Configure connection
      ↓
Create SQLAlchemy models
      ↓
Create migration
      ↓
Run migration
      ↓
Verify tables
```

Example:

```bash
alembic revision --autogenerate -m "initial schema"
```

Then:

```bash
alembic upgrade head
```

---

# 10. Environment Variables

Create:

```text
.env
```

for local development.

Also provide:

```text
.env.example
```

as a safe template.

Example:

```env
APP_ENV=development

DATABASE_URL=

JWT_SECRET=

N8N_WEBHOOK_URL=

N8N_WEBHOOK_SECRET=

AI_API_KEY=

GOOGLE_SHEETS_CREDENTIALS=

CORS_ORIGINS=
```

The actual `.env` file must never be committed.

---

# 11. API Development Order

Build the API in this order:

### Step 1 — Health

```text
GET /api/v1/health
```

Purpose:

Verify that the backend is running.

---

### Step 2 — Authentication

Implement:

```text
POST /api/v1/auth/login
```

Then add protected endpoints.

---

### Step 3 — Leads

Implement:

```text
POST /api/v1/leads
GET /api/v1/leads
GET /api/v1/leads/{id}
PATCH /api/v1/leads/{id}
```

---

### Step 4 — Conversations

Implement:

```text
POST /api/v1/conversations
GET /api/v1/conversations/{id}
```

---

### Step 5 — Messages

Implement:

```text
POST /api/v1/messages
GET /api/v1/conversations/{id}/messages
```

---

### Step 6 — Qualification

Implement the endpoint required to qualify or update a lead.

Example:

```text
POST /api/v1/leads/{id}/qualify
```

---

### Step 7 — Follow-ups

Implement:

```text
POST /api/v1/leads/{id}/follow-ups
GET /api/v1/leads/{id}/follow-ups
PATCH /api/v1/follow-ups/{id}
```

---

# 12. Customer Message Flow

The customer-facing message flow should be:

```text
Customer
   ↓
React
   ↓
POST /messages
   ↓
FastAPI
   ↓
Store customer message
   ↓
Trigger n8n
   ↓
AI processing
   ↓
Lead information extracted
   ↓
Lead updated
   ↓
Response generated
   ↓
Bot response stored
   ↓
React receives response
```

The customer should not communicate directly with n8n.

---

# 13. n8n Setup

Create an n8n environment for the project.

Recommended workflow directory:

```text
n8n/
│
├── workflows/
│   ├── lead-process-message.json
│   ├── lead-qualify.json
│   ├── lead-notify-sales.json
│   ├── followup-reminder.json
│   └── error-handler.json
│
└── README.md
```

Workflow names should remain consistent.

Example:

```text
PRH-LEAD-PROCESS-MESSAGE
PRH-LEAD-QUALIFY
PRH-LEAD-NOTIFY-SALES
PRH-FOLLOWUP-REMINDER
PRH-ERROR-HANDLER
```

---

# 14. First n8n Workflow

The first workflow to build should be:

```text
PRH-LEAD-PROCESS-MESSAGE
```

Basic flow:

```text
Webhook
   ↓
Validate Input
   ↓
Get Conversation Context
   ↓
AI Extraction
   ↓
Validate AI Result
   ↓
Update Lead
   ↓
Check Missing Information
   ↓
Generate Response
   ↓
Save Response
   ↓
Notify Customer
```

Do not build every workflow before testing this one.

---

# 15. AI Implementation

AI should initially focus on only the most important tasks.

### Task 1 — Intent Detection

Determine whether the customer wants to:

```text
BUY
RENT
SELL
LAND
PROPERTY_ENQUIRY
GENERAL_ENQUIRY
HUMAN_AGENT
OTHER
```

### Task 2 — Information Extraction

Extract:

```text
Name
Email
Phone
Property type
Bedrooms
Location
Budget
Transaction type
Timeline
```

### Task 3 — Response Generation

Generate a short, helpful response.

---

# 16. AI Output

AI should return structured data.

Example:

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

The application should validate this response before using it.

---

# 17. Handling Missing Information

The bot should not ask for every field immediately.

Example:

### Customer

```text
I want to buy a house in Lekki.
```

The system already knows:

```text
Intent: BUY
Location: Lekki
Property type: HOUSE
```

Instead of asking several questions, it should ask something useful:

```text
Great! What budget range are you working with, and how many bedrooms are you looking for?
```

---

# 18. Lead Qualification

Once enough information has been collected:

```text
Lead Information
      ↓
Qualification Rules
      ↓
Lead Score
      ↓
Classification
```

Example:

```text
Score: 90
Classification: HOT
```

The qualification system should remain simple initially.

The exact scoring rules should be defined in the qualification implementation rather than duplicated across React, FastAPI, and n8n.

---

# 19. Sales Notification

If a lead is classified as HOT:

```text
Lead
 ↓
Score
 ↓
HOT
 ↓
n8n
 ↓
Sales Notification
```

The notification should contain useful information such as:

```text
New Hot Lead

Name: John Doe
Property: 3-bedroom apartment
Location: Lekki
Budget: ₦80,000,000
Timeline: Within 3 months
Score: 90
```

---

# 20. Google Sheets

Google Sheets should be treated as a secondary operational tool.

Example:

```text
PostgreSQL
    ↓
n8n
    ↓
Google Sheets
```

The system should not depend on Google Sheets to function.

If Google Sheets is temporarily unavailable:

```text
PostgreSQL → Continue working
Google Sheets → Sync later
```

---

# 21. Testing Strategy

Testing should happen at three main levels.

## Backend Tests

Test:

- API endpoints.
- Validation.
- Database operations.
- Lead creation.
- Lead updates.
- Authentication.
- Business rules.

---

## AI Tests

Test messages such as:

```text
I want a 3 bedroom apartment in Lekki.
```

```text
Looking for land around Ibadan under 20 million.
```

```text
I need somewhere to rent in Ikeja.
```

```text
I don't know exactly what I want yet.
```

```text
Can I speak with someone?
```

Verify that the AI extracts the correct information.

---

## Workflow Tests

Test:

- Successful workflow.
- Missing information.
- Invalid AI output.
- API failure.
- Notification failure.
- Duplicate messages.
- Customer response generation.

---

# 22. Local Development

A developer should be able to run the main services locally.

Example:

```text
React
localhost:3000

FastAPI
localhost:8000

PostgreSQL
localhost:5432

n8n
localhost:5678
```

Exact ports can be changed if necessary.

---

# 23. Docker

Docker may be used to simplify local setup.

A basic development environment can contain:

```text
React
FastAPI
PostgreSQL
n8n
```

The AI provider does not need to run locally unless there is a specific reason to do so.

---

# 24. Recommended Development Sequence

The coding agent should follow this sequence.

```text
1. Project setup
       ↓
2. Database
       ↓
3. FastAPI health endpoint
       ↓
4. Lead APIs
       ↓
5. Conversation/message APIs
       ↓
6. React customer interface
       ↓
7. Basic n8n workflow
       ↓
8. AI extraction
       ↓
9. Lead qualification
       ↓
10. Customer responses
       ↓
11. Sales notifications
       ↓
12. Sales dashboard
       ↓
13. Follow-ups
       ↓
14. Testing
       ↓
15. Refinement
```

---

# 25. Definition of Done

A feature is not considered complete simply because the code has been written.

A feature should:

- Work as expected.
- Follow the existing architecture.
- Have appropriate validation.
- Handle basic errors.
- Be tested.
- Not break existing functionality.
- Have clear naming.
- Avoid unnecessary complexity.

For important backend features, include tests.

For important workflows, test both success and failure paths.

---

# 26. AI Coding Agent Instructions

When an AI coding agent is working on this repository:

### Before coding

Read:

```text
README.md
PRD.md
DATABASE_DESIGN.md
API_SPEC.md
N8N_WORKFLOW_SPEC.md
AI_SPEC.md
UI_UX_SPEC.md
```

Only read the documents relevant to the requested task when the project becomes large.

---

### Before changing architecture

Ask:

```text
Is this actually required?
```

If not, use the existing architecture.

---

### Before adding a dependency

Ask:

```text
Can the existing stack solve this cleanly?
```

If yes, do not add another dependency.

---

### Before creating a new service

Ask:

```text
Does this functionality really need a separate service?
```

If not, keep it inside the appropriate existing layer.

---

# 27. What Not To Do

Do not:

- Create unnecessary microservices.
- Add multiple databases without a real requirement.
- Put business logic in React.
- Allow React to access PostgreSQL directly.
- Put all logic inside n8n.
- Allow AI to directly modify the database.
- Duplicate the same business rules across multiple systems.
- Add unnecessary infrastructure.
- Build advanced features before the MVP works.
- Over-engineer simple workflows.

---

# 28. First Development Milestone

The first milestone is not the complete product.

It is:

```text
Customer
   ↓
React Chat
   ↓
FastAPI
   ↓
PostgreSQL
```

The customer should be able to send a message and have it successfully stored.

Once this works:

```text
React
   ↓
FastAPI
   ↓
PostgreSQL
   ↓
n8n
```

Then introduce AI processing.

This incremental approach makes debugging much easier.

---

# 29. Final Principle

The project should always prioritize:

```text
Simplicity
    +
Reliability
    +
Clear Responsibilities
    +
Good User Experience
```

over unnecessary technical complexity.

The objective is to build a system that actually solves the real estate lead problem—not to build the most complicated architecture possible.
