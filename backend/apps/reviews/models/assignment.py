from django.conf import settings
from django.db import models

from apps.protocols.models import Protocol
from apps.tenants.models import Tenant


class AssignmentRole(models.TextChoices):
    PRIMARY = "PRIMARY", "Primary"
    SECONDARY = "SECONDARY", "Secondary"


class ReviewAssignment(models.Model):
    tenant = models.ForeignKey(
        Tenant,
        on_delete=models.PROTECT,
        related_name="review_assignments",
    )

    protocol = models.ForeignKey(
        Protocol,
        on_delete=models.PROTECT,
        related_name="review_assignments",
    )

    reviewer = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        related_name="review_assignments",
    )

    role = models.CharField(
        max_length=20,
        choices=AssignmentRole.choices,
        default=AssignmentRole.PRIMARY,
    )

    assigned_at = models.DateTimeField(
        auto_now_add=True
    )

    class Meta:
        db_table = "review_assignments"
