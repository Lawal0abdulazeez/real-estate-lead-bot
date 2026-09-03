# Frontend — React

Customer chat interface and sales dashboard for the Real Estate Lead Bot.

## Responsibilities

- Customer chat UI
- Sales dashboard (leads, filters, details, follow-ups)
- Loading / error / retry states
- No direct database access or business-rule calculation

## Recommended structure

```text
frontend/
├── src/
│   ├── components/
│   │   ├── ui/
│   │   ├── chat/
│   │   ├── leads/
│   │   ├── dashboard/
│   │   └── followups/
│   ├── pages/
│   │   ├── customer/
│   │   ├── auth/
│   │   └── dashboard/
│   ├── services/
│   ├── hooks/
│   ├── types/
│   ├── utils/
│   └── app/
├── package.json
└── README.md
```

## Quick start

```bash
cd frontend
npm create vite@latest . -- --template react-ts   # if starting fresh
# or use the existing scaffold once package.json is populated
npm install
npm run dev
```

Default local URL: `http://localhost:5173` (Vite) or `http://localhost:3000`.

Point the API base URL to `http://localhost:8000/api/v1`.
