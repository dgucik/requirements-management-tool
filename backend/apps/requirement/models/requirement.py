from django.db import models

from core.models import BaseModel


class Requirement(BaseModel):
    """Identify a requirement independently from its versions."""

    key = models.CharField(max_length=100, unique=True)

    def __str__(self):
        """Return the requirement key."""

        return self.key
