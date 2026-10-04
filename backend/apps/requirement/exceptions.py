from core.exceptions import BusinessRuleError, EntityNotFoundError, PermissionDeniedError


class RequirementCreationForbiddenError(PermissionDeniedError):
    """Raised when a user cannot create requirements in a project."""


class RequirementFeatureNotFoundError(EntityNotFoundError):
    """Raised when the selected feature does not belong to the project."""


class RequirementTitleRequiredError(BusinessRuleError):
    """Raised when the first requirement version has no title."""


class RequirementDescriptionRequiredError(BusinessRuleError):
    """Raised when the first requirement version has no description."""
