from core.exceptions import (
    BusinessRuleError,
    EntityNotFoundError,
    PermissionDeniedError,
)


class ProjectNameRequiredError(BusinessRuleError):
    """Raised when a project is created without a non-empty name."""


class UserNotFoundError(EntityNotFoundError):
    """Raised when a referenced user does not exist."""


class ProjectNotFoundError(EntityNotFoundError):
    """Raised when a referenced project does not exist."""


class ProjectDeletionForbiddenError(PermissionDeniedError):
    """Raised when a non-owner tries to delete a project."""


class ProjectUpdateForbiddenError(PermissionDeniedError):
    """Raised when a non-owner tries to update a project."""


class ProjectMembershipManagementForbiddenError(PermissionDeniedError):
    """Raised when a user cannot manage project memberships."""


class ProjectMembershipOwnerRoleForbiddenError(BusinessRuleError):
    """Raised when membership creation attempts to assign the Owner role."""


class ProjectMembershipAlreadyExistsError(BusinessRuleError):
    """Raised when a user already belongs to a project."""
