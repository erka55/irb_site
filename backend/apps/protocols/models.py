from django.db import models

from apps.core.models import BaseModel
from apps.tenants.models import Tenant
from apps.users.models import User

from .enums import (
    ProtocolStatus,
    RiskLevel,
)

class Protocol(BaseModel):

    tenant = models.ForeignKey(
        Tenant,
        on_delete=models.CASCADE,
        related_name="protocols",
    )

    title = models.CharField(
        max_length=500,
    )

    protocol_number = models.CharField(
        max_length=50,
        unique=True,
    )

    principal_investigator = models.ForeignKey(
        User,
        on_delete=models.PROTECT,
        related_name="investigator_protocols",
    )

    risk_level = models.CharField(
        max_length=20,
        choices=RiskLevel.choices,
    )

    status = models.CharField(
        max_length=30,
        choices=ProtocolStatus.choices,
        default=ProtocolStatus.DRAFT,
    )

    summary = models.TextField(
        blank=True,
    )

    class Meta:
        db_table = "protocols"
        ordering = ["-created_at"]

    def __str__(self):
        return self.title


class ProtocolVersion(BaseModel):

    protocol = models.ForeignKey(
        Protocol,
        on_delete=models.CASCADE,
        related_name="versions",
    )

    version_number = models.CharField(
        max_length=20,
    )

    snapshot = models.JSONField()

    created_by = models.ForeignKey(
        User,
        on_delete=models.PROTECT,
        related_name="created_protocol_versions",
    )

    class Meta:
        db_table = "protocol_versions"
        ordering = ["-created_at"]


class ProtocolStatusHistory(BaseModel):

    protocol = models.ForeignKey(
        Protocol,
        on_delete=models.CASCADE,
        related_name="status_history",
    )

    from_status = models.CharField(
        max_length=30,
        blank=True,
    )

    to_status = models.CharField(
        max_length=30,
    )

    changed_by = models.ForeignKey(
        User,
        on_delete=models.PROTECT,
        related_name="protocol_status_changes",
    )
    
    reason = models.TextField(
        blank=True,
    )

    class Meta:
        db_table = "protocol_status_history"
        ordering = ["-created_at"]
