from core.exceptions import BusinessRuleError, EntityNotFoundError


class ProjectNameRequiredError(BusinessRuleError):
    """Raised when a project is created without a name."""


class ProjectOwnerNotFoundError(EntityNotFoundError):
    """Raised when the project owner cannot be found."""
