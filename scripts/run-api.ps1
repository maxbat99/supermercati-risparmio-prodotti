param([int]$Port = 8000)
$ErrorActionPreference = "Stop"
$root = Split-Path -Parent (Split-Path -Parent $MyInvocation.MyCommand.Path)
$venv = Join-Path $root ".venv"
if (-not (Test-Path $venv)) {
  Write-Host "==> Creo virtualenv"
  python -m venv $venv
}
Write-Host "==> Attivo virtualenv"
& (Join-Path $venv "Scripts\Activate.ps1")
Write-Host "==> Aggiorno pip"
python -m pip install --upgrade pip
Write-Host "==> Installo dipendenze"
pip install -r (Join-Path $root "requirements.txt")
Write-Host "==> Avvio API su http://127.0.0.1:$Port"
$env:PYTHONPATH = $root   # assicura che 'api' sia importabile
uvicorn api.main:app --host 127.0.0.1 --port $Port --reload
