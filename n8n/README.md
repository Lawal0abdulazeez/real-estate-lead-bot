# n8n Workflows

Automation and orchestration layer for the Real Estate Lead Bot.

## Principle

> FastAPI manages the application. n8n manages the workflows.

n8n should not become the source of truth. PostgreSQL remains authoritative.

## Workflows (planned)

| Workflow ID | File | Purpose |
|-------------|------|--------|
| PRH-LEAD-PROCESS-MESSAGE | `workflows/lead-process-message.json` | Main customer message pipeline |
| PRH-LEAD-QUALIFY | `workflows/lead-qualify.json` | Deterministic scoring & classification |
| PRH-LEAD-NOTIFY-SALES | `workflows/lead-notify-sales.json` | HOT lead notifications |
| PRH-FOLLOWUP-REMINDER | `workflows/followup-reminder.json` | Due follow-up reminders |
| PRH-ERROR-HANDLER | `workflows/error-handler.json` | Centralised error handling |

## Local access

With docker-compose: `http://localhost:5678`

Import the JSON files from `workflows/` into the n8n UI when ready.
