# LEAD_QUALIFICATION_SPEC.md

# Real Estate Lead Bot — Lead Qualification & Scoring

## 1. Purpose

This document defines how the Real Estate Lead Bot should qualify incoming real estate leads.

The objective is simple:

> Determine how ready and valuable a customer appears to be so the sales team knows which leads deserve the most immediate attention.

The qualification system should be:

- Simple.
- Understandable.
- Consistent.
- Easy to modify.
- Easy to explain to the sales team.

The system should not attempt to predict customer behavior perfectly.

---

# 2. Qualification Flow

The basic process is:

```text
Customer Message
      ↓
Extract Information
      ↓
Check Available Information
      ↓
Qualification Rules
      ↓
Calculate Score
      ↓
Classify Lead
      ↓
Take Action
```

Example:

```text
Score: 87
Classification: HOT
Action: Notify Sales Team
```

---

# 3. Lead Classification

The system uses four main classifications.

| Score | Classification |
|---:|---|
| 80–100 | HOT |
| 60–79 | WARM |
| 30–59 | COLD |
| 0–29 | UNQUALIFIED |

These thresholds can be adjusted later based on real business results.

---

# 4. What Makes a Good Lead?

The system should consider a few simple factors.

### 1. Clear Intent

Does the customer clearly want to:

- Buy?
- Rent?
- Sell?
- Acquire land?

A clear intent is stronger than a general enquiry.

---

### 2. Property Requirement

Does the customer know what they want?

For example:

```text
3-bedroom apartment
```

is more useful than:

```text
I need a property.
```

---

### 3. Location

A specific location provides more useful information.

Example:

```text
Lekki Phase 1
```

is more actionable than:

```text
Somewhere in Lagos.
```

---

### 4. Budget

A stated budget is an important qualification signal.

Example:

```text
My budget is ₦80 million.
```

is more actionable than:

```text
I don't know my budget yet.
```

---

### 5. Timeline

Customers who intend to make a decision soon should generally receive more attention.

Examples:

```text
I want to buy this month.
```

```text
I'm planning to buy within three months.
```

```text
I'm just researching for now.
```

---

### 6. Contact Information

A lead with usable contact information is easier for the sales team to follow up.

Useful information includes:

- Name.
- Phone number.
- Email.

---

# 5. Initial Scoring Model

The MVP can use a simple point-based system.

## Intent — Maximum 20 Points

| Condition | Points |
|---|---:|
| Clear BUY/RENT/SELL/LAND intent | +20 |
| General property enquiry | +10 |
| Unknown intent | +0 |

---

## Property Requirement — Maximum 15 Points

| Condition | Points |
|---|---:|
| Specific property type | +10 |
| Specific bedrooms/size requirement | +5 |
| No clear property requirement | +0 |

---

## Location — Maximum 15 Points

| Condition | Points |
|---|---:|
| Specific location | +15 |
| General area/region | +8 |
| No location | +0 |

---

## Budget — Maximum 20 Points

| Condition | Points |
|---|---:|
| Clear budget/range | +20 |
| Approximate budget | +10 |
| No budget information | +0 |

The system should not assume that a customer is wealthy or unqualified simply because their budget is high or low.

The budget should primarily measure **how actionable the enquiry is**.

---

## Timeline — Maximum 20 Points

| Timeline | Points |
|---|---:|
| Immediate | +20 |
| Within 1 month | +18 |
| Within 3 months | +15 |
| Within 6 months | +10 |
| Researching | +5 |
| Unknown | +0 |

---

## Contact Information — Maximum 10 Points

| Condition | Points |
|---|---:|
| Phone available | +5 |
| Email available | +3 |
| Name available | +2 |

---

# 6. Maximum Score

The maximum possible score is:

```text
20 + 15 + 15 + 20 + 20 + 10 = 100
```

Therefore:

```text
Lead Score = 0–100
```

---

# 7. Example Qualification

Customer message:

```text
Hi, I'm looking for a 3-bedroom apartment around Lekki.
My budget is around ₦80 million and I want to buy within
the next two months. My name is John and my phone number is
080XXXXXXXX.
```

