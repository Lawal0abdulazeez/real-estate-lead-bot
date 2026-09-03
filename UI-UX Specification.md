# UI/UX Specification

## PrimeHomes Realty — Real Estate Lead Bot

**Document:** UI/UX Specification  
**Version:** 1.0  
**Status:** Draft  
**Frontend:** React  
**Backend:** FastAPI  
**Automation:** n8n  
**Database:** PostgreSQL

---

# 1. Purpose

This document defines the user interface and user experience requirements for the PrimeHomes Realty Real Estate Lead Bot.

The frontend should provide a simple and professional experience for:

1. Potential customers interacting with the lead bot.
2. Sales agents managing leads.
3. Managers monitoring lead activity.
4. Administrators managing the system.

The frontend must remain focused on presentation and user interaction.

Business rules, authorization, data persistence, lead scoring, and automation remain backend responsibilities.

---

# 2. UI Architecture

```text
CUSTOMER
   │
   ▼
React Customer Interface
   │
   ▼
FastAPI
   │
   ├── PostgreSQL
   │
   └── n8n
        │
        ├── AI
        ├── Notifications
        └── Integrations
```

For internal users:

```text
SALES AGENT / MANAGER
          │
          ▼
React Dashboard
          │
          ▼
       FastAPI
          │
          ▼
      PostgreSQL
```

---

# 3. Design Principles

The UI should follow these principles:

### Simple

Users should understand what to do without extensive instructions.

### Fast

Important information should appear quickly.

### Responsive

The application should work across:

- Desktop.
- Tablet.
- Mobile.

### Accessible

The interface should consider:

- Keyboard navigation.
- Readable typography.
- Sufficient contrast.
- Clear labels.
- Visible focus states.
- Screen-reader-friendly controls.

### Consistent

Buttons, forms, cards, status indicators, spacing, and typography should behave consistently throughout the application.

---

# 4. User Types

Initial user roles:

```text
CUSTOMER
SALES_AGENT
MANAGER
ADMIN
```

---

# 5. Customer Experience

The customer-facing experience should be the simplest part of the application.

Primary objective:

> Allow a potential customer to communicate their real-estate needs naturally without feeling like they are completing a complicated form.

---

# 6. Customer Entry Points

The MVP may support:

```text
Chat interface
Lead enquiry form
```

Future integrations may include:

```text
WhatsApp
Telegram
Website widget
Facebook Messenger
Instagram
SMS
```

The UI architecture should avoid tightly coupling the frontend to one messaging platform.

---

# 7. Customer Chat Interface

Primary screen:

```text
┌─────────────────────────────────────────┐
│ PrimeHomes Realty                       │
│ Real Estate Assistant                  │
├─────────────────────────────────────────┤
│                                         │
│ Bot: Hi! How can we help you today?    │
│                                         │
│             Customer:                  │
│     I need a 3-bedroom apartment       │
│     around Lekki.                      │
│                                         │
│ Bot: Great! What's your budget range?  │
│                                         │
├─────────────────────────────────────────┤
│ Type your message...              Send  │
└─────────────────────────────────────────┘
```

---

# 8. Chat Components

The customer chat should contain:

```text
ChatHeader
ConversationList / MessageList
MessageBubble
TypingIndicator
MessageInput
SendButton
ErrorMessage
ConversationStatus
```

Optional:

```text
QuickReplyButtons
AttachmentButton
ContactInformationForm
```

---

# 9. Message Bubble

Customer messages:

```text
Customer
                    ┌───────────────────┐
                    │ I need a house    │
                    │ around Lekki.     │
                    └───────────────────┘
```

Bot messages:

```text
┌────────────────────────────────────┐
│ Sure! Are you looking to buy or    │
│ rent?                              │
└────────────────────────────────────┘
PrimeHomes Assistant
```

---

# 10. Message States

Each message may have:

```text
SENDING
SENT
PROCESSING
DELIVERED
FAILED
```

The user should receive clear feedback when something goes wrong.

Example:

```text
Message failed to send.
[Retry]
```

---

# 11. Typing State

While the bot is processing:

```text
PrimeHomes Assistant
● ● ●
```

