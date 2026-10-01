class ApplicationError(Exception):
    """Base class for expected application-level errors."""

    def __init__(self, message: str, extra: dict | None = None):
        self.message = message
        self.extra = extra or {}
        super().__init__(message)


class BusinessRuleError(ApplicationError):
    """Base class for business rule violations."""


class EntityNotFoundError(ApplicationError):
    """Base class for expected missing-entity errors."""


class PermissionDeniedError(ApplicationError):
    """Base class for expected authorization failures."""
