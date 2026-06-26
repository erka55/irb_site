from django.db import models

from apps.core.models import BaseModel
from apps.protocols.models import Protocol
from apps.users.models import User

from apps.decision.enums import DecisionType


class Decision(BaseModel):

    protocol = models.ForeignKey(
        Protocol,
        on_delete=models.CASCADE,
        related_name="decisions",
    )

    decision_type = models.CharField(
        max_length=50,
        choices=DecisionType.choices,
    )

    decision_date = models.DateField()

    meeting_reference = models.CharField(
        max_length=255,
        blank=True,
    )

    rationale = models.TextField()

    created_by = models.ForeignKey(
        User,
        on_delete=models.PROTECT,
        related_name="created_decisions",
    )

    class Meta:
        db_table = "decisions"
        ordering = ["-decision_date"]

    def __str__(self):
        return (
            f"{self.protocol.protocol_number}"
            f" - {self.decision_type}"
        )
