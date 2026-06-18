import uuid

from django.db import models
from django.utils import timezone


class UUIDMixin(models.Model):
    """
    UUID primary key for all domain entities.
    """

    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
    )

    class Meta:
        abstract = True


class TimeStampedMixin(models.Model):
    """
    Automatic timestamps.
    """

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )

    class Meta:
        abstract = True


class SoftDeleteMixin(models.Model):
    """
    Soft delete support.
    """

    is_deleted = models.BooleanField(
        default=False
    )

    deleted_at = models.DateTimeField(
        null=True,
        blank=True,
    )

    def soft_delete(self):
        self.is_deleted = True
        self.deleted_at = timezone.now()

        self.save(
            update_fields=[
                "is_deleted",
                "deleted_at",
            ]
        )

    class Meta:
        abstract = True