The typing indicator should disappear when the response arrives.

It should also have a timeout/fallback state if the backend does not respond.

---

# 12. Customer Conversation Flow

Typical flow:

```text
Customer opens chat
        ↓
Bot greeting
        ↓
Customer sends enquiry
        ↓
Message appears immediately
        ↓
Loading / typing state
        ↓
Backend processes message
        ↓
Bot response
        ↓
Customer continues conversation
```

---

# 13. Progressive Lead Collection

The UI should not force customers to complete a large form immediately.

Example:

```text
Customer:
I need a 3-bedroom apartment in Lekki.

Bot:
Sure. What's your budget range?
```

Later:

```text
Bot:
And when are you hoping to purchase?
```

This creates a conversational experience.

---

# 14. Lead Form

A structured lead form may be used when appropriate.

Fields:

```text
Name
Email
Phone
Property Type
Bedrooms
Location
Budget
Buy / Rent
Timeline
```

---

# 15. Lead Form Design

Example:

```text
┌──────────────────────────────────────────┐
│ Tell us what you're looking for          │
│                                          │
│ Full Name                                │
│ [____________________________]           │
│                                          │
│ Phone Number                             │
│ [____________________________]           │
│                                          │
│ Property Type                            │
│ [ Apartment ▼ ]                          │
│                                          │
│ Location                                 │
│ [____________________________]           │
│                                          │
│ Budget                                   │
│ [____________________________]           │
│                                          │
│ [ Continue ]                             │
└──────────────────────────────────────────┘
```

---

# 16. Form Validation

Frontend validation should improve user experience.

Examples:

```text
Invalid email
Invalid phone number
Required field missing
Invalid number
```

However:

> Frontend validation is not a security boundary.

FastAPI must validate all submitted data again.

---

# 17. Dashboard Overview

Internal users should have access to a dashboard.

Example:

```text
┌──────────────────────────────────────────────────────┐
│ PrimeHomes Realty                         User ▼     │
├────────────┬─────────────────────────────────────────┤
│ Dashboard  │                                         │
│ Leads      │  Total Leads       248                  │
│ Follow-ups │  New Leads          32                  │
│ Activities │  Hot Leads          14                  │
│ Settings   │  Converted          21                  │
│            │                                         │
│            │  Recent Leads                           │
│            │  ───────────────────────────────────    │
│            │  John Doe       HOT       Lekki         │
│            │  Jane Smith     WARM      Ikeja         │
│            │  Mike Adams     COLD      Ibadan        │
└────────────┴─────────────────────────────────────────┘
```

---

# 18. Dashboard Metrics

Initial metrics:

```text
Total Leads
New Leads
Hot Leads
Warm Leads
Cold Leads
Qualified Leads
Assigned Leads
Converted Leads
Follow-ups Due
```

Future metrics:

```text
Conversion Rate
Average Lead Score
Average Response Time
Lead Sources
Agent Performance
```

---

# 19. Lead List

The lead-management page should provide:

```text
Search
Filters
Sorting
Pagination
Status
Classification
Assigned Agent
Location
Property Type
Date Range
```

Example:

```text
┌──────────────────────────────────────────────────────────────┐
│ Leads                                                        │
│                                                              │
│ Search: [ Lekki________________ ] [Filter ▼] [Sort ▼]       │
│                                                              │
│ Name       Property      Location   Score   Status           │
│ John Doe   3 Bed Apt     Lekki       87     HOT             │
│ Jane Smith 2 Bed Apt     Ikeja       72     WARM            │
│ Mike Adams Land          Ibadan      41     COLD            │
└──────────────────────────────────────────────────────────────┘
```

---

# 20. Lead Classification UI

Use visually distinct status indicators.

Example:

```text
HOT
WARM
COLD
UNQUALIFIED
```

The exact colors should follow the application's design system.

Do not rely on color alone.

Example:

```text
🔥 HOT
● WARM
○ COLD
— UNQUALIFIED
```

Icons and text should reinforce the classification.

---

# 21. Lead Details Page

The lead details screen should show:

