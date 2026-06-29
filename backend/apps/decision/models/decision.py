from django.db import models
from django.conf import settings

from apps.core.models import BaseModel
from apps.tenants.models import Tenant
from apps.protocols.models import Protocol


class Decision(BaseModel):
    """
    Core IRB decision record.
    """

    class Status(models.TextChoices):
        DRAFT       = "draft",       "Draft"
        PENDING     = "pending",     "Pending"
        APPROVED    = "approved",    "Approved"
        CONDITIONAL = "conditional", "Conditional Approval"
        REJECTED    = "rejected",    "Rejected"
        WITHDRAWN   = "withdrawn",   "Withdrawn"

    tenant = models.ForeignKey(
        Tenant,
        on_delete=models.CASCADE,
        related_name="decisions",
    )

    protocol = models.ForeignKey(
        Protocol,
        on_delete=models.CASCADE,
        related_name="decisions",
    )

    decided_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        related_name="decisions_made",
        null=True,
        blank=True,
        help_text="Шийдвэр гаргасан хэрэглэгч (Chair/PC гишүүн)",
    )

    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.DRAFT,
    )

    class Meta:
        db_table = "decisions"
        ordering = ["-created_at"]

    def __str__(self):
        return f"Decision #{self.pk} ({self.status})"
