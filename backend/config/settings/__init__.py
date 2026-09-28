"""Django settings package.

The public settings module remains ``config.settings``. Django imports this
package, while the individual modules keep related settings together.
"""

from .auth import AUTH_PASSWORD_VALIDATORS
from .environment import (
    ALLOWED_HOSTS,
    BASE_DIR,
    DEBUG,
    SECRET_KEY,
)
from .database import DATABASES
from .installed_apps import INSTALLED_APPS
from .localization import LANGUAGE_CODE, TIME_ZONE, USE_I18N, USE_TZ
from .middleware import MIDDLEWARE
from .rest_framework import REST_FRAMEWORK
from .static_files import DEFAULT_AUTO_FIELD, STATIC_URL
from .templates import TEMPLATES
from .urls import ROOT_URLCONF, WSGI_APPLICATION

__all__ = [
    "ALLOWED_HOSTS",
    "AUTH_PASSWORD_VALIDATORS",
    "BASE_DIR",
    "DATABASES",
    "DEBUG",
    "DEFAULT_AUTO_FIELD",
    "INSTALLED_APPS",
    "LANGUAGE_CODE",
    "MIDDLEWARE",
    "REST_FRAMEWORK",
    "ROOT_URLCONF",
    "SECRET_KEY",
    "STATIC_URL",
    "TEMPLATES",
    "TIME_ZONE",
    "USE_I18N",
    "USE_TZ",
    "WSGI_APPLICATION",
]