```text
Customer Information
Property Requirements
Lead Score
Lead Classification
Lead Status
Conversation
Assigned Agent
Follow-ups
Activity History
```

Example:

```text
┌─────────────────────────────────────────────┐
│ John Doe                         HOT        │
│ Score: 87                                  │
├─────────────────────────────────────────────┤
│ Customer                                    │
│ Phone: +234...                              │
│ Email: john@example.com                     │
│                                             │
│ Requirements                                │
│ 3-bedroom apartment                         │
│ Lekki                                       │
│ ₦80M                                        │
│ Buy                                         │
│ Within 3 months                             │
├─────────────────────────────────────────────┤
│ Conversation                                │
│                                             │
│ Customer: ...                               │
│ Bot: ...                                    │
└─────────────────────────────────────────────┘
```

---

# 22. Lead Score Display

The lead score should be visible but not overwhelming.

Example:

```text
Lead Score

87 / 100
█████████████████░░░
HOT
```

The score should be retrieved from the backend.

The frontend must never calculate the official lead score.

---

# 23. Lead Status

Possible statuses:

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

The UI should only allow transitions permitted by the backend.

---

# 24. Lead Assignment

Sales agents or managers should be able to see:

```text
Assigned Agent
Assignment Date
Assignment Status
```

Managers may have controls to assign or reassign leads.

Authorization must be enforced by FastAPI.

---

# 25. Conversation View

Sales agents should be able to review the customer conversation.

Example:

```text
Customer:
I'm looking for a 3-bedroom apartment in Lekki.

Bot:
What's your budget?

Customer:
Around ₦80 million.

Bot:
When are you hoping to buy?

Customer:
Within two months.
```

The conversation should be chronological.

---

# 26. Conversation Context

The sales agent should also see a structured summary.

Example:

```text
AI Summary

Customer wants to buy a 3-bedroom apartment around
Lekki with an approximate budget of ₦80M.

Timeline:
Within 3 months

Missing:
None
```

The summary is assistance only.

The original conversation remains available for verification.

---

# 27. Follow-Up Interface

The follow-up screen should show:

```text
Upcoming
Due
Completed
Overdue
Cancelled
```

Example:

```text
┌────────────────────────────────────────────────────┐
│ Follow-ups                                         │
├────────────────────────────────────────────────────┤
│ 🔴 Due      John Doe       Today     Contact      │
│ 🟠 Upcoming Jane Smith     Tomorrow  Call         │
│ 🟢 Done     Mike Adams     Yesterday WhatsApp     │
└────────────────────────────────────────────────────┘
```

---

# 28. Follow-Up Creation

Users with appropriate permissions may create a follow-up.

Fields:

```text
Lead
Date
Time
Type
Note
Assigned User
```

Types:

```text
CALL
EMAIL
MESSAGE
VIEWING
OTHER
```

---

# 29. Activity Timeline

The lead page should contain an activity timeline.

Example:

```text
Today
│
├── 10:30 Customer sent message
├── 10:31 AI extracted requirements
├── 10:31 Lead scored 87
├── 10:31 Classified as HOT
├── 10:32 Assigned to Sarah
└── 10:33 Sales notification sent
```

---

# 30. Loading States

Every asynchronous operation should have a loading state.

Examples:

```text
Loading leads...
Loading conversation...
Saving...
Assigning...
Sending...
```

Avoid blank screens during loading.

---

# 31. Skeleton Loading

For larger dashboard sections, use skeleton loaders rather than blocking the entire application.

Example:

```text
┌──────────────────────────┐
│ █████████████████        │
│ ███████████              │
│ ███████████████████      │
└──────────────────────────┘
```

---

# 32. Error States

Errors should be understandable.

Bad:

```text
500 Internal Server Error
```

Better:

```text
We couldn't load the leads right now.

Please try again.

[Retry]
```

Technical details may still be logged for developers.

---

# 33. Empty States

When no leads exist:

```text
No leads yet.

New customer enquiries will appear here.
```

When a search returns nothing:

```text
No leads match your search.

Try changing your filters.
```

---

# 34. Offline / Network Failure

If the customer loses connectivity:

```text
Connection lost.

Your message may not have been sent.

[Retry]
```

