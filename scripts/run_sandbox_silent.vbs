' Silent CI/CD Sandbox Launcher for Windows
' Runs the sandbox CI pipeline with window style 0 (SW_HIDE) - 100% windowless execution.
Set fso = CreateObject("Scripting.FileSystemObject")
Set WshShell = CreateObject("WScript.Shell")

scriptDir = fso.GetParentFolderName(WScript.ScriptFullName)
projectRoot = fso.GetParentFolderName(scriptDir)

cmd = "powershell.exe -WindowStyle Hidden -ExecutionPolicy Bypass -File """ & scriptDir & "\sandbox_ci.ps1"""
WshShell.Run cmd, 0, True
