# Esegue la pipeline mock che aggiorna data\offers.json
if (-not (Test-Path ".\.venv\Scripts\python.exe")) {
  Write-Error "Ambiente non inizializzato. Esegui prima .\scripts\setup.ps1"
  exit 1
}
.\.venv\Scripts\python.exe pipeline\run_pipeline.py
