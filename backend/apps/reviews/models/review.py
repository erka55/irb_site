from django.conf import settings
from django.db import models

from apps.core.models import BaseModel
from apps.tenants.models import Tenant


class ReviewStatus(models.TextChoices):
    ASSIGNED = "ASSIGNED", "Assigned"
    IN_PROGRESS = "IN_PROGRESS", "In Progress"
    SUBMITTED = "SUBMITTED", "Submitted"
    OVERDUE = "OVERDUE", "Overdue"


class ReviewRecommendation(models.TextChoices):
    APPROVE = "APPROVE", "Approve"
    APPROVE_WITH_CHANGES = (
        "APPROVE_WITH_CHANGES",
        "Approve With Changes",
    )
    DEFER = "DEFER", "Defer"
    REJECT = "REJECT", "Reject"


class Review(BaseModel):
    tenant = models.ForeignKey(
        Tenant,
        on_delete=models.PROTECT,
        related_name="reviews",
    )
    protocol = models.ForeignKey(
        "protocols.Protocol",
        on_delete=models.PROTECT,
        related_name="reviews",
    )
    reviewer = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        related_name="reviews",
    )
    status = models.CharField(
        max_length=30,
        choices=ReviewStatus.choices,
        default=ReviewStatus.ASSIGNED,
    )
    recommendation = models.CharField(
        max_length=50,
        choices=ReviewRecommendation.choices,
        null=True,
        blank=True,
    )
    score = models.DecimalField(
        max_digits=3,
        decimal_places=1,
        null=True,
        blank=True,
    )
    comments = models.TextField(blank=True, default="")
    due_date = models.DateTimeField()
    submitted_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        db_table = "reviews"
