# Safe deploy to production server (Ubuntu + gunicorn at /var/www/farazbam)
# Usage: .\scripts\deploy-remote.ps1
# Requires: PuTTY plink.exe and pscp.exe

$ErrorActionPreference = "Stop"

$ServerHost = if ($env:DEPLOY_HOST) { $env:DEPLOY_HOST } else { "87.248.155.111" }
$ServerPort = if ($env:DEPLOY_PORT) { $env:DEPLOY_PORT } else { "9011" }
$ServerUser = if ($env:DEPLOY_USER) { $env:DEPLOY_USER } else { "root" }
$ServerPass = $env:DEPLOY_PASS
if (-not $ServerPass) { throw "Set DEPLOY_PASS environment variable before running deploy." }
$RemotePath = "/var/www/farazbam"
$LocalRoot = Split-Path (Split-Path $PSScriptRoot -Parent) -Parent
$ProjectRoot = Join-Path $LocalRoot "farazbam"

$Plink = "C:\Program Files\PuTTY\plink.exe"
$Pscp = "C:\Program Files\PuTTY\pscp.exe"

if (-not (Test-Path $Plink)) { throw "PuTTY plink not found at $Plink" }
if (-not (Test-Path $Pscp)) { throw "PuTTY pscp not found at $Pscp" }

function Invoke-Remote([string]$Command) {
    & $Plink -ssh -P $ServerPort -batch -pw $ServerPass "${ServerUser}@${ServerHost}" $Command
    if ($LASTEXITCODE -ne 0) { throw "Remote command failed: $Command" }
}

Write-Host "==> Testing SSH connection..."
Invoke-Remote "echo OK && uname -a"

Write-Host "==> Syncing code (excluding venv, media, db, staticfiles)..."
$ExcludeArgs = @(
    "-r", "-P", $ServerPort, "-pw", $ServerPass,
    "-x", "venv/*",
    "-x", "media/*",
    "-x", "staticfiles/*",
    "-x", "db.sqlite3",
    "-x", ".git/*",
    "-x", "__pycache__/*",
    "-x", "*.pyc"
)
& $Pscp @ExcludeArgs (Join-Path $ProjectRoot "*") "${ServerUser}@${ServerHost}:${RemotePath}/"
if ($LASTEXITCODE -ne 0) { throw "pscp sync failed" }

Write-Host "==> Running migrations, collectstatic, and restart..."
$DeployCmd = @"
set -e
cd $RemotePath
source venv/bin/activate
export DJANGO_DEBUG=false
pip install -r requirements.txt -q
python manage.py migrate --noinput
python manage.py collectstatic --noinput
python manage.py seed_site || true
systemctl restart gunicorn
systemctl is-active gunicorn
echo DEPLOY_OK
"@
Invoke-Remote $DeployCmd

Write-Host "Deploy finished successfully."
