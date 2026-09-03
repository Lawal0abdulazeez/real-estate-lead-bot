# Documentation

All project specifications and trackers live under `docs/`.

## Core documents (current in this folder)

| Document | Purpose |
|----------|--------|
| [DEVELOPMENT_SETUP.md](./DEVELOPMENT_SETUP.md) | Local setup & implementation guide |
| [IMPLEMENTATION.md](./IMPLEMENTATION.md) | Engineering progress log (updated for foundation) |
| [TASK.md](./TASK.md) | Task tracker (updated for foundation) |
| [AI Specification.md](./AI%20Specification.md) | AI behaviour (stub — restore full from history if needed) |
| [API Specification.md](./API%20Specification.md) | API contracts (stub — restore full from history if needed) |

## Full original specifications

The complete original specification files were moved out of the repository root for a cleaner structure.

**Full content is preserved in git history** at commit `85cdb7f61bdc157fc0a370fc6fae874f8f7e1811`.

Restore any file with:

```bash
git show 85cdb7f61bdc157fc0a370fc6fae874f8f7e1811:"AI Specification.md" > "docs/AI Specification.md"
git show 85cdb7f61bdc157fc0a370fc6fae874f8f7e1811:"API Specification.md" > "docs/API Specification.md"
git show 85cdb7f61bdc157fc0a370fc6fae874f8f7e1811:"DEPLOYMENT_SPEC.md" > "docs/DEPLOYMENT_SPEC.md"
git show 85cdb7f61bdc157fc0a370fc6fae874f8f7e1811:"Database & Data Model Specification.md" > "docs/Database & Data Model Specification.md"
git show 85cdb7f61bdc157fc0a370fc6fae874f8f7e1811:"LEAD_QUALIFICATION_SPEC.md" > "docs/LEAD_QUALIFICATION_SPEC.md"
git show 85cdb7f61bdc157fc0a370fc6fae874f8f7e1811:"PRD.md" > "docs/PRD.md"
git show 85cdb7f61bdc157fc0a370fc6fae874f8f7e1811:"System Architecture Document (SAD).md" > "docs/System Architecture Document (SAD).md"
git show 85cdb7f61bdc157fc0a370fc6fae874f8f7e1811:"TESTING_SPEC.md" > "docs/TESTING_SPEC.md"
git show 85cdb7f61bdc157fc0a370fc6fae874f8f7e1811:"UI-UX Specification.md" > "docs/UI-UX Specification.md"
git show 85cdb7f61bdc157fc0a370fc6fae874f8f7e1811:"n8n Workflow Specification.md" > "docs/n8n Workflow Specification.md"
```

Or browse that commit on GitHub.

## Reading order for AI coding agents

1. Root `README.md`
2. `docs/IMPLEMENTATION.md` / `docs/TASK.md`
3. Relevant specification for the current task
4. Make the smallest change that satisfies the task
5. Update `IMPLEMENTATION.md` and `TASK.md`
