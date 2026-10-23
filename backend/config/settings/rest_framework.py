REST_FRAMEWORK = {
    "DEFAULT_SCHEMA_CLASS": "drf_spectacular.openapi.AutoSchema",
    "DEFAULT_AUTHENTICATION_CLASSES": [
        "rest_framework_simplejwt.authentication.JWTAuthentication",
    ],
    "EXCEPTION_HANDLER": "core.exception_handlers.api_exception_handler",
    "DEFAULT_PERMISSION_CLASSES": [
        "rest_framework.permissions.IsAuthenticated",
    ],
}

SPECTACULAR_SETTINGS = {
    "TITLE": "Requirements Management API",
    "DESCRIPTION": "API for the Requirements Management Tool.",
    "VERSION": "1.0.0",
    "TAGS": [
        {
            "name": "Projects",
            "description": "Create, list, update, and delete projects.",
        },
        {
            "name": "Requirements",
            "description": "Create and list project requirements and versions.",
        },
        {"name": "Features", "description": "Create project features."},
        {
            "name": "Project memberships",
            "description": "Manage project members and roles.",
        },
    ],
}
