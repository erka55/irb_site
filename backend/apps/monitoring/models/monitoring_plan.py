from django.db import models

from apps.core.models import BaseModel
from apps.protocols.models import Protocol
from apps.tenants.models import Tenant


class MonitoringFrequency(models.TextChoices):
    THREE_MONTHS = "3_MONTHS", "Every 3 months"
    SIX_MONTHS = "6_MONTHS", "Every 6 months"


class MonitoringPlanStatus(models.TextChoices):
    ACTIVE = "ACTIVE", "Active"
    COMPLETED = "COMPLETED", "Completed"
    SUSPENDED = "SUSPENDED", "Suspended"
    TERMINATED = "TERMINATED", "Terminated"


class MonitoringPlan(BaseModel):

    tenant = models.ForeignKey(
        Tenant,
        on_delete=models.CASCADE,
        related_name="monitoring_plans",
    )

    protocol = models.OneToOneField(
        Protocol,
        on_delete=models.CASCADE,
        related_name="monitoring_plan",
    )

    frequency = models.CharField(
        max_length=20,
        choices=MonitoringFrequency.choices,
    )

    status = models.CharField(
        max_length=20,
        choices=MonitoringPlanStatus.choices,
        default=MonitoringPlanStatus.ACTIVE,
    )

    next_due_date = models.DateField(
        null=True,
        blank=True,
    )

    last_completed_at = models.DateTimeField(
        null=True,
        blank=True,
    )

    class Meta:
        db_table = "monitoring_plans"
        ordering = ["next_due_date"]

    def __str__(self):
        return f"Monitoring plan - {self.protocol}"
