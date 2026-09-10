Write-Host "==========================================================" -ForegroundColor Cyan
Write-Host "  PrimeHomes n8n Startup (PowerShell Script)              " -ForegroundColor Yellow
Write-Host "==========================================================" -ForegroundColor Cyan

# 0. Load .env file if present
$envPath = Join-Path $PSScriptRoot ".env"
if (Test-Path $envPath) {
    Get-Content $envPath | ForEach-Object {
        $line = $_.Trim()
        if ($line -and -not $line.StartsWith("#") -and $line.Contains("=")) {
            $parts = $line.Split("=", 2)
            $k = $parts[0].Trim()
            $v = $parts[1].Trim().Trim('"').Trim("'")
            $curr = [System.Environment]::GetEnvironmentVariable($k)
            if (-not $curr -or $curr.StartsWith("YOUR_") -or $curr.StartsWith("change-me")) {
                [System.Environment]::SetEnvironmentVariable($k, $v)
            }
        }
    }
}

# 1. Allow n8n expressions to read custom environment variables (comma-separated list)
$env:N8N_ENV_VARS_EXPRESSION_ALLOW = "API_BASE_URL,LLM_BASE_URL,QUALIFY_WEBHOOK_URL,SALES_NOTIFY_WEBHOOK_URL,FASTAPI_INTERNAL_TOKEN,LLM_API_KEY,N8N_INTERNAL_TOKEN,LLM_MODEL,N8N_CONTEXT_MESSAGE_LIMIT,GROQ_API_KEY,GROQ_BASE_URL,GROQ_MODEL,AI_API_KEY,AI_BASE_URL,AI_MODEL"
$env:N8N_BLOCK_ENV_ACCESS_IN_NODE = "false"

# 2. FastAPI Backend URL
if (-not $env:API_BASE_URL) { $env:API_BASE_URL = "http://127.0.0.1:8000" }

# 3. n8n Server & Webhook Configuration
if (-not $env:N8N_BASE_URL) { $env:N8N_BASE_URL = "http://127.0.0.1:5678" }
if (-not $env:N8N_PORT) { $env:N8N_PORT = "5678" }
if (-not $env:N8N_HOST) { $env:N8N_HOST = "localhost" }
if (-not $env:N8N_PROTOCOL) { $env:N8N_PROTOCOL = "http" }
if (-not $env:N8N_WEBHOOK_URL) { $env:N8N_WEBHOOK_URL = "http://127.0.0.1:5678/webhook/primehomes/lead/process-message" }
if (-not $env:N8N_CONTEXT_MESSAGE_LIMIT) { $env:N8N_CONTEXT_MESSAGE_LIMIT = "12" }

# 4. LLM / Groq Configuration (synced from environment)
if (-not $env:LLM_API_KEY) { $env:LLM_API_KEY = $env:GROQ_API_KEY }
if (-not $env:GROQ_API_KEY) { $env:GROQ_API_KEY = $env:LLM_API_KEY }
if (-not $env:AI_API_KEY) { $env:AI_API_KEY = $env:LLM_API_KEY }
if (-not $env:LLM_BASE_URL) { $env:LLM_BASE_URL = $env:GROQ_BASE_URL }
if (-not $env:LLM_MODEL) { $env:LLM_MODEL = if ($env:GROQ_MODEL) { $env:GROQ_MODEL } else { "openai/gpt-oss-120b" } }

# 5. Webhook URLs
if (-not $env:SALES_NOTIFY_WEBHOOK_URL) { $env:SALES_NOTIFY_WEBHOOK_URL = "http://127.0.0.1:8000/api/v1/health" }
if (-not $env:QUALIFY_WEBHOOK_URL) { $env:QUALIFY_WEBHOOK_URL = "http://127.0.0.1:8000/api/v1/leads" }

Write-Host "Connecting to API: $env:API_BASE_URL" -ForegroundColor Green
Write-Host "Connecting to LLM: $env:LLM_BASE_URL ($env:LLM_MODEL)" -ForegroundColor Green
Write-Host "Starting n8n on port $env:N8N_PORT..." -ForegroundColor Cyan

if (Get-Command "n8n.cmd" -ErrorAction SilentlyContinue) {
    & "n8n.cmd" start
} else {
    n8n start
}

