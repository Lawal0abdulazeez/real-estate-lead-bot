# REAL ESTATE LEAD BOT

## PrimeHomes Realty

> An AI-powered real estate lead management system that receives customer enquiries, understands their requirements, qualifies leads, stores customer information, and helps the sales team follow up efficiently.

---

# 1. Project Overview

The **Real Estate Lead Bot** is a digital receptionist and lead qualification system for **PrimeHomes Realty**.

The system is designed to handle incoming customer enquiries automatically instead of requiring a salesperson to manually process every message.

A customer can simply send a message such as:

> "Hi, I'm looking for a 3-bedroom apartment around Lekki. My budget is around ₦80 million."

The system should understand the message, extract the useful information, determine whether additional information is required, qualify the lead, store the information, respond to the customer, and notify the sales team when necessary.

---

# 2. Main Goal

The main goal is to reduce the amount of manual work required to process real estate enquiries.

The system should help PrimeHomes Realty:

- Respond to customers faster.
- Capture leads automatically.
- Reduce forgotten enquiries.
- Extract useful customer information.
- Identify valuable leads.
- Notify sales representatives.
- Maintain conversation history.
- Support follow-up.
- Keep lead information organized.

---

# 3. How the System Works

The basic flow is:

```text
CUSTOMER
   ↓
REACT CUSTOMER INTERFACE
   ↓
FASTAPI BACKEND
   ↓
N8N WORKFLOW
   ↓
AI PROCESSING
   ↓
LEAD QUALIFICATION
   ↓
POSTGRESQL DATABASE
   ↓
SALES TEAM
   ↓
FOLLOW-UP
```

A typical interaction looks like:

```text
Customer sends message
        ↓
System receives message
        ↓
Understand customer request
        ↓
Extract available information
        ↓
Check missing information
        ↓
Ask clarification if necessary
        ↓
Qualify the lead
        ↓
Calculate lead score
        ↓
Save/update lead
        ↓
Respond to customer
        ↓
Notify sales team when necessary
```

---

# 4. Example

### Customer

```text
Hi, I'm looking for a 3-bedroom apartment around Lekki.
My budget is around ₦80 million.
I want to buy within the next two months.
```

### System extracts

```json
{
  "intent": "BUY",
  "property_type": "APARTMENT",
  "bedrooms": 3,
  "location": "Lekki",
  "budget_max": 80000000,
  "currency": "NGN",
  "timeline": "WITHIN_3_MONTHS"
}
```

### System then

1. Validates the extracted information.
2. Updates the customer's lead.
3. Calculates the lead score.
4. Classifies the lead.
5. Stores the information.
6. Generates an appropriate response.
7. Notifies the sales team if the lead requires attention.

---

# 5. Technology Stack

| Layer | Technology | Main Responsibility |
|---|---|---|
| Frontend | React | Customer interface and sales dashboard |
| Backend | FastAPI / Python | API and application logic |
| Automation | n8n | Workflow orchestration |
| Database | PostgreSQL | Main source of truth |
| AI | LLM | Understanding and generating responses |
| Reporting | Google Sheets | Operational/reporting projection |
| API Format | REST / JSON | Communication between services |

---

# 6. Responsibility of Each Technology

## React

React is responsible for the user interface.

It handles:

- Customer chat interface.
- Lead forms.
- Sales dashboard.
- Lead lists.
- Lead details.
- Conversation display.
- Follow-up interface.
- Loading and error states.

React should **not**:

- Connect directly to PostgreSQL.
- Calculate the official lead score.
- Implement important business rules.
- Store sensitive backend credentials.

---

## FastAPI

FastAPI is the main application/API layer.

It handles:

- API endpoints.
- Request validation.
- Authentication.
- Authorization.
- Business rules.
- Database access.
- Lead management.
- Conversation management.
- Communication with n8n.

FastAPI acts as the main boundary between the frontend and backend systems.

---

## n8n

