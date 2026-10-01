from core.exceptions import BusinessRuleError, EntityNotFoundError


class ProjectNameRequiredError(BusinessRuleError):
    """Raised when a project is created without a non-empty name."""


class UserNotFoundError(EntityNotFoundError):
    """Raised when a referenced user does not exist."""