The UI should not falsely display a message as successfully delivered.

---

# 35. Authentication UI

Internal users should have:

```text
Login
Logout
Session handling
Protected routes
```

Example:

```text
Email
[________________________]

Password
[________________________]

[ Sign In ]
```

---

# 36. Authorization

The frontend may hide controls that the user cannot use.

However:

> Hiding a button is not authorization.

FastAPI must independently enforce permissions.

---

# 37. Role-Based UI

### Sales Agent

Can generally:

```text
View assigned leads
View conversations
Update permitted lead information
Create follow-ups
Update permitted statuses
```

### Manager

May additionally:

```text
View team leads
Assign leads
Reassign leads
View team metrics
```

### Admin

May additionally:

```text
Manage users
Manage roles
Manage configuration
View system-level information
```

The exact permissions are defined by backend authorization.

---

# 38. Navigation

Recommended navigation:

```text
Dashboard
Leads
Follow-ups
Activities
Reports
Settings
```

Customer-facing users should not see internal navigation.

---

# 39. Responsive Layout

Desktop:

```text
Sidebar + Main Content
```

Tablet:

```text
Collapsible Sidebar + Main Content
```

Mobile:

```text
Top Bar
Main Content
Bottom/Drawer Navigation where appropriate
```

The lead-management tables should transform appropriately on small screens rather than simply overflowing.

---

# 40. Mobile Lead Card

Instead of a wide table:

```text
┌─────────────────────────────┐
│ John Doe             HOT    │
│ 3-bedroom Apartment         │
│ Lekki                       │
│ ₦80M                        │
│ Score: 87                   │
│                             │
│ [View Lead]                 │
└─────────────────────────────┘
```

---

# 41. Design System

Create reusable UI primitives.

Suggested components:

```text
Button
Input
Select
Textarea
Modal
Drawer
Card
Badge
Table
Pagination
Dropdown
Toast
Alert
Tabs
Avatar
Skeleton
Tooltip
```

Avoid building separate versions of the same component for every page.

---

# 42. Component Architecture

Suggested React structure:

```text
frontend/
└── src/
    ├── components/
    │   ├── ui/
    │   ├── chat/
    │   ├── leads/
    │   ├── followups/
    │   └── dashboard/
    │
    ├── pages/
    │   ├── customer/
    │   ├── auth/
    │   └── dashboard/
    │
    ├── layouts/
    ├── hooks/
    ├── services/
    ├── stores/
    ├── types/
    ├── utils/
    └── app/
```

The exact structure may evolve.

---

# 43. API Communication

The frontend communicates with FastAPI.

```text
React
  ↓
API Client
  ↓
FastAPI
```

Avoid putting raw `fetch()` calls throughout individual components.

Prefer a centralized API layer.

Example:

```text
services/
    authService
    leadService
    conversationService
    followupService
```

---

# 44. API Client

The frontend should have a consistent API client responsible for:

```text
Base URL
Authentication
Headers
Request IDs
Error handling
Timeouts
Response parsing
```

---

# 45. State Management

Use local component state when possible.

Use shared state only where necessary.

Examples of shared state:

```text
Authenticated user
Session
Global notifications
Conversation state
Application preferences
```

Do not put every API response into a global store.

---

# 46. Server State

Server-owned data should preferably use a server-state/query pattern.

Examples:

```text
Leads
Lead details
Follow-ups
Activities
Dashboard metrics
```

This allows:

```text
Caching
Refetching
Invalidation
Loading states
Error states
```

---

# 47. Optimistic Updates

Use optimistic updates carefully.

Good candidates:

```text
UI-only preferences
Simple reversible interactions
```

Be cautious with:

```text
Lead status
Lead assignment
Customer information
```

because these affect business data.

---

# 48. Chat Message Handling

When a customer sends a message:

```text
User types
   ↓
Frontend validation
   ↓
POST message
   ↓
Show sending state
   ↓
Backend accepts
   ↓
n8n processes
   ↓
Bot response
   ↓
Update conversation
```

---

# 49. Prevent Duplicate Sends

Disable or protect the send operation while the same message is being submitted.

