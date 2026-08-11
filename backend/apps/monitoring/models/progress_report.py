from django.db import models

from apps.core.models import BaseModel
from apps.protocols.models import Protocol
from apps.tenants.models import Tenant
from apps.users.models import User

from .monitoring_plan import MonitoringPlan


class ProgressReportType(models.TextChoices):
    PERIODIC = "PERIODIC", "Periodic"
    FINAL = "FINAL", "Final"


class ProgressReportStatus(models.TextChoices):
    DRAFT = "DRAFT", "Draft"
    SUBMITTED = "SUBMITTED", "Submitted"
    UNDER_REVIEW = "UNDER_REVIEW", "Under review"
    ACCEPTED = "ACCEPTED", "Accepted"
    ADDITIONAL_INFORMATION_REQUIRED = (
        "ADDITIONAL_INFORMATION_REQUIRED",
        "Additional information required",
    )


class ProgressReport(BaseModel):

    tenant = models.ForeignKey(
        Tenant,
        on_delete=models.CASCADE,
        related_name="progress_reports",
    )

    protocol = models.ForeignKey(
        Protocol,
        on_delete=models.CASCADE,
        related_name="progress_reports",
    )

    monitoring_plan = models.ForeignKey(
        MonitoringPlan,
        on_delete=models.CASCADE,
        related_name="progress_reports",
    )

    submitted_by = models.ForeignKey(
        User,
        on_delete=models.PROTECT,
        related_name="submitted_progress_reports",
    )

    report_type = models.CharField(
        max_length=20,
        choices=ProgressReportType.choices,
    )

    status = models.CharField(
        max_length=40,
        choices=ProgressReportStatus.choices,
        default=ProgressReportStatus.DRAFT,
    )

    period_start = models.DateField()

    period_end = models.DateField()

    submitted_at = models.DateTimeField(
        null=True,
        blank=True,
    )

    summary = models.TextField(
        blank=True,
    )

    issues = models.TextField(
        blank=True,
    )

    review_notes = models.TextField(
        blank=True,
    )

    reviewed_by = models.ForeignKey(
        User,
        on_delete=models.PROTECT,
        related_name="reviewed_progress_reports",
        null=True,
        blank=True,
    )

    reviewed_at = models.DateTimeField(
        null=True,
        blank=True,
    )

    class Meta:
        db_table = "progress_reports"
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.protocol} - {self.report_type} report"
