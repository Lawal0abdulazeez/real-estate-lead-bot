<#
.SYNOPSIS
    Starts all PrimeHomes Lead Bot Services in ONE SINGLE terminal window:
    - FastAPI Backend (:8000)
    - n8n Server (:5678)
    - React Frontend (:5173)
#>

$WorkspaceRoot = $PSScriptRoot
$VenvPython = Join-Path $WorkspaceRoot ".venv\Scripts\python.exe"

if (-not (Test-Path $VenvPython)) {
    Write-Host "[ERROR] Virtual environment not found at .venv" -ForegroundColor Red
    exit 1
}

# Run the unified runner in this terminal
& $VenvPython (Join-Path $WorkspaceRoot "run_all.py")
