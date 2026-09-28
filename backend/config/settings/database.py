from pathlib import Path

from .environment import BASE_DIR, get_env


DATABASE_ENGINE = get_env("DJANGO_DB_ENGINE", "sqlite").lower()

if DATABASE_ENGINE in {"sqlite", "sqlite3"}:
    database_name = Path(get_env("DJANGO_DB_NAME", "db.sqlite3"))
    if not database_name.is_absolute():
        database_name = BASE_DIR / database_name

    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.sqlite3",
            "NAME": database_name,
        }
    }
elif DATABASE_ENGINE in {"postgres", "postgresql"}:
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.postgresql",
            "NAME": get_env("DJANGO_DB_NAME", "requirements_management"),
            "USER": get_env("DJANGO_DB_USER", "postgres"),
            "PASSWORD": get_env("DJANGO_DB_PASSWORD", ""),
            "HOST": get_env("DJANGO_DB_HOST", "localhost"),
            "PORT": get_env("DJANGO_DB_PORT", "5432"),
        }
    }
else:
    raise ValueError("Unsupported DJANGO_DB_ENGINE. Use 'sqlite' or 'postgresql'.")
