# Chiede all'API di eseguire la pipeline (/refresh) e ricarica i dati
try {
  Invoke-RestMethod -Method POST -Uri "http://localhost:8000/refresh" | Out-Host
} catch {
  Write-Error "API non raggiungibile. Avvia prima .\scripts\run-api.ps1"
}
