<#
Portable backend startup script.
This script activates the repository virtual environment (if present) and runs api.py from the repository root.
Run from the repository root or by double-clicking this script in Explorer.
#>

Write-Host "Starting Cattle Breed Detection API Server..." -ForegroundColor Green

# Determine repo root relative to this script
$scriptRoot = Split-Path -Parent $MyInvocation.MyCommand.Definition
Set-Location $scriptRoot

# Activate virtual environment if present
$venvActivate = Join-Path $scriptRoot ".venv\Scripts\Activate.ps1"
if (Test-Path $venvActivate) {
	Write-Host "Activating venv: $venvActivate"
	. $venvActivate
} else {
	Write-Host "Warning: venv not found at $venvActivate. Ensure you create one (py -3.11 -m venv .venv)" -ForegroundColor Yellow
}

Write-Host "Running api.py from: $scriptRoot"
python .\api.py
