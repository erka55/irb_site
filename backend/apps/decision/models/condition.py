from django.db import models

from apps.core.models import BaseModel


class DecisionCondition(BaseModel):

    decision = models.ForeignKey(
        "decision.Decision",
        on_delete=models.CASCADE,
        related_name="conditions",
    )

    description = models.TextField()

    order = models.PositiveIntegerField(
        default=1,
    )

    class Meta:
        db_table = "decision_conditions"
        ordering = ["order"]

    def __str__(self):
        return self.description[:50]
