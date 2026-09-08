# DEPLOYMENT_SPEC.md

# Real Estate Lead Bot — VPS Deployment Specification

## 1. Purpose

This document defines how the Real Estate Lead Bot should be deployed to a VPS.

The deployment should be:

- Simple.
- Affordable.
- Easy to maintain.
- Easy to troubleshoot.
- Suitable for an MVP and early production use.
- Easy for an AI coding agent or developer to understand.

The initial deployment should use a single VPS rather than a complicated multi-server architecture.

---

# 2. Deployment Architecture

The initial production architecture is:

```text
                    INTERNET
                       │
                       ▼
                    DOMAIN
                       │
                       ▼
                    NGINX
                       │
          ┌────────────┼────────────┐
          │            │            │
          ▼            ▼            ▼
       React        FastAPI        n8n
          │            │
          │            ▼
          │        PostgreSQL
          │
          └───────────────► FastAPI
```

A more practical Docker-based layout:

```text
VPS
│
├── Nginx
│
├── Frontend
│
├── Backend
│
├── PostgreSQL
│
└── n8n
```

Docker Compose should manage the application containers.

---

# 3. VPS Requirements

For the MVP, a reasonable starting VPS is:

```text
CPU:
2 vCPU

RAM:
4 GB

Storage:
40–80 GB SSD

Operating System:
Ubuntu LTS

Architecture:
64-bit
```

This is a starting point, not a permanent requirement.

The VPS can be upgraded when traffic or workload increases.

---

# 4. Recommended VPS Components

The server should run:

```text
Ubuntu
Docker
Docker Compose
Nginx
Git
```

The application itself should run mainly inside Docker containers.

---

# 5. Production Services

The initial production services are:

```text
nginx
frontend
backend
postgres
n8n
```

Example:

```text id="4ld7v4"
┌─────────────────────────────────────┐
│               VPS                   │
│                                     │
│  ┌─────────┐                        │
│  │  Nginx  │                        │
│  └────┬────┘                        │
│       │                             │
│   ┌───┴──────────────┐              │
│   │                  │              │
│   ▼                  ▼              │
│ Frontend           Backend          │
│                      │              │
│              ┌───────┴───────┐      │
│              ▼               ▼      │
│         PostgreSQL          n8n     │
│                                     │
└─────────────────────────────────────┘
```

---

# 6. Domain Structure

A simple domain setup is recommended.

Example:

```text
primehomes.com
```

Customer application:

```text
primehomes.com
```

API:

```text
api.primehomes.com
```

n8n:

```text
n8n.primehomes.com
```

The actual domain names can be changed.

---

# 7. DNS

Create DNS records pointing to the VPS IP address.

Example:

```text
A     primehomes.com       → VPS_IP
A     api.primehomes.com   → VPS_IP
A     n8n.primehomes.com   → VPS_IP
```

DNS changes may take some time to propagate.

---

# 8. Server Setup

Connect to the VPS using SSH.

Example:

```bash
ssh root@YOUR_SERVER_IP
```

Create a dedicated application user instead of running the application as root.

Example:

```bash
adduser deploy
```

Give the user the required Docker permissions.

The exact VPS provider may have its own recommended setup.

---

# 9. Update Ubuntu

Before installing the application:

```bash
sudo apt update
sudo apt upgrade -y
```

Install basic utilities:

```bash
sudo apt install -y \
    curl \
    git \
    unzip \
    ca-certificates
```

---

# 10. Install Docker

Install Docker using the official Docker installation method.

Verify:

```bash
docker --version
```

Then verify Docker Compose:

```bash
docker compose version
```

Expected:

```text
Docker version ...
Docker Compose version ...
```

---

# 11. Project Directory

Create a deployment directory:

```bash
sudo mkdir -p /opt/real-estate-lead-bot
```

Set ownership appropriately:

```bash
sudo chown -R deploy:deploy /opt/real-estate-lead-bot
```

The application can then be placed under:

```text
/opt/real-estate-lead-bot/
```

---

# 12. Production Project Structure

The deployment repository can contain:

```text
real-estate-lead-bot/
│
├── frontend/
├── backend/
├── n8n/
├── database/
├── tests/
├── docs/
│
├── docker-compose.yml
├── docker-compose.prod.yml
├── .env.example
├── .gitignore
└── README.md
```

The exact structure can evolve.

---

# 13. Docker Compose

Docker Compose should be used to manage the main application services.

Conceptually:

```yaml
services:

  frontend:
    ...

  backend:
    ...

  postgres:
    ...

  n8n:
    ...

  nginx:
    ...
```

