# CAD CI/CD Sandbox Simulation Runner (PowerShell)
Write-Host "===================================================" -ForegroundColor Cyan
Write-Host "  Starting CAD CI/CD Local Sandbox Simulation...   " -ForegroundColor Cyan
Write-Host "===================================================" -ForegroundColor Cyan

$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$ProjectRoot = Split-Path -Parent $ScriptDir

# Disable cadgen background daemon and warm worker pool to prevent console window popups
$env:CADGEN_DAEMON = "0"

$p1 = Start-Process -FilePath "python" -ArgumentList "`"$ScriptDir\ci_sandbox.py`"", "--all" -NoNewWindow -Wait -PassThru
if ($p1.ExitCode -ne 0) {
    Write-Host "`n[FAIL] CI/CD Sandbox Pipeline Failed!" -ForegroundColor Red
    exit $p1.ExitCode
}

Write-Host "`n[PASS] Running Pytest Verification Suite..." -ForegroundColor Green
$p2 = Start-Process -FilePath "python" -ArgumentList "-m", "pytest", "`"$ProjectRoot\tests`"", "-v" -NoNewWindow -Wait -PassThru
exit $p2.ExitCode