The backend should also support idempotency.

Frontend protection alone is insufficient.

---

# 50. Customer Session

The customer conversation should have a stable conversation identifier.

Example:

```text
conversation_id
```

This allows the backend to associate messages with the correct conversation.

---

# 51. Browser Storage

Only non-sensitive state should be stored in browser storage.

Avoid storing:

```text
Passwords
API secrets
Long-lived sensitive credentials
```

Authentication strategy should be selected together with the backend security design.

---

# 52. Notifications

The frontend may display:

```text
Success
Warning
Error
Information
```

Example:

```text
✓ Lead updated successfully.
```

Notifications should not replace proper page-level error states.

---

# 53. Accessibility

The application should support:

```text
Keyboard navigation
Visible focus states
Semantic HTML
Accessible form labels
ARIA where appropriate
Screen-reader-friendly status messages
Readable text
```

Interactive controls should be usable without a mouse.

---

# 54. Forms

Every form should have:

```text
Label
Input
Validation
Error message
Loading state
Submit action
Success state
```

Avoid relying on placeholders as the only field labels.

---

# 55. Confirmation Dialogs

Confirmation should be required for destructive or consequential actions.

Example:

```text
Delete this lead?

This action cannot be easily undone.

[Cancel] [Delete]
```

The frontend should only present actions the backend permits.

---

# 56. Search

Lead search should support:

```text
Name
Phone
Email
Location
Lead ID
```

Search should be server-side for large datasets.

Avoid downloading thousands of leads to the browser just to filter them.

---

# 57. Filtering

Useful filters:

```text
Classification
Status
Property Type
Transaction Type
Location
Assigned Agent
Date Created
Date Updated
```

---

# 58. Pagination

Lead lists should use server-side pagination.

Example:

```text
Showing 1–25 of 248

[Previous] 1 2 3 4 ... 10 [Next]
```

---

# 59. Sorting

Possible sorting:

```text
Newest
Oldest
Highest Score
Lowest Score
Recently Updated
Follow-up Due
```

Sorting should be performed by the backend where datasets are large.

---

# 60. Dashboard Data Freshness

Dashboard data may be refreshed:

```text
On page load
On user refresh
After relevant mutation
Periodically where appropriate
```

Do not refresh excessively.

---

# 61. Security Considerations

The frontend must:

- Use HTTPS in production.
- Avoid exposing secrets.
- Respect authentication state.
- Avoid trusting client-provided roles.
- Avoid rendering unsafe HTML.
- Validate user input for UX.
- Handle expired sessions gracefully.

---

# 62. XSS Prevention

Customer messages are untrusted content.

Do not render customer-generated HTML directly.

Preferred:

```text
Plain text
```

unless sanitized rendering is deliberately implemented.

---

# 63. Error Boundary

The React application should use error boundaries to prevent a component failure from crashing the entire application.

Example:

```text
Something went wrong.

[Reload]
```

Developers should still receive useful diagnostic information through logging.

---

# 64. Performance

Initial priorities:

```text
Fast initial load
Small bundles
Lazy-loaded dashboard pages
Efficient API calls
Pagination
Avoid unnecessary rerenders
Optimized images
```

Do not prematurely optimize every component.

Measure before making complex optimizations.

---

# 65. Frontend Logging

Development logging may include:

```text
API errors
Navigation errors
Component failures
```

Production logging should avoid exposing:

```text
Passwords
Tokens
Sensitive customer information
```

---

# 66. Customer UX Principles

The bot should make the customer feel:

```text
Heard
Understood
Guided
Not pressured
```

Avoid excessive questioning.

Example:

```text
Good:
What's your budget range?

Bad:
Please provide your exact budget, preferred property,
bedrooms, location, timeline, email, phone number,
full name and transaction type.
```

---

# 67. Sales UX Principles

Sales agents should be able to answer these questions quickly:

```text
Who is this customer?
What do they want?
Where do they want it?
What is their budget?
How urgent are they?
What is their lead score?
Who is handling them?
What happened previously?
What should I do next?
```

If the dashboard cannot answer these questions quickly, the interface should be reconsidered.

---

