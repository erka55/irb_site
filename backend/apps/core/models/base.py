from django.db import models

from .mixins import (
    UUIDMixin,
    TimeStampedMixin,
    SoftDeleteMixin,
)


class BaseModel(
    UUIDMixin,
    TimeStampedMixin,
    SoftDeleteMixin,
):
    """
    Base model for all domain entities.
    """

    class Meta:
        abstract = True
