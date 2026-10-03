#!/bin/bash
set -euo pipefail

cd /var/www/farazbam

echo "==> Backup local changes"
cp -a config/settings.py /tmp/farazbam-settings.py.bak 2>/dev/null || true
cp -a core/migrations/0005_alter_sitesettings_hero_subtitle_and_more.py /tmp/0005_alter.bak 2>/dev/null || true

echo "==> Stash tracked local edits"
git stash push -m "pre-deploy-$(date +%Y%m%d-%H%M)" config/settings.py || true

echo "==> Remove server-only migration file (already applied in DB)"
rm -f core/migrations/0005_alter_sitesettings_hero_subtitle_and_more.py

echo "==> Fix migration history for repo 0005_team_member"
source venv/bin/activate
python <<'PY'
import os, django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
django.setup()
from django.db import connection
with connection.cursor() as c:
    c.execute(
        "DELETE FROM django_migrations WHERE app=%s AND name=%s",
        ["core", "0005_alter_sitesettings_hero_subtitle_and_more"],
    )
    print("Removed old 0005_alter migration record:", c.rowcount)
PY

echo "==> Pull latest code"
git fetch origin
git pull --ff-only origin main

echo "==> Install deps, migrate, collectstatic"
export DJANGO_DEBUG=false
pip install -r requirements.txt -q
python manage.py migrate --noinput
python manage.py collectstatic --noinput
python manage.py seed_site || true

echo "==> Restart gunicorn"
systemctl restart gunicorn
systemctl is-active gunicorn

echo "==> Migration status"
python manage.py showmigrations core | tail -10

echo "DEPLOY_OK"
