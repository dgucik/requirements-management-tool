from core.exceptions import BusinessRuleError, EntityNotFoundError


class ProjectNameRequiredError(BusinessRuleError):
    """Raised when a project is created without a name."""


class UserNotFoundError(EntityNotFoundError):
    """Raised when a referenced user cannot be found."""