Each service should have a clear responsibility.

---

# 14. PostgreSQL Container

PostgreSQL should use persistent storage.

Example:

```yaml
volumes:
  postgres_data:
```

The database must not rely only on the container filesystem.

If the container is removed:

```text
Container → Can be recreated
Database Data → Must remain
```

---

# 15. n8n Storage

n8n should also use persistent storage.

Example:

```yaml
volumes:
  n8n_data:
```

This ensures that n8n configuration and workflow data survive container recreation.

---

# 16. Environment Variables

Production configuration should be stored in:

```text
.env
```

Example:

```env
APP_ENV=production

POSTGRES_DB=real_estate_leads
POSTGRES_USER=
POSTGRES_PASSWORD=

DATABASE_URL=

JWT_SECRET=

N8N_WEBHOOK_SECRET=

AI_API_KEY=

N8N_BASIC_AUTH_USER=
N8N_BASIC_AUTH_PASSWORD=

CORS_ORIGINS=
```

Never commit the production `.env` file to Git.

---

# 17. Production Secrets

Secrets include:

- Database passwords.
- JWT secrets.
- AI API keys.
- n8n credentials.
- Webhook secrets.
- Authentication credentials.

They should only exist in the deployment environment.

Never place them inside:

```text
Git repository
Dockerfile
React source code
Frontend environment variables
n8n workflow JSON
README.md
```

---

# 18. Frontend Deployment

The React application should be built for production.

Example:

```bash
npm install
npm run build
```

The resulting static files can be served through Nginx.

Conceptually:

```text
React Source
    ↓
npm run build
    ↓
Production Static Files
    ↓
Nginx
```

There is no need to run a React development server in production.

---

# 19. Backend Deployment

FastAPI should run using a production ASGI server.

Example:

```bash
uvicorn app.main:app --host 0.0.0.0 --port 8000
```

For production, the container should run the backend directly rather than using development reload mode.

Do not use:

```text
--reload
```

in production.

---

# 20. Database Migration

Before the application is considered live, run database migrations.

Example:

```bash
docker compose exec backend alembic upgrade head
```

The exact command depends on the final container configuration.

The migration process should be documented and repeatable.

---

# 21. Nginx

Nginx should act as the public entry point.

Its responsibilities include:

- Receiving HTTPS traffic.
- Serving the React application.
- Forwarding API requests to FastAPI.
- Forwarding n8n traffic to the n8n container.
- Handling SSL/TLS.
- Basic request routing.

Example routing:

```text
primehomes.com
        ↓
     Nginx
        ↓
    Frontend


api.primehomes.com
        ↓
     Nginx
        ↓
    FastAPI


n8n.primehomes.com
        ↓
     Nginx
        ↓
      n8n
```

---

# 22. HTTPS

All production traffic should use HTTPS.

The application should not depend on plain HTTP for normal public access.

Recommended approach:

```text
Let's Encrypt
       ↓
SSL Certificate
       ↓
Nginx
       ↓
HTTPS
```

Certificates should be automatically renewed.

---

# 23. Firewall

Only required ports should be publicly accessible.

Typical public ports:

```text
22   SSH
80   HTTP
443  HTTPS
```

Application ports such as:

```text
5432 PostgreSQL
5678 n8n
8000 FastAPI
```

should not normally be exposed directly to the public internet.

Instead:

```text
Internet
   ↓
80 / 443
   ↓
Nginx
   ↓
Internal Docker Network
```

---

# 24. Docker Networking

Services should communicate using an internal Docker network.

Example:

```text
nginx
  │
  ├── frontend
  ├── backend
  └── n8n

backend
  │
  └── postgres
```

The public internet should not directly access PostgreSQL.

---

# 25. Application Startup

After configuring the server:

```bash
cd /opt/real-estate-lead-bot
```

Start the application:

```bash
docker compose -f docker-compose.prod.yml up -d
```

Check running containers:

```bash
docker compose ps
```

Expected services:

```text
nginx
frontend
backend
postgres
n8n
```

---

# 26. Viewing Logs

Logs should be easy to access.

All services:

```bash
docker compose logs
```

Backend:

```bash
docker compose logs backend
```

n8n:

```bash
docker compose logs n8n
```

Nginx:

```bash
docker compose logs nginx
```

Follow logs:

```bash
docker compose logs -f backend
```

---

# 27. Health Checks

The backend should expose:

```text
GET /api/v1/health
```

The deployment should use this to confirm that FastAPI is running.

Example:

```text
https://api.primehomes.com/api/v1/health
```

Expected:

