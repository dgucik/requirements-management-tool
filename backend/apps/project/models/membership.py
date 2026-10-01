from django.conf import settings
from django.db import models

from core.models import BaseModel
from .project import Project


class ProjectMembership(BaseModel):
    """Associate a user with a project and define the user's project role."""

    class Role(models.TextChoices):
        """Roles available to project members."""

        VIEWER = "Viewer", "Viewer"
        EDITOR = "Editor", "Editor"
        MODERATOR = "Moderator", "Moderator"
        OWNER = "Owner", "Owner"

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="project_memberships",
        db_column="user_id",
    )
    project = models.ForeignKey(
        Project,
        on_delete=models.CASCADE,
        related_name="memberships",
        db_column="project_id",
    )
    role = models.CharField(max_length=10, choices=Role.choices)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["user", "project"],
                name="unique_project_membership_user_project",
            )
        ]

    def __str__(self):
        """Return a human-readable membership label."""

        return f"{self.user} - {self.project} ({self.role})"
