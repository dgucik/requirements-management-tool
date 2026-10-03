from django.db import models

from core.models import BaseModel


class ReleaseVersion(BaseModel):
    """Represent a named product release to which requirements can be tied."""

    name = models.CharField(max_length=255, unique=True)

    def __str__(self):
        """Return the release version name."""

        return self.name