The system could calculate:

```text
Intent
BUY = +20

Property
Apartment + 3 bedrooms = +15

Location
Lekki = +15

Budget
₦80 million = +20

Timeline
Within 3 months = +15

Contact
Phone + name = +7
```

Total:

```text
92 / 100
```

Classification:

```text
HOT
```

Action:

```text
Notify Sales Team
```

---

# 8. Another Example

Customer:

```text
Hello, I want to buy a house someday.
```

Possible score:

```text
Intent = +20
Property = +0
Location = +0
Budget = +0
Timeline = +5
Contact = +0

Total = 25
```

Classification:

```text
UNQUALIFIED
```

The bot should not reject the customer.

Instead, it should continue the conversation and collect useful information.

---

# 9. Qualification Is Not Customer Rejection

This is important.

A low score does **not** mean:

```text
Customer is bad.
```

It means:

```text
There is currently not enough information or urgency
to prioritize this lead.
```

The customer can become a HOT lead later.

For example:

```text
First message
→ Score: 25

Customer provides budget
→ Score: 45

Customer provides location and property type
→ Score: 70

Customer confirms purchase within one month
→ Score: 88
```

The score should therefore be recalculated when important information changes.

---

# 10. When To Recalculate

Recalculate the lead score when:

- New customer information is extracted.
- Budget changes.
- Location changes.
- Property requirement changes.
- Timeline changes.
- Intent changes.
- Contact information is added.
- The lead moves through the sales process.

The system should avoid recalculating unnecessarily when nothing relevant has changed.

---

# 11. Lead Classification Actions

## HOT

```text
Score: 80–100
```

Recommended action:

```text
Save Lead
   ↓
Notify Sales Team
   ↓
Mark as Priority
   ↓
Continue Customer Conversation
```

The sales team should be encouraged to follow up quickly.

---

## WARM

```text
Score: 60–79
```

Recommended action:

```text
Save Lead
   ↓
Normal Sales Follow-up
   ↓
Continue Qualification
```

---

## COLD

```text
Score: 30–59
```

Recommended action:

```text
Save Lead
   ↓
Continue Qualification
   ↓
Nurture / Follow-up
```

---

## UNQUALIFIED

```text
Score: 0–29
```

Recommended action:

```text
Save Lead
   ↓
Ask Useful Questions
   ↓
Continue Qualification
```

The system should not automatically discard unqualified leads.

---

# 12. Required Information

The bot should prioritize collecting information that helps the sales team.

The most important fields are:

```text
Intent
Property Type
Location
Budget
Timeline
```

Secondary information:

```text
Name
Phone
Email
Bedrooms
```

The exact priority can be adjusted based on PrimeHomes Realty's sales process.

---

# 13. Progressive Qualification

The bot should not overwhelm customers with a long form.

Instead of asking:

```text
What is your name?
What is your email?
What is your phone?
What property do you want?
How many bedrooms?
Where do you want it?
What is your budget?
When do you want it?
Do you want to buy or rent?
```

The bot should have a natural conversation.

Example:

### Customer

```text
I need an apartment in Lekki.
```

### Bot

```text
Sure. Are you looking to buy or rent, and how many bedrooms
would you like?
```

Then:

### Customer

```text
I want to buy a 3-bedroom.
```

### Bot

```text
Great. What budget range are you working with, and how soon
are you looking to make the purchase?
```

This makes qualification feel like a conversation rather than a questionnaire.

---

# 14. Missing Information

The system should identify missing high-value information.

Example:

```text
Intent: BUY
Property: APARTMENT
Bedrooms: 3
Location: Lekki
Budget: Missing
Timeline: Missing
```

The bot should ask for the most useful missing information.

Example:

```text
Thanks! What budget range are you considering, and are you
looking to purchase immediately or within the next few months?
```

---

# 15. Avoid Asking For Known Information

If the customer already provided information, the bot should not ask for it again.

Example:

Customer:

```text
I want a 3-bedroom apartment in Lekki for ₦80 million.
```

The bot should not ask:

