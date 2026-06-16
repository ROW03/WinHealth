# Runbook

## Automating with Task Scheduler
To run these scripts automatically:
1. Open PowerShell as an **Administrator**.
2. Run this command:
   ```powershell
   $Action = New-ScheduledTaskAction -Execute "powershell.exe" -Argument "-File C:\Path\To\scripts\Get-SystemSnapshot.ps1"
   $Trigger = New-ScheduledTaskTrigger -Daily -At 9am
   Register-ScheduledTask -Action $Action -Trigger $Trigger -TaskName "WinHealth-Snapshot"