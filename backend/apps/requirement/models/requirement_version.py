from django.db import models
from django.conf import settings

from core.models import BaseModel

from .feature import Feature
from .release_version import ReleaseVersion
from .requirement import Requirement


class RequirementVersion(BaseModel):
    """Store one versioned description of a requirement."""

    class Status(models.TextChoices):
        """Workflow states available for a requirement version."""

        DRAFT = "DRAFT", "Draft"
        PENDING = "PENDING", "Pending"
        APPROVED = "APPROVED", "Approved"
        REJECTED = "REJECTED", "Rejected"

    requirement = models.ForeignKey(
        Requirement,
        on_delete=models.CASCADE,
        related_name="versions",
        db_column="requirement_id",
    )
    based_on_version = models.ForeignKey(
        "self",
        on_delete=models.PROTECT,
        null=True,
        blank=True,
        related_name="derived_versions",
        db_column="based_on_version_id",
    )
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        null=True,
        blank=True,
        related_name="created_requirement_versions",
        db_column="created_by_id",
    )
    title = models.CharField(max_length=255)
    description = models.TextField()
    target_release_version = models.ForeignKey(
        ReleaseVersion,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="target_requirement_versions",
        db_column="target_release_version_id",
    )
    implemented_release_version = models.ForeignKey(
        ReleaseVersion,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="implemented_requirement_versions",
        db_column="implemented_release_version_id",
    )
    status = models.CharField(
        max_length=10,
        choices=Status.choices,
        default=Status.DRAFT,
    )
    version = models.PositiveIntegerField(default=1)
    feature = models.ForeignKey(
        Feature,
        on_delete=models.CASCADE,
        related_name="requirement_versions",
        db_column="feature_id",
    )
    is_deleted = models.BooleanField(default=False)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["requirement", "version"],
                name="unique_requirement_version_number",
            ),
        ]

    def __str__(self):
        """Return a readable requirement version label."""

        return f"{self.requirement.key} v{self.version}"