```text
What type of property are you looking for?
```

It already knows.

---

# 16. Score Storage

Every important score change should be stored.

Example:

```json id="w7u9di"
{
  "lead_id": "lead-123",
  "score": 87,
  "classification": "HOT",
  "reason": "Customer has clear purchase intent, budget, location and timeline"
}
```

This creates a history of how the lead changed.

---

# 17. Explainable Scoring

The sales team should be able to understand why a lead received a score.

Example:

```text
Lead Score: 87

Reasons:
✓ Clear purchase intent
✓ Specific property requirement
✓ Specific location
✓ Budget provided
✓ Purchase timeline provided
✓ Phone number available
```

Avoid displaying unexplained AI-generated scores.

The score should be based on identifiable rules.

---

# 18. AI's Role

AI can help extract information from the conversation.

For example:

```text
Customer:
"I need a 3-bed around Lekki, budget is about 80m."
```

AI extracts:

```json id="w4t8f3"
{
  "property_type": "APARTMENT",
  "bedrooms": 3,
  "location": "Lekki",
  "budget_max": 80000000
}
```

The scoring logic should then use these structured values.

The AI should **not invent a final score without the qualification rules being applied**.

---

# 19. Where Qualification Logic Lives

The qualification process should have one clear implementation.

Recommended flow:

```text
AI
 ↓
Extract Structured Information
 ↓
FastAPI / Qualification Service
 ↓
Apply Qualification Rules
 ↓
Calculate Score
 ↓
Store Score
```

n8n can orchestrate this process, but the actual scoring rules should not be duplicated in multiple places.

---

# 20. Handling Uncertain AI Extraction

If AI is uncertain:

```text
Confidence < acceptable threshold
```

the system should not blindly use the information.

Example:

Customer:

```text
I need something around 50-ish.
```

The system should clarify:

```text
Just to confirm, is your budget around ₦50 million?
```

The system should prefer confirmation over guessing.

---

# 21. Important Qualification Rules

### Rule 1

Never invent missing customer information.

### Rule 2

Never assume budget.

### Rule 3

Never assume location.

### Rule 4

Never assume buying or renting.

### Rule 5

Do not permanently classify a customer based on the first message.

### Rule 6

Recalculate when important information changes.

### Rule 7

Keep the scoring rules understandable.

### Rule 8

A low score should not prevent future qualification.

### Rule 9

AI extraction and lead scoring are separate processes.

### Rule 10

Sales staff should be able to understand why a lead received its classification.

---

# 22. Future Improvements

The MVP should use the simple scoring system above.

Later, the system may consider additional signals such as:

- Previous conversations.
- Response frequency.
- Property viewing requests.
- Sales agent interactions.
- Customer engagement.
- Follow-up responses.
- Appointment scheduling.
- Historical conversion data.
- Property availability.
- Lead source.

These should only be introduced when there is enough real-world data to justify them.

---

# 23. Qualification Example Flow

```text
Customer
"I want to buy a house in Lekki."
        ↓
Extract
        ↓
BUY + HOUSE + LEKKI
        ↓
Score
        ↓
45
        ↓
COLD
        ↓
Ask for budget + timeline
        ↓
Customer
"My budget is ₦100m and I want to buy this month."
        ↓
Extract new information
        ↓
Recalculate
        ↓
85
        ↓
HOT
        ↓
Notify Sales
```

---

# 24. Definition of Done

The qualification system is complete when:

- A lead can receive a score from 0–100.
- The score follows documented rules.
- Leads are classified as HOT, WARM, COLD, or UNQUALIFIED.
- Scores can be recalculated.
- Score history can be stored.
- Missing information can trigger further questions.
- AI extraction is separated from scoring.
- Sales staff can understand the reason for a score.
- Low-scoring leads are not automatically discarded.
- Tests cover common qualification scenarios.

---

# 25. Final Principle

The qualification system should answer one simple question:

> **"How much attention should the sales team give this lead right now?"**

It should not pretend to know exactly whether a customer will eventually buy.

Start with simple, explainable rules.

Use real customer data to improve the system later.