n8n handles automation and workflow orchestration.

It is responsible for:

- Triggering workflows.
- Calling AI services.
- Processing lead information.
- Sending notifications.
- Scheduling follow-ups.
- Google Sheets synchronization.
- Connecting external services.
- Handling automation logic.

The principle is:

> **FastAPI manages the application. n8n manages the workflows.**

---

## AI

AI is responsible for understanding natural language.

It can:

- Identify customer intent.
- Extract property requirements.
- Identify budget.
- Identify location.
- Identify bedrooms.
- Identify timeline.
- Generate customer responses.
- Summarize conversations.
- Detect when human assistance may be required.

AI should not be responsible for:

- Authentication.
- Database integrity.
- User permissions.
- Final business rules.
- Direct database writes.

---

## PostgreSQL

PostgreSQL is the primary source of truth.

It stores:

- Leads.
- Conversations.
- Messages.
- Lead scores.
- Assignments.
- Follow-ups.
- Activities.
- Integration records.

Google Sheets may contain useful operational information, but it should not replace the main database.

---

# 7. Core Lead Information

The system should gradually collect the following information.

### Customer Information

- Name
- Email
- Phone number

### Property Information

- Property type
- Number of bedrooms
- Location
- Budget
- Buy or rent

### Customer Intent

- Buying
- Renting
- Selling
- Land
- Property enquiry

### Timeline

- Immediately
- Within 1 month
- Within 3 months
- Within 6 months
- Researching

The system does not need to collect everything in one message.

It should collect information progressively.

---

# 8. Lead Qualification

Each lead should receive a score between:

```text
0 - 100
```

The score helps determine how much attention a lead should receive.

### Lead Classification

```text
HOT
WARM
COLD
UNQUALIFIED
```

Example:

```text
Lead Score: 88
Classification: HOT
```

A hot lead may trigger an immediate notification to the sales team.

A cold lead may be placed into a normal follow-up or nurturing process.

---

# 9. Lead Status

The system may use the following statuses:

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

These statuses represent the customer's journey through the sales process.

---

# 10. Project Structure

The project can initially use:

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
│   ├── PRD.md
│   ├── database/
│   │   └── DATABASE_DESIGN.md
│   ├── api/
│   │   └── API_SPEC.md
│   ├── automation/
│   │   └── N8N_WORKFLOW_SPEC.md
│   ├── ai/
│   │   └── AI_SPEC.md
│   └── frontend/
│       └── UI_UX_SPEC.md
│
└── README.md
```

The structure can change if development reveals a better organization.

---

# 11. Documentation Structure

The project documentation should remain simple.

### PRD

Defines:

- What we are building.
- Why we are building it.
- Who will use it.
- What the system should accomplish.

### Database Design

Defines:

- Tables.
- Fields.
- Relationships.
- Data types.
- Database rules.

### API Specification

Defines:

- Endpoints.
- Requests.
- Responses.
- Authentication.
- API responsibilities.

### n8n Workflow Specification

Defines:

- Workflows.
- Triggers.
- Nodes.
- Automation logic.
- AI processing.
- Notifications.

### AI Specification

Defines:

- What AI should understand.
- What AI should extract.
- AI response behavior.
- AI limitations.

### UI/UX Specification

Defines:

- Screens.
- Components.
- User interactions.
- Dashboard behavior.
- Customer chat experience.

---

# 12. Development Principle

The project should follow one simple rule:

> **Use the simplest technology that correctly solves the problem.**

Do not introduce additional tools just because they are available.

For example:

- Use FastAPI for application/API logic.
- Use n8n for automation and integrations.
- Use AI where natural-language understanding is needed.
- Use PostgreSQL for persistent data.
- Use React for the interface.

Avoid unnecessary microservices, complicated infrastructure, or additional technologies unless the project actually needs them.

---

# 13. Development Approach

Development should happen in small, understandable stages.

### Phase 1 — Foundation

Set up:

- Repository.
- React application.
- FastAPI application.
- PostgreSQL.
- n8n.
- Environment configuration.

### Phase 2 — Database

Implement:

- Users.
- Leads.
- Conversations.
- Messages.
- Scores.
- Follow-ups.
- Activities.

### Phase 3 — Backend

Implement the main APIs:

```text
POST /api/v1/leads
GET /api/v1/leads
GET /api/v1/leads/{id}
PATCH /api/v1/leads/{id}

