param()

# --- Paths ---
$root = "C:\Users\batti\Desktop\supermercati risparmio prodotti"
$site = Join-Path $root "site"
$idx  = Join-Path $site "index.html"

# --- 1) Ensure index exists (create simple test page if missing) ---
if (!(Test-Path $site)) { New-Item -ItemType Directory -Path $site -Force | Out-Null }
if (!(Test-Path $idx)) {
  $html = "<!doctype html><html lang=""it""><head><meta charset=""utf-8""><meta name=""viewport"" content=""width=device-width,initial-scale=1""><title>Spesa Semplice - Test</title><style>body{font-family:system-ui,Arial;padding:24px}</style></head><body><h1>Pagina di test</h1><p>Index creato. Poi sostituiscilo con l'index completo.</p></body></html>"
  $html | Set-Content -Path $idx -Encoding UTF8 -Force
}

# --- 2) Start API in new window ---
$apiCmd = @"
Set-Location ""$root""
& .\.venv\Scripts\Activate.ps1
$env:PYTHONPATH = (Get-Location).Path
.\.venv\Scripts\uvicorn.exe api.main:app --host 127.0.0.1 --port 8000 --reload
"@
Start-Process powershell -ArgumentList $apiCmd -WindowStyle Normal

Start-Sleep -Seconds 2

# --- 3) Start static file server on 5500 in new window ---
$py = "$env:LOCALAPPDATA\Programs\Python\Python313\python.exe"
if (!(Test-Path $py)) { $py = "python" }
$siteCmd = @"
Set-Location ""$site""
""$py"" -m http.server 5500
"@
Start-Process powershell -ArgumentList $siteCmd -WindowStyle Normal

Start-Sleep -Seconds 1

# --- 4) Open Edge at correct URL ---
Start-Process msedge "http://127.0.0.1:5500"
Write-Host "OK: aperto http://127.0.0.1:5500 - se richiesto, imposta API: http://127.0.0.1:8000"
