import os

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

STATIC_URL = "static_source/"

STATIC_ROOT = "static"
STATICFILES_DIRS = ["static_source"]

MEDIA_ROOT = "media"
