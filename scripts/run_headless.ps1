# Headless command runner for Windows - guarantees 0 terminal popups
param(
    [Parameter(Mandatory=$true)]
    [string]$Command,
    [string]$LogFile = "$PSScriptRoot\..\tmp\headless.log"
)

$env:CADGEN_DAEMON = "0"
$proc = Start-Process -FilePath "powershell" -ArgumentList "-NoProfile", "-Command", $Command -WindowStyle Hidden -Wait -PassThru -RedirectStandardOutput $LogFile -RedirectStandardError "$LogFile.err"
exit $proc.ExitCode
