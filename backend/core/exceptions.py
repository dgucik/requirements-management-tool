class ApplicationError(Exception):
    """Base class for expected application-level errors."""


class BusinessRuleError(ApplicationError):
    """Base class for business rule violations."""


class EntityNotFoundError(ApplicationError):
    """Base class for expected missing-entity errors."""
