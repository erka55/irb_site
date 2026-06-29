from django.db import models
from django.conf import settings
from django.core.exceptions import ValidationError

from apps.core.models import BaseModel
from apps.tenants.models import Tenant
from apps.protocols.models import Protocol


class Decision(BaseModel):
    """
    Official IRB decision record (requirements FR-007, workflow-v1.0 §3.6).
    Immutable once published — see BR-005 / BR-007.
    """

    class DecisionType(models.TextChoices):
        APPROVED             = "approved",            "Approved"
        CONDITIONAL_APPROVAL = "conditional_approval", "Conditional Approval"
        REVISION_REQUIRED    = "revision_required",    "Revision Required"
        REJECTED             = "rejected",              "Rejected"

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
    )

    decision_type = models.CharField(
        max_length=30,
        choices=DecisionType.choices,
    )

    quorum_met = models.BooleanField()

    is_published = models.BooleanField(default=False)
    published_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        db_table = "decisions"
        ordering = ["-created_at"]

    def __str__(self):
        return f"Decision #{self.pk} ({self.decision_type})"

    def clean(self):
        if not self.quorum_met:
            raise ValidationError(
                "Decision cannot be issued without quorum (BR-004)."
            )

    def save(self, *args, **kwargs):
        if self.pk:
            original = Decision.objects.filter(pk=self.pk).first()
            if original and original.is_published:
                raise ValueError("Published decisions are immutable.")

        self.full_clean()
        super().save(*args, **kwargs)