# 68. Customer-to-Sales Handoff

When a lead requires human intervention:

```text
Customer
   ↓
Bot detects handoff
   ↓
FastAPI updates conversation state
   ↓
n8n notifies sales
   ↓
Sales agent opens lead
   ↓
Agent reviews summary + conversation
   ↓
Agent continues follow-up
```

---

# 69. Real-Time Updates

Real-time communication may be introduced later.

Possible technologies:

```text
WebSocket
Server-Sent Events
Polling
```

MVP may use polling or request-based updates if real-time infrastructure is unnecessary.

Do not introduce WebSockets merely because the application is chat-based.

---

# 70. Frontend Testing

Tests should include:

### Component Tests

```text
Buttons
Forms
Message bubbles
Lead cards
Filters
```

### Page Tests

```text
Login
Chat
Lead list
Lead details
Dashboard
Follow-ups
```

### Integration Tests

```text
React → FastAPI
Authentication
Lead creation
Message submission
Lead updates
```

### End-to-End Tests

Example:

```text
Customer sends enquiry
       ↓
Lead created
       ↓
AI processes message
       ↓
Lead updated
       ↓
Bot response appears
```

---

# 71. Important UI Test Cases

Test:

```text
Empty state
Loading state
Success state
API failure
Network failure
Invalid form
Expired session
Unauthorized action
Duplicate submission
Long message
Very long customer name
Large lead list
Mobile layout
```

---

# 72. Definition of Done

The MVP frontend is complete when:

- [ ] Customer chat interface works.
- [ ] Customer lead form works.
- [ ] Internal login works.
- [ ] Protected routes exist.
- [ ] Dashboard exists.
- [ ] Lead list exists.
- [ ] Lead filtering exists.
- [ ] Lead search exists.
- [ ] Lead details page exists.
- [ ] Conversation history is visible.
- [ ] Lead score is displayed.
- [ ] Lead classification is displayed.
- [ ] Lead status is displayed.
- [ ] Follow-ups are visible.
- [ ] Activity timeline exists.
- [ ] Loading states exist.
- [ ] Error states exist.
- [ ] Empty states exist.
- [ ] Responsive layouts exist.
- [ ] Accessibility basics are implemented.
- [ ] API communication is centralized.
- [ ] Frontend does not contain core business rules.
- [ ] Frontend does not directly access PostgreSQL.
- [ ] Frontend does not contain secrets.
- [ ] Component tests exist.
- [ ] End-to-end critical paths are tested.

---

# 73. Frontend Architectural Rule

The frontend should follow:

```text
React
   │
   ├── Presentation
   ├── Interaction
   ├── Client State
   └── API Consumption
          │
          ▼
       FastAPI
```

The frontend should **not** become:

```text
React
   ↓
Business Logic
   ↓
Database
```

---

# 74. Final UI Architecture

```text
                         REACT APPLICATION
                                │
             ┌──────────────────┼──────────────────┐
             │                  │                  │
             ▼                  ▼                  ▼
       CUSTOMER UI         SALES DASHBOARD     ADMIN UI
             │                  │                  │
             └──────────────────┼──────────────────┘
                                ▼
                           API CLIENT
                                │
                                ▼
                             FASTAPI
                                │
              ┌─────────────────┼─────────────────┐
              │                 │                 │
              ▼                 ▼                 ▼
          PostgreSQL           n8n             Auth
                                │
                    ┌───────────┼───────────┐
                    ▼           ▼           ▼
                   AI      Notifications  Sheets
```

---

# 75. Final UX Principle

The PrimeHomes Realty frontend should make the complex system feel simple.

For the customer:

```text
Send message
      ↓
Get understood
      ↓
Answer a few useful questions
      ↓
Get connected to the right person
```

For the sales agent:

```text
Open lead
    ↓
Understand customer
    ↓
See priority
    ↓
Review conversation
    ↓
Take action
```

For the manager:

```text
See pipeline
    ↓
Identify opportunities
    ↓
Monitor follow-ups
    ↓
Improve team performance
```

The frontend should expose the value of the automation without exposing the underlying complexity of AI, n8n, APIs, or database operations to the end user.