```json
{
  "status": "ok"
}
```

---

# 28. Deployment Verification

After deployment, verify:

### Frontend

```text
https://primehomes.com
```

The application should load.

### Backend

```text
https://api.primehomes.com/api/v1/health
```

The API should respond.

### n8n

```text
https://n8n.primehomes.com
```

The n8n interface should load.

### Database

The backend should successfully connect to PostgreSQL.

---

# 29. First Production Test

Perform a complete customer journey after deployment.

```text
Customer
   ↓
Open Website
   ↓
Send Message
   ↓
FastAPI
   ↓
PostgreSQL
   ↓
n8n
   ↓
AI
   ↓
Lead Qualification
   ↓
Database
   ↓
Bot Response
```

Then verify that the sales team receives the appropriate notification.

---

# 30. Deployment Process

The normal deployment process should be:

```text
Developer
   ↓
Make Changes
   ↓
Run Tests
   ↓
Git Commit
   ↓
Push to Repository
   ↓
VPS
   ↓
Pull Latest Code
   ↓
Build Containers
   ↓
Run Migrations
   ↓
Restart Services
   ↓
Health Check
   ↓
Production Test
```

---

# 31. Simple Manual Deployment

For the MVP, deployment can initially be manual.

On the VPS:

```bash
cd /opt/real-estate-lead-bot
git pull
```

Build:

```bash
docker compose -f docker-compose.prod.yml build
```

Run migrations:

```bash
docker compose -f docker-compose.prod.yml run --rm backend alembic upgrade head
```

Start services:

```bash
docker compose -f docker-compose.prod.yml up -d
```

Check:

```bash
docker compose ps
```

This is sufficient for the initial MVP.

---

# 32. Automatic Deployment

A CI/CD pipeline can be introduced later.

For example:

```text
GitHub
   ↓
GitHub Actions
   ↓
Build / Test
   ↓
Deploy to VPS
```

This should not be required before the basic application is working.

---

# 33. Database Backups

PostgreSQL should be backed up regularly.

A simple backup process can use:

```bash
pg_dump
```

Example concept:

```bash
pg_dump DATABASE_URL > backup.sql
```

Backups should be stored separately from the main database.

Do not keep the only backup on the same VPS.

---

# 34. Backup Schedule

A practical starting point:

```text
Daily
↓
Database Backup
```

Keep several recent backups.

For example:

```text
backup-2026-09-01.sql
backup-2026-09-02.sql
backup-2026-09-03.sql
```

The exact retention period can be adjusted later.

---

# 35. Backup Testing

A backup is only useful if it can actually be restored.

Periodically test:

```text
Backup
  ↓
Restore
  ↓
Verify Database
```

Do not assume that a successful backup command means the backup is usable.

---

# 36. Updating the Application

When a new version is ready:

```text
1. Test locally
2. Push code
3. Pull code on VPS
4. Build containers
5. Run migrations if required
6. Restart services
7. Check logs
8. Test health endpoint
9. Test customer flow
```

---

# 37. Database Migration Rule

Database migrations should be backward-conscious.

Avoid making a deployment that requires the old application and new database schema to work only in one specific order unless necessary.

For simple MVP deployments:

```text
Code Change
    ↓
Migration
    ↓
Deploy
```

Document any migration that can affect existing data.

---

# 38. Rollback

If a deployment causes a serious problem:

```text
Stop
 ↓
Identify Problem
 ↓
Rollback Application
 ↓
Restore Database Backup if necessary
 ↓
Verify
```

Application rollback and database rollback are separate decisions.

Do not restore a database automatically unless data has actually been damaged.

---

# 39. Monitoring

The initial monitoring setup can remain simple.

Monitor:

```text
VPS CPU
VPS RAM
VPS Storage
Docker Containers
FastAPI Health
Database Availability
n8n Workflow Failures
```

The system should make it easy to notice when something stops working.

---

# 40. Storage Monitoring

Disk space is especially important because the VPS contains:

- Docker images.
- Logs.
- PostgreSQL data.
- n8n data.
- Backups if stored locally.

Check:

```bash
df -h
```

Docker storage:

```bash
docker system df
```

Do not blindly delete Docker volumes because they may contain important data.

---

# 41. Log Management

Logs should not grow indefinitely.

Production deployment should eventually use log rotation or an appropriate logging strategy.

The goal is:

```text
Useful Logs
+
Controlled Storage
```

rather than keeping unlimited logs.

---

# 42. Restart Policy

Production containers should automatically restart when appropriate.

Example concept:

```yaml
restart: unless-stopped
```

This helps recover from unexpected container failures.

