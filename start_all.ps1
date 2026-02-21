<#
start_all.ps1

Opens two PowerShell windows:
 - backend: activates .venv and runs api.py from repo root
 - frontend: cd into frontend folder and runs `npm run dev`

Usage: run this script from the repository root (or double-click it).
#>

Write-Host "Starting backend and (then) frontend in separate PowerShell windows..." -ForegroundColor Green

$scriptRoot = Split-Path -Parent $MyInvocation.MyCommand.Definition

# Backend command: activate venv (if present) and run api.py
$venvActivate = Join-Path $scriptRoot ".venv\Scripts\Activate.ps1"
$backendCmdParts = @()
if (Test-Path $venvActivate) {
    $backendCmdParts += ". '$venvActivate'"
} else {
    $backendCmdParts += "Write-Host 'Warning: venv not found at $venvActivate' -ForegroundColor Yellow"
}
$backendCmdParts += "Set-Location -Path '$scriptRoot'"
$backendCmdParts += "python .\api.py"
$backendCommand = $backendCmdParts -join "; `n"

Write-Host "Launching backend window..."
Start-Process -FilePath "powershell.exe" -ArgumentList "-NoExit", "-Command", $backendCommand -WorkingDirectory $scriptRoot

# Wait for backend health endpoint to be ready before starting frontend
$healthUrl = 'http://127.0.0.1:5000/health'
$maxWaitSeconds = 60
$intervalSeconds = 2
$elapsed = 0
Write-Host "Waiting for backend to become healthy at $healthUrl (timeout: ${maxWaitSeconds}s)" -ForegroundColor Cyan
while ($elapsed -lt $maxWaitSeconds) {
    try {
        $resp = Invoke-RestMethod -Uri $healthUrl -Method Get -TimeoutSec 5
        if ($resp -and $resp.status -eq 'healthy') {
            Write-Host "Backend is healthy. Proceeding to start frontend..." -ForegroundColor Green
            break
        }
    } catch {
        # ignore errors, not ready yet
    }
    Start-Sleep -Seconds $intervalSeconds
    $elapsed += $intervalSeconds
}

if ($elapsed -ge $maxWaitSeconds) {
    Write-Host "Warning: backend did not become healthy within ${maxWaitSeconds}s. Starting frontend anyway." -ForegroundColor Yellow
}

# Frontend command: cd to frontend folder and run npm dev
$frontendDir = Join-Path $scriptRoot "Cattles-Breed-Detection-Frontend\Frontend"
$frontendCmd = "Set-Location -Path '$frontendDir'; npm run dev"
Write-Host "Launching frontend window..."
Start-Process -FilePath "powershell.exe" -ArgumentList "-NoExit", "-Command", $frontendCmd -WorkingDirectory $frontendDir

Write-Host "Launched backend and frontend windows." -ForegroundColor Green