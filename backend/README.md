# Backend — FastAPI

PrimeHomes Realty Real Estate Lead Bot API.

## Responsibilities

- REST API (`/api/v1/...`)
- Request validation & authentication
- Business rules and lead/conversation/message management
- Database access (PostgreSQL via SQLAlchemy)
- Boundary to n8n workflows

## Structure

```text
backend/
├── app/
│   ├── main.py
│   ├── api/v1/
│   ├── models/
│   ├── schemas/
│   ├── services/
│   ├── repositories/
│   ├── core/
│   └── db/
├── tests/
├── requirements.txt
└── README.md
```

## Quick start (local)

```bash
cd backend
python -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -r requirements.txt
cp ../.env.example ../.env  # fill values
uvicorn app.main:app --reload --port 8000
```

Health check: `GET http://localhost:8000/api/v1/health`

## Development order (from DEVELOPMENT_SETUP.md)

1. Health endpoint
2. Configuration & DB connection
3. Models + Alembic
4. Lead APIs
5. Conversation & Message APIs
6. Auth
7. Qualification & Follow-ups
