# Crea venv e installa dipendenze API
Write-Host "==> Creazione ambiente Python"
python -m venv .venv
.\.venv\Scripts\pip.exe install --upgrade pip
.\.venv\Scripts\pip.exe install -r api\requirements.txt
Write-Host "Pronto. Usa run-api.ps1 per avviare l'API e open-site.ps1 per aprire il sito."
