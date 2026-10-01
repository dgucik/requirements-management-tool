from django.apps import AppConfig


class ProjectConfig(AppConfig):
    """Configure the project Django application."""

    default_auto_field = "django.db.models.BigAutoField"
    name = "apps.project"
