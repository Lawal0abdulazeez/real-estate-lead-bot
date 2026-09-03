# Database

PostgreSQL is the primary source of truth.

## Primary tables (from Database & Data Model Specification)

- users
- roles
- leads
- conversations
- messages
- lead_scores
- lead_assignments
- follow_ups
- activities
- integration_syncs

## Migration approach

Alembic is used from the backend (`backend/`).

Typical flow:

```bash
cd backend
alembic revision --autogenerate -m "initial schema"
alembic upgrade head
```

This folder may hold:

- Seed scripts
- Reference SQL
- Documentation notes
- Backup helpers

Do not put production credentials here.
