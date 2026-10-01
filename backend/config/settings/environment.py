import os
from pathlib import Path

from dotenv import load_dotenv


BASE_DIR = Path(__file__).resolve().parent.parent.parent
load_dotenv(BASE_DIR / ".env")


def get_env(name, default=None):
    """Read an environment variable, returning a fallback when it is missing.

    Args:
        name: Environment variable name.
        default: Value returned when the variable is not set.

    Returns:
        The environment value or the provided default.
    """

    return os.getenv(name, default)


def get_bool_env(name, default=False):
    """Read a boolean environment variable.

    Args:
        name: Environment variable name.
        default: Boolean fallback when the variable is not set.

    Returns:
        Whether the normalized value represents an enabled flag.
    """

    return get_env(name, str(default)).lower() in {"1", "true", "yes", "on"}


def get_list_env(name, default=""):
    """Read a comma-separated environment variable as a trimmed list.

    Args:
        name: Environment variable name.
        default: Comma-separated fallback value.

    Returns:
        Non-empty, trimmed values from the environment variable.
    """

    return [item.strip() for item in get_env(name, default).split(",") if item.strip()]


SECRET_KEY = get_env("DJANGO_SECRET_KEY", "django-insecure-change-me-in-production")
DEBUG = get_bool_env("DJANGO_DEBUG", True)
ALLOWED_HOSTS = get_list_env("DJANGO_ALLOWED_HOSTS")
