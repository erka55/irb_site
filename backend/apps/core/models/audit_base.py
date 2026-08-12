from django.db import models

from .mixins import UUIDMixin, TimeStampedMixin


class AuditBaseModel(
    UUIDMixin,
    TimeStampedMixin,
):
    """
    Base model for immutable audit records.

    Audit records intentionally do not include SoftDeleteMixin.
    """

    class Meta:
        abstract = True
