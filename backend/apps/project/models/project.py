from django.db import models

from core.models import BaseModel


class Project(BaseModel):
    """A project that groups requirements and project members."""

    name = models.CharField(max_length=255)

    def __str__(self):
        """Return the project's display name."""

        return self.name
