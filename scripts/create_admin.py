import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
django.setup()

from django.contrib.auth import get_user_model

User = get_user_model()

username = os.environ.get("ADMIN_USERNAME", "admin")
password = os.environ.get("ADMIN_PASSWORD")
email = os.environ.get("ADMIN_EMAIL", "admin@farazbamgostar.ir")

if not password:
    raise RuntimeError("ADMIN_PASSWORD is not set in the environment.")

user, created = User.objects.get_or_create(
    username=username,
    defaults={
        "email": email,
        "is_staff": True,
        "is_superuser": True,
    },
)

user.email = email
user.is_staff = True
user.is_superuser = True
user.set_password(password)
user.save()

print("created" if created else "updated")