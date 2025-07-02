import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": os.environ.get("DBNAME"),
        "USER": os.environ.get("DBUSER"),
        "PASSWORD": os.environ.get("DBPASS"),
        "HOST": os.environ.get("DBHOST", "127.0.0.1"),
        "PORT": os.environ.get("DBPORT", "5432"),
    }
}

DEBUG = False
ALLOWED_HOSTS = ["13.222.4.243"]

STATIC_URL = "/static/"
STATIC_ROOT = BASE_DIR / "static"
MEDIA_ROOT = "media"