---

# 43. VPS Restart

After a VPS reboot:

```text
VPS starts
   ↓
Docker starts
   ↓
Containers restart
   ↓
Nginx starts
   ↓
Application becomes available
```

The deployment should be tested after a server restart.

---

# 44. Production Environment

The production environment should use:

```text
APP_ENV=production
```

Production should have:

- Production database.
- Production n8n.
- Production API credentials.
- Production domain.
- HTTPS.

Do not accidentally connect production to development services.

---

# 45. Development vs Production

Development:

```text
Developer Computer
       ↓
Local React
       ↓
Local FastAPI
       ↓
Local PostgreSQL
       ↓
Local n8n
```

Production:

```text
VPS
       ↓
Nginx
       ↓
React
       ↓
FastAPI
       ↓
PostgreSQL
       ↓
n8n
```

They should remain separate.

---

# 46. n8n Production Configuration

n8n should run as a persistent service.

It should have:

- Persistent data.
- Proper domain.
- HTTPS.
- Authentication.
- Required environment variables.
- Production credentials.

n8n should not be exposed through an unsecured public endpoint.

---

# 47. n8n Webhooks

When FastAPI communicates with n8n:

```text
FastAPI
   ↓
Authenticated Webhook
   ↓
n8n
```

The webhook should use the agreed authentication mechanism.

Do not expose internal workflows as completely open public endpoints.

---

# 48. AI API Configuration

The AI API key should only be available to the backend/n8n components that actually require it.

The React application should never receive the AI provider's secret key.

Correct:

```text
React
 ↓
FastAPI / n8n
 ↓
AI Provider
```

Incorrect:

```text
React
 ↓
AI API Key
 ↓
AI Provider
```

---

# 49. Production Data

Production should contain real customer information only when the application is ready for it.

Before launch:

```text
Development Data
       ↓
Remove / Separate
       ↓
Production
```

Do not copy unnecessary development/test data into production.

---

# 50. VPS Scaling

Start with one VPS.

If the application grows significantly:

```text
Single VPS
    ↓
Monitor Usage
    ↓
Upgrade VPS
```

The first scaling step should usually be increasing VPS resources.

Only introduce multiple servers when there is a genuine need.

---

# 51. Future Scaling Architecture

If the application eventually becomes large:

```text
Load Balancer
      ↓
┌─────┴─────┐
▼           ▼
API 1      API 2
      │
      ▼
PostgreSQL
      │
      ▼
Automation / Workers
```

This is a future consideration.

It is not required for the initial project.

---

# 52. Deployment Checklist

Before going live:

### VPS

- [ ] Ubuntu installed.
- [ ] Docker installed.
- [ ] Docker Compose working.
- [ ] Application user configured.
- [ ] Firewall configured.
- [ ] Domain connected.

### Application

- [ ] Frontend builds successfully.
- [ ] Backend starts successfully.
- [ ] PostgreSQL starts successfully.
- [ ] n8n starts successfully.
- [ ] Environment variables configured.

### Database

- [ ] Migrations completed.
- [ ] Persistent volume configured.
- [ ] Backup process configured.

### Nginx

- [ ] Domain configured.
- [ ] API routing works.
- [ ] HTTPS enabled.
- [ ] n8n routing works.

### Application Testing

- [ ] Customer can open website.
- [ ] Customer can send message.
- [ ] Message reaches FastAPI.
- [ ] Message is stored.
- [ ] n8n workflow runs.
- [ ] AI processes message.
- [ ] Lead is qualified.
- [ ] Bot responds.
- [ ] Sales notification works.

---

# 53. Definition of Done

The VPS deployment is considered complete when:

- The application runs successfully on the VPS.
- The frontend is accessible through the domain.
- FastAPI is accessible through the API domain.
- PostgreSQL persists data correctly.
- n8n runs persistently.
- HTTPS works.
- Production environment variables are configured.
- Database migrations work.
- Database backups work.
- The complete customer journey works.
- Containers restart correctly after a VPS reboot.
- Logs can be inspected.
- The application can be updated without manually rebuilding the entire server.

---

# 54. Final Deployment Principle

The first production environment should be:

```text
ONE VPS
+
DOCKER
+
NGINX
+
REACT
+
FASTAPI
+
POSTGRESQL
+
N8N
```

That is enough.

Do not introduce Kubernetes, multiple VPS instances, complex cloud infrastructure, message brokers, or microservices unless the application's actual requirements justify them.

The priority is to get a **stable, maintainable, working production system** running on a VPS first.

Scale the infrastructure only when the application needs it.