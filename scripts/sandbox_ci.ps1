# CAD CI/CD Sandbox Simulation Runner (PowerShell)
# Configured for zero terminal window popups on Windows 10/11
param(
    [switch]$Silent = $false
)

$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$ProjectRoot = Split-Path -Parent $ScriptDir

# Force silent execution and suppress cadgen daemon warm worker spawning
$env:CADGEN_DAEMON = "0"

function Invoke-CommandSilent {
    param(
        [string]$Executable,
        [string[]]$Arguments
    )

    $resolvedExe = $Executable
    if ($Executable -eq "python") {
        $pyw = (Get-Command pythonw.exe -ErrorAction SilentlyContinue)
        if ($pyw) { $resolvedExe = $pyw.Source }
    }

    $psi = New-Object System.Diagnostics.ProcessStartInfo
    $psi.FileName = $resolvedExe
    $psi.Arguments = ($Arguments -join " ")
    $psi.WorkingDirectory = $ProjectRoot
    $psi.CreateNoWindow = $true
    $psi.UseShellExecute = $false
    $psi.RedirectStandardInput = $true
    $psi.RedirectStandardOutput = $true
    $psi.RedirectStandardError = $true
    $psi.WindowStyle = [System.Diagnostics.ProcessWindowStyle]::Hidden

    $process = [System.Diagnostics.Process]::Start($psi)
    $stdout = $process.StandardOutput.ReadToEnd()
    $stderr = $process.StandardError.ReadToEnd()
    $process.WaitForExit()

    if ($stdout) { Write-Host $stdout }
    if ($stderr) { Write-Host $stderr -ForegroundColor Yellow }
    return $process.ExitCode
}

Write-Host "===================================================" -ForegroundColor Cyan
Write-Host "  Starting CAD CI/CD Local Sandbox Simulation...   " -ForegroundColor Cyan
Write-Host "===================================================" -ForegroundColor Cyan

# Run CI sandbox pipeline (runs silent via ProcessStartInfo)
$exitCode = Invoke-CommandSilent -Executable "python" -Arguments @("`"$ScriptDir\ci_sandbox.py`"", "--all")
if ($exitCode -ne 0) {
    Write-Host "`n[FAIL] CI/CD Sandbox Pipeline Failed (Exit Code: $exitCode)!" -ForegroundColor Red
    exit $exitCode
}

Write-Host "`n[PASS] Running Pytest Verification Suite..." -ForegroundColor Green
$testExit = Invoke-CommandSilent -Executable "python" -Arguments @("-m", "pytest", "`"$ProjectRoot\tests`"", "-v")
exit $testExit
