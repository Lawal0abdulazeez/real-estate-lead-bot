import os
import sys
import subprocess
import threading
import time
import signal

# Set up paths
ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
VENV_PYTHON = os.path.join(ROOT_DIR, ".venv", "Scripts", "python.exe")
BACKEND_DIR = os.path.join(ROOT_DIR, "backend")
FRONTEND_DIR = os.path.join(ROOT_DIR, "frontend")

processes = []

def stream_output(process, prefix, color_code):
    """Streams output from a subprocess with a tagged prefix."""
    reset_code = "\033[0m"
    try:
        for line in iter(process.stdout.readline, ""):
            if not line:
                break
            print(f"{color_code}[{prefix}]{reset_code} {line.rstrip()}", flush=True)
    except Exception:
        pass

def load_dotenv(filepath, override=True):
    """Loads key-value pairs from .env into os.environ."""
    if not os.path.exists(filepath):
        return
    with open(filepath, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith("#") or "=" not in line:
                continue
            k, v = line.split("=", 1)
            k = k.strip()
            v = v.strip().strip('"').strip("'")
            if k:
                # If override is True, or not present, or current value is a placeholder
                current = os.environ.get(k, "")
                if override or not current or current.startswith("YOUR_") or current.startswith("change-me"):
                    os.environ[k] = v


def main():
    # Load .env variables from root
    load_dotenv(os.path.join(ROOT_DIR, ".env"))

    # Fix Windows console encoding
    try:
        sys.stdout.reconfigure(encoding='utf-8', errors='replace')
        sys.stderr.reconfigure(encoding='utf-8', errors='replace')
    except Exception:
        pass

    # ANSI color codes
    CYAN = "\033[96m"
    GREEN = "\033[92m"
    YELLOW = "\033[93m"
    MAGENTA = "\033[95m"
    RESET = "\033[0m"

    # Enable ANSI colors on Windows console
    os.system("")

    print(f"{CYAN}=========================================================={RESET}")
    print(f"{YELLOW}  PrimeHomes Real Estate Lead Bot - Unified Runner        {RESET}")
    print(f"{CYAN}=========================================================={RESET}")

    # 1. Check MySQL connection & ensure tables exist
    sys.path.insert(0, BACKEND_DIR)
    try:
        import asyncio
        from app.db.base import Base
        from app.db.session import engine
        from app.models import Activity, Conversation, FollowUp, Lead, LeadScore, Message  # noqa: F401
        from sqlalchemy import text

        async def init_db():
            async with engine.begin() as conn:
                await conn.execute(text("SELECT 1"))
                await conn.run_sync(Base.metadata.create_all)
            await engine.dispose()

        asyncio.run(init_db())
        print(f"{GREEN}[OK] MySQL Database connected & tables verified successfully.{RESET}")
    except Exception as e:
        print(f"{YELLOW}[WARN] MySQL warning: {e}{RESET}")
        print(f"{YELLOW}       (Ensure MySQL80 service is running if DB operations fail){RESET}")

    print("\nStarting all 3 services in this single terminal:")
    print("  • [BACKEND]   FastAPI API     -> http://localhost:8000/docs")
    print("  • [N8N]       Workflow Engine -> http://localhost:5678")
    print("  • [FRONTEND]  React Web App   -> http://localhost:5173")
    print(f"\n{YELLOW}Press Ctrl+C at any time to stop all services simultaneously.{RESET}")
    print(f"{CYAN}----------------------------------------------------------{RESET}\n")

    # 2. Dynamic Environment for n8n (read entirely from .env / process env)
    llm_key = os.environ.get("LLM_API_KEY") or os.environ.get("GROQ_API_KEY") or os.environ.get("AI_API_KEY") or ""
    llm_base = os.environ.get("LLM_BASE_URL") or os.environ.get("GROQ_BASE_URL") or os.environ.get("AI_BASE_URL") or "https://api.groq.com/openai/v1"
    llm_model = os.environ.get("LLM_MODEL") or os.environ.get("GROQ_MODEL") or os.environ.get("AI_MODEL") or "openai/gpt-oss-120b"
    api_base = os.environ.get("API_BASE_URL", "http://127.0.0.1:8000").rstrip("/")
    internal_token = os.environ.get("FASTAPI_INTERNAL_TOKEN", "primehomes-internal-dev-token")

    n8n_env = os.environ.copy()
    n8n_env.update({
        "N8N_ENV_VARS_EXPRESSION_ALLOW": (
            "API_BASE_URL,LLM_BASE_URL,QUALIFY_WEBHOOK_URL,SALES_NOTIFY_WEBHOOK_URL,"
            "FASTAPI_INTERNAL_TOKEN,LLM_API_KEY,N8N_INTERNAL_TOKEN,LLM_MODEL,"
            "N8N_CONTEXT_MESSAGE_LIMIT,GROQ_API_KEY,GROQ_BASE_URL,GROQ_MODEL,"
            "AI_API_KEY,AI_BASE_URL,AI_MODEL,RECORD_ACTIVITY_URL,QUALIFICATION_API_URL,"
            "SAVE_SCORE_HISTORY_URL,SALES_FALLBACK_WEBHOOK_URL,FOLLOWUP_NOTIFY_WEBHOOK_URL,"
            "GOOGLE_SHEET_ID,GOOGLE_SHEET_NAME"
        ),
        "N8N_BLOCK_ENV_ACCESS_IN_NODE": "false",
        "API_BASE_URL": api_base,
        "N8N_BASE_URL": os.environ.get("N8N_BASE_URL", "http://127.0.0.1:5678"),
        "N8N_PORT": os.environ.get("N8N_PORT", "5678"),
        "N8N_HOST": os.environ.get("N8N_HOST", "localhost"),
        "N8N_PROTOCOL": os.environ.get("N8N_PROTOCOL", "http"),
        "N8N_WEBHOOK_URL": os.environ.get("N8N_WEBHOOK_URL", "http://127.0.0.1:5678/webhook/primehomes/lead/process-message"),
        "N8N_WEBHOOK_SECRET": os.environ.get("N8N_WEBHOOK_SECRET", ""),
        "N8N_CONTEXT_MESSAGE_LIMIT": os.environ.get("N8N_CONTEXT_MESSAGE_LIMIT", "12"),
        "LLM_API_KEY": llm_key,
        "GROQ_API_KEY": llm_key,
        "AI_API_KEY": llm_key,
        "LLM_BASE_URL": llm_base,
        "GROQ_BASE_URL": llm_base,
        "AI_BASE_URL": llm_base,
        "LLM_MODEL": llm_model,
        "GROQ_MODEL": llm_model,
        "AI_MODEL": llm_model,
        "FASTAPI_INTERNAL_TOKEN": internal_token,
        "N8N_INTERNAL_TOKEN": os.environ.get("N8N_INTERNAL_TOKEN", internal_token),
        "RECORD_ACTIVITY_URL": os.environ.get("RECORD_ACTIVITY_URL", f"{api_base}/api/v1/activities"),
        "QUALIFICATION_API_URL": os.environ.get("QUALIFICATION_API_URL", f"{api_base}/api/v1/qualification/calculate"),
        "SAVE_SCORE_HISTORY_URL": os.environ.get("SAVE_SCORE_HISTORY_URL", f"{api_base}/api/v1/qualification/score-history"),
        "QUALIFY_WEBHOOK_URL": os.environ.get("QUALIFY_WEBHOOK_URL", "http://127.0.0.1:5678/webhook/prh-lead-qualify"),
        "SALES_NOTIFY_WEBHOOK_URL": os.environ.get("SALES_NOTIFY_WEBHOOK_URL", "http://127.0.0.1:5678/webhook/prh-lead-notify-sales"),
        "SALES_FALLBACK_WEBHOOK_URL": os.environ.get("SALES_FALLBACK_WEBHOOK_URL", f"{api_base}/api/v1/qualification/notifications/sales"),
        "FOLLOWUP_NOTIFY_WEBHOOK_URL": os.environ.get("FOLLOWUP_NOTIFY_WEBHOOK_URL", f"{api_base}/api/v1/qualification/notifications/sales"),
        "GOOGLE_SHEET_ID": os.environ.get("GOOGLE_SHEET_ID", ""),
        "GOOGLE_SHEET_NAME": os.environ.get("GOOGLE_SHEET_NAME", "Leads"),
    })

    n8n_cmd = "n8n.cmd" if os.name == "nt" else "n8n"

    # Start Backend
    backend_proc = subprocess.Popen(
        [VENV_PYTHON, "-m", "uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"],
        cwd=BACKEND_DIR,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True,
        bufsize=1,
    )
    processes.append(("BACKEND", backend_proc))

    # Start n8n
    n8n_proc = subprocess.Popen(
        [n8n_cmd, "start"],
        cwd=ROOT_DIR,
        env=n8n_env,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True,
        bufsize=1,
        shell=True,
    )
    processes.append(("N8N", n8n_proc))

    # Start Frontend
    frontend_proc = subprocess.Popen(
        ["npm.cmd" if os.name == "nt" else "npm", "run", "dev"],
        cwd=FRONTEND_DIR,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True,
        bufsize=1,
        shell=True,
    )
    processes.append(("FRONTEND", frontend_proc))

    # Start streaming threads
    threads = []
    t_backend = threading.Thread(target=stream_output, args=(backend_proc, "BACKEND", GREEN), daemon=True)
    t_n8n = threading.Thread(target=stream_output, args=(n8n_proc, "N8N", MAGENTA), daemon=True)
    t_frontend = threading.Thread(target=stream_output, args=(frontend_proc, "FRONTEND", CYAN), daemon=True)

    for t in [t_backend, t_n8n, t_frontend]:
        t.start()
        threads.append(t)

    try:
        while True:
            time.sleep(0.5)
            for name, p in processes:
                code = p.poll()
                if code is not None and code != 0:
                    print(f"{YELLOW}[{name}] Process stopped with code {code}{RESET}", flush=True)
    except KeyboardInterrupt:
        print(f"\n{YELLOW}Stopping all services...{RESET}", flush=True)
        for name, p in processes:
            try:
                p.terminate()
            except Exception:
                pass
        time.sleep(0.8)
        for name, p in processes:
            try:
                p.kill()
            except Exception:
                pass
        print(f"{GREEN}All services stopped successfully.{RESET}")

if __name__ == "__main__":
    main()
