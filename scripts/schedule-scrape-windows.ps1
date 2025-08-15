# Pianifica aggiornamento ogni 6 ore (locale)
$python = (Resolve-Path ".\.venv\Scripts\python.exe").Path
$script = (Resolve-Path ".\pipeline\run_pipeline.py").Path
$action = New-ScheduledTaskAction -Execute $python -Argument $script
$trigger = New-ScheduledTaskTrigger -Once -At (Get-Date).AddMinutes(5) -RepetitionInterval (New-TimeSpan -Hours 6) -RepetitionDuration ([TimeSpan]::MaxValue)
Register-ScheduledTask -Action $action -Trigger $trigger -TaskName "Supermercati-Update" -Description "Aggiorna data\\offers.json ogni 6 ore" -User "$env:USERNAME" -RunLevel Limited
Write-Host "Attività pianificata creata (Supermercati-Update)."
