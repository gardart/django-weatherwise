#!/usr/bin/env sh
set -e

# Ensure the directory for the SQLite database exists (useful for Docker volumes).
DB_DIR="$(dirname "${DJANGO_DB_PATH:-/data/weather.db}")"
mkdir -p "${DB_DIR}"

python weatherwise/manage.py migrate --noinput

# Create/ensure a Django superuser; logs a generated password if none supplied.
python weatherwise/manage.py shell <<'PY'
import os
import secrets
from django.contrib.auth import get_user_model

User = get_user_model()
username = os.environ.get("ADMIN_USERNAME", "admin")
email = os.environ.get("ADMIN_EMAIL", "admin@example.com")
password = os.environ.get("ADMIN_PASSWORD")

user, created = User.objects.get_or_create(
    username=username,
    defaults={"email": email, "is_staff": True, "is_superuser": True},
)

if created:
    if not password:
        password = secrets.token_urlsafe(16)
    user.set_password(password)
    user.email = email
    user.is_staff = True
    user.is_superuser = True
    user.save()
    print(f"[superuser] Created {username} ({email})")
    print(f"[superuser] Password: {password}")
else:
    if password:
        user.set_password(password)
        user.save()
        print(f"[superuser] Updated password for existing user {username}")
    else:
        print(f"[superuser] User {username} already exists; no changes")
PY

exec "$@"
