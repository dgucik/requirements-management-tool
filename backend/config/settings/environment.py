import os
from pathlib import Path

from dotenv import load_dotenv


BASE_DIR = Path(__file__).resolve().parent.parent.parent
load_dotenv(BASE_DIR / ".env")


def get_env(name, default=None):
    return os.getenv(name, default)


def get_bool_env(name, default=False):
    return get_env(name, str(default)).lower() in {"1", "true", "yes", "on"}


def get_list_env(name, default=""):
    return [item.strip() for item in get_env(name, default).split(",") if item.strip()]


SECRET_KEY = get_env("DJANGO_SECRET_KEY", "django-insecure-change-me-in-production")
DEBUG = get_bool_env("DJANGO_DEBUG", True)
ALLOWED_HOSTS = get_list_env("DJANGO_ALLOWED_HOSTS")
