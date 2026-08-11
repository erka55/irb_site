from django.db import models

from apps.core.models import BaseModel
from apps.protocols.models import Protocol
from apps.tenants.models import Tenant
from apps.users.models import User

from .monitoring_plan import MonitoringPlan


class IncidentReportType(models.TextChoices):
    PARTICIPANT_SAFETY = (
        "PARTICIPANT_SAFETY",
        "Human rights or participant safety concern",
    )
    UNAPPROVED_PROTOCOL_CHANGE = (
        "UNAPPROVED_PROTOCOL_CHANGE",
        "Unapproved research purpose or methodology change",
    )
    SERIOUS_UNEXPECTED_EVENT = (
        "SERIOUS_UNEXPECTED_EVENT",
        "Serious unexpected event",
    )


class IncidentReportStatus(models.TextChoices):
    SUBMITTED = "SUBMITTED", "Submitted"
    UNDER_REVIEW = "UNDER_REVIEW", "Under review"
    ACTION_REQUIRED = "ACTION_REQUIRED", "Action required"
    RESOLVED = "RESOLVED", "Resolved"
    CLOSED = "CLOSED", "Closed"


class IncidentReport(BaseModel):

    tenant = models.ForeignKey(
        Tenant,
        on_delete=models.CASCADE,
        related_name="incident_reports",
    )

    protocol = models.ForeignKey(
        Protocol,
        on_delete=models.CASCADE,
        related_name="incident_reports",
    )

    monitoring_plan = models.ForeignKey(
        MonitoringPlan,
        on_delete=models.CASCADE,
        related_name="incident_reports",
    )

    reported_by = models.ForeignKey(
        User,
        on_delete=models.PROTECT,
        related_name="reported_incidents",
    )

    incident_type = models.CharField(
        max_length=40,
        choices=IncidentReportType.choices,
    )

    status = models.CharField(
        max_length=20,
        choices=IncidentReportStatus.choices,
        default=IncidentReportStatus.SUBMITTED,
    )

    occurred_at = models.DateTimeField()

    reported_at = models.DateTimeField(
        null=True,
        blank=True,
    )

    description = models.TextField()

    review_notes = models.TextField(
        blank=True,
    )

    reviewed_by = models.ForeignKey(
        User,
        on_delete=models.PROTECT,
        related_name="reviewed_incident_reports",
        null=True,
        blank=True,
    )

    reviewed_at = models.DateTimeField(
        null=True,
        blank=True,
    )

    class Meta:
        db_table = "incident_reports"
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.protocol} - {self.incident_type}"
