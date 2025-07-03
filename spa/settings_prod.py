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

STATICFILES_DIRS = [BASE_DIR / "static_source"]

# Optional
AWS_S3_OBJECT_PARAMETERS = {
    "Expires": "Thu, 31 Dec 2099 20:00:00 GMT",
    "CacheControl": "max-age=94608000",
}
# Required
AWS_STORAGE_BUCKET_NAME = "spacoffehouse"
AWS_S3_REGION_NAME = "us-east-1"  # e.g. us-east-2
AWS_ACCESS_KEY_ID = os.environ.get("AWS_KEY")
AWS_SECRET_ACCESS_KEY = os.environ.get("AWS_SECRET")


STATICFILES_LOCATION = "static"
STATICFILES_STORAGE = "myspa.custom_storages.StaticStorage"

MEDIAFILES_LOCATION = "media"
DEFAULT_FILE_STORAGE = "myspa.custom_storages.MediaStorage"
