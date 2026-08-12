from django.conf import settings
from django.db import models

from apps.core.models import AuditBaseModel
from apps.tenants.models import Tenant


class AuditLog(AuditBaseModel):

    tenant = models.ForeignKey(
        Tenant,
        on_delete=models.PROTECT,
        related_name="audit_logs",
        null=True,
        blank=True,
    )

    actor = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        related_name="audit_logs",
        null=True,
        blank=True,
    )

    event_id = models.UUIDField(
        unique=True,
        null=True,
        blank=True,
    )

    occurred_at = models.DateTimeField(
        null=True,
        blank=True,
    )

    action = models.CharField(
        max_length=100,
    )

    entity_type = models.CharField(
        max_length=100,
    )

    entity_id = models.UUIDField()

    payload = models.JSONField(
        default=dict,
        blank=True,
    )

    ip_address = models.GenericIPAddressField(
        null=True,
        blank=True,
    )

    user_agent = models.TextField(
        blank=True,
    )

    class Meta:
        db_table = "audit_logs"

        ordering = [
            "-occurred_at",
            "-created_at",
        ]

    def __str__(self):
        return (
            f"{self.action} "
            f"({self.entity_type})"
        )

    def save(self, *args, **kwargs):

        if self.pk and AuditLog.objects.filter(
            pk=self.pk
        ).exists():
            raise ValueError(
                "Audit logs are immutable."
            )

        super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        raise ValueError(
            "Audit logs cannot be deleted."
        )
