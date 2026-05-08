$ErrorActionPreference = "Stop"

Write-Host "== NewsHub Windows setup ==" -ForegroundColor Cyan
Set-Location -Path "C:\Users\LENOVO\Desktop\django"

if (Test-Path ".venv") {
    Write-Host "Removing existing .venv ..." -ForegroundColor Yellow
    Remove-Item -Recurse -Force ".venv"
}

Write-Host "Creating virtual environment ..." -ForegroundColor Cyan
try {
    python -m venv .venv
} catch {
    Write-Host "venv failed, trying ensurepip and retry ..." -ForegroundColor Yellow
    python -m ensurepip --upgrade
    python -m venv .venv
}

Write-Host "Activating .venv ..." -ForegroundColor Cyan
& ".\.venv\Scripts\Activate.ps1"

Write-Host "Upgrading pip/setuptools/wheel ..." -ForegroundColor Cyan
python -m pip install --upgrade pip setuptools wheel

Write-Host "Installing requirements ..." -ForegroundColor Cyan
pip install -r requirements.txt

Write-Host "Applying migrations ..." -ForegroundColor Cyan
python manage.py migrate

Write-Host ""
Write-Host "Setup complete." -ForegroundColor Green
Write-Host "Next commands:"
Write-Host "  python manage.py createsuperuser"
Write-Host "  python manage.py runserver"
