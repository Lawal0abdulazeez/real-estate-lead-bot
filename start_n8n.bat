@echo off
setlocal enabledelayedexpansion

cd /d "%~dp0"

echo ==========================================================
echo   PrimeHomes n8n Startup (Batch Script)
echo ==========================================================

:: 0. Load variables from .env
if exist ".env" (
    for /f "usebackq eol=# tokens=1* delims==" %%A in (".env") do (
        if not "%%B"=="" (
            set "key=%%A"
            set "val=%%B"
            if not defined !key! set "!key!=!val!"
        )
    )
)

:: 1. Allow n8n expressions to read custom environment variables
set N8N_ENV_VARS_EXPRESSION_ALLOW=API_BASE_URL,LLM_BASE_URL,QUALIFY_WEBHOOK_URL,SALES_NOTIFY_WEBHOOK_URL,FASTAPI_INTERNAL_TOKEN,LLM_API_KEY,N8N_INTERNAL_TOKEN,LLM_MODEL,N8N_CONTEXT_MESSAGE_LIMIT,GROQ_API_KEY,GROQ_BASE_URL,GROQ_MODEL,AI_API_KEY,AI_BASE_URL,AI_MODEL
set N8N_BLOCK_ENV_ACCESS_IN_NODE=false

:: 2. Ensure defaults if not set in .env
if not defined API_BASE_URL set API_BASE_URL=http://127.0.0.1:8000
if not defined N8N_BASE_URL set N8N_BASE_URL=http://127.0.0.1:5678
if not defined N8N_PORT set N8N_PORT=5678
if not defined N8N_HOST set N8N_HOST=localhost
if not defined N8N_PROTOCOL set N8N_PROTOCOL=http
if not defined N8N_WEBHOOK_URL set N8N_WEBHOOK_URL=http://127.0.0.1:5678/webhook/primehomes/lead/process-message
if not defined N8N_CONTEXT_MESSAGE_LIMIT set N8N_CONTEXT_MESSAGE_LIMIT=12

if not defined LLM_API_KEY set LLM_API_KEY=%GROQ_API_KEY%
if not defined GROQ_API_KEY set GROQ_API_KEY=%LLM_API_KEY%
if not defined AI_API_KEY set AI_API_KEY=%LLM_API_KEY%
if not defined LLM_BASE_URL set LLM_BASE_URL=%GROQ_BASE_URL%
if not defined LLM_MODEL set LLM_MODEL=%GROQ_MODEL%
if not defined LLM_MODEL set LLM_MODEL=openai/gpt-oss-120b

if not defined SALES_NOTIFY_WEBHOOK_URL set SALES_NOTIFY_WEBHOOK_URL=http://127.0.0.1:8000/api/v1/health
if not defined QUALIFY_WEBHOOK_URL set QUALIFY_WEBHOOK_URL=http://127.0.0.1:8000/api/v1/leads

echo API URL:   %API_BASE_URL%
echo LLM Model: %LLM_MODEL%
echo LLM Host:  %LLM_BASE_URL%
echo.
echo Starting n8n...
call n8n.cmd start
