# Setup script for Windows PowerShell
$ErrorActionPreference = "Stop"
Set-Location $PSScriptRoot

Write-Host "Creating virtual environment..." -ForegroundColor Cyan
py -3 -m venv .venv

Write-Host "Installing dependencies..." -ForegroundColor Cyan
.\.venv\Scripts\python.exe -m pip install -r requirements.txt

Write-Host "Generating customer data..." -ForegroundColor Cyan
.\.venv\Scripts\python.exe -m src.data.generate_data

Write-Host "Training churn model..." -ForegroundColor Cyan
.\.venv\Scripts\python.exe -m src.models.train

Write-Host ""
Write-Host "Setup complete!" -ForegroundColor Green
Write-Host "  API:       uvicorn src.api.main:app --reload --port 8000"
Write-Host "  Dashboard: streamlit run src/dashboard/app.py"
