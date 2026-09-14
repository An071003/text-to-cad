# CAD CI/CD Sandbox Simulation Runner (PowerShell)
Write-Host "===================================================" -ForegroundColor Cyan
Write-Host "  Starting CAD CI/CD Local Sandbox Simulation...   " -ForegroundColor Cyan
Write-Host "===================================================" -ForegroundColor Cyan

$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$ProjectRoot = Split-Path -Parent $ScriptDir

python "$ScriptDir\ci_sandbox.py" --all
if ($LASTEXITCODE -ne 0) {
    Write-Host "`n[FAIL] CI/CD Sandbox Pipeline Failed!" -ForegroundColor Red
    exit $LASTEXITCODE
}

Write-Host "`n[PASS] Running Pytest Verification Suite..." -ForegroundColor Green
python -m pytest "$ProjectRoot\tests" -v
exit $LASTEXITCODE