POST /api/v1/conversations
GET /api/v1/conversations/{id}

POST /api/v1/messages
```

Exact endpoints should follow the API specification.

### Phase 4 — Customer Interface

Build:

- Chat interface.
- Message input.
- Message history.
- Loading states.
- Error handling.
- Basic lead information collection.

### Phase 5 — n8n

Build the main workflow:

```text
Message
 ↓
Receive
 ↓
Validate
 ↓
AI Extraction
 ↓
Check Missing Information
 ↓
Qualify
 ↓
Store
 ↓
Respond
 ↓
Notify Sales
```

### Phase 6 — AI

Implement:

- Intent detection.
- Requirement extraction.
- Lead qualification support.
- Response generation.
- Conversation summarization.

### Phase 7 — Sales Dashboard

Build:

- Lead list.
- Search.
- Filters.
- Lead details.
- Conversation history.
- Score.
- Status.
- Assignment.
- Follow-ups.

### Phase 8 — Testing

Test:

- Normal enquiries.
- Incomplete enquiries.
- Multiple messages.
- Invalid information.
- Duplicate messages.
- AI failures.
- API failures.
- n8n failures.
- Notification failures.

---

# 14. Agentic Development Rules

When using an AI coding assistant, it should follow these rules.

### Rule 1 — Read the documentation first

Before changing code, inspect the relevant project documentation.

### Rule 2 — Do not invent architecture

Do not introduce new services, databases, frameworks, or workflows without a reason.

### Rule 3 — Follow existing contracts

If an API, database model, or workflow is already defined, follow it.

### Rule 4 — Keep changes focused

Avoid changing unrelated parts of the application.

### Rule 5 — Explain architectural changes

If a change requires modifying the architecture, explain why before implementing it.

### Rule 6 — Validate after changes

Run the appropriate tests or checks after implementation.

### Rule 7 — Prefer simple solutions

Do not over-engineer the MVP.

---

# 15. MVP Definition

The first usable version should be able to:

```text
Customer
   ↓
Send Message
   ↓
System Understands Message
   ↓
Extracts Information
   ↓
Stores Lead
   ↓
Scores Lead
   ↓
Responds
   ↓
Alerts Sales Team
```

The MVP does **not** need to contain every possible real estate feature.

Features such as advanced property matching, marketing campaigns, sophisticated analytics, mobile applications, and complex CRM functionality can be added later.

---

# 16. Success Criteria

The project is successful when a customer can send a natural-language real estate enquiry and the system can reliably:

- Receive the message.
- Understand the request.
- Extract useful information.
- Ask for missing information when necessary.
- Create or update the lead.
- Score and classify the lead.
- Store the conversation.
- Respond to the customer.
- Alert the appropriate sales team member when required.
- Support follow-up.

---

# 17. Final Architecture Principle

The system should remain understandable:

```text
             CUSTOMER
                 │
                 ▼
              REACT
                 │
                 ▼
             FASTAPI
              /    \
             /      \
            ▼        ▼
      POSTGRESQL    N8N
                     │
              ┌──────┼──────┐
              ▼      ▼      ▼
             AI  NOTIFY  SHEETS
```

The most important separation is:

```text
React
→ User Interface

FastAPI
→ Application/API

n8n
→ Automation

AI
→ Understanding & Generation

PostgreSQL
→ Data

Google Sheets
→ Operational Reporting
```

Keep the system simple, modular, and easy to maintain.