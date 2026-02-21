<#
start_frontend.ps1

Simple helper to start the frontend dev server from the repo root.
Run this from the repository root or double-click.
#>

Write-Host "Starting frontend dev server..." -ForegroundColor Green
$scriptRoot = Split-Path -Parent $MyInvocation.MyCommand.Definition
$frontendDir = Join-Path $scriptRoot "Cattles-Breed-Detection-Frontend\Frontend"
if (-Not (Test-Path $frontendDir)) {
    Write-Host "Frontend directory not found: $frontendDir" -ForegroundColor Red
    exit 1
}
Set-Location -Path $frontendDir
npm install
npm run